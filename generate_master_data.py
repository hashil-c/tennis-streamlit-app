import datetime
import json

import numpy as np

from calculator import Calculator, TableEntry
from constants import Constants
import pandas as pd
from data import games, players
import math


def generate_dataframe_data(table_entries):
    """Reformat table entries into data that can be used in a dataframe"""
    df_data = []
    for count, entry in enumerate(table_entries):
        row = {"game_number": count, 'date': entry.game.date.strftime("%Y-%m-%d") if entry.game is not None else None}
        for key, value in entry.__dict__.items():
            if key != 'game':
                row[value['player'].name] = value['score']
        df_data.append(row)
    return df_data


def generate_player_stats(scores_df):
    """Get the player stats for each player"""
    stats = {}
    for player in players:
        processing_df = scores_df[['game_number', 'date', player.name]].copy()
        processing_df['diff'] = processing_df[player.name].diff()
        data = {
            "Match Participation %": (processing_df[processing_df['diff'] != 0].shape[0]) / processing_df.shape[
                0] * 100,
            "Highest Elo": float(processing_df[player.name].max()),
            "Lowest Elo": float(processing_df[player.name].min()),
            "Best Points Change": float(processing_df["diff"].max()),
            "Worst Points Change": float(processing_df["diff"].min()),
            "Total Points Lost": float(processing_df[processing_df["diff"] < 0]["diff"].sum()),
            "Total Points Gained": float(processing_df[processing_df["diff"] > 0]["diff"].sum()),
            "No. Games w Elo Gain": int(processing_df[processing_df["diff"] > 0]["diff"].shape[0]),
            "No. Games w Elo Loss": int(processing_df[processing_df["diff"] < 0]["diff"].shape[0]),
            "Standard Deviation": float(processing_df[processing_df["diff"] != 0][player.name].std()),
        }
        stats[player.name] = data
    return stats


def generate_interaction_matrix():
    """Return the interaction matrix for each player"""
    output = {}
    for focus_player in players:
        player_dict = {player.name: {"teammate": 0, "opponent": 0} for player in players}
        teammates = []
        opponents = []
        for game in games:
            team_1 = [player.name for player in game.team_1]
            team_2 = [player.name for player in game.team_2]
            if focus_player.name in team_1:
                temp_teammates = set(team_1) - set([focus_player.name])
                temp_opponents = set(team_2)
            elif focus_player.name in team_2:
                temp_teammates = set(team_2) - set([focus_player.name])
                temp_opponents = set(team_1)
            else:
                temp_teammates = set()
                temp_opponents = set()
            teammates.extend(list(temp_teammates))
            opponents.extend(list(temp_opponents))
        for name in teammates:
            player_dict[name]['teammate'] += 1
        for name in opponents:
            player_dict[name]['opponent'] += 1
        player_dict.pop(focus_player.name)
        output[focus_player.name] = player_dict
    return output


def generate_average_expected_score(game_data):
    """Generate average expected score"""
    df = pd.DataFrame(game_data)
    # Step 1: Explode team_1
    team1_df = df[['team_1', 'team_1_exp_score_pct']].explode('team_1')
    team1_df.columns = ['player', 'expected_score']

    # Step 2: Explode team_2
    team2_df = df[['team_2', 'team_2_exp_score_pct']].explode('team_2')
    team2_df.columns = ['player', 'expected_score']

    # Step 3: Combine both
    all_players_df = pd.concat([team1_df, team2_df])

    # Step 4: Compute average expected score
    output = []
    for player, player_df in all_players_df.groupby('player'):
        last_10_games = player_df.tail(10)
        output.append({'player': player, 'expected_win_pct_last_10': round(last_10_games['expected_score'].mean(), 1)})

    df = pd.DataFrame(output)
    df['rank'] = df["expected_win_pct_last_10"].rank(method='min', ascending=False).astype(int)
    # df['expected_win'] = df['expected_win_pct_last_10'] / 100
    # df['elo_difference'] = df['expected_win'].apply(lambda delta: 400*math.log(-delta/(delta - 1))/math.log(10) + 1000)
    df.set_index('player', drop=True, inplace=True)
    return df.to_dict(orient='index')


def generate_points_to_win_percent_bucketed(game_data):
    df = pd.DataFrame(game_data)
    df['elo_change'] = np.where(
        df['team_2_score_pct'] < df['team_2_exp_score_pct'],
        df['elo_change'] * -1,
        df['elo_change']
    )

    # Step 1: Explode team_1
    team1_df = df[['team_1', 'team_1_exp_score_pct', 'elo_change']].explode('team_1')
    team1_df.columns = ['player', 'expected_score', 'elo_diff']
    team1_df['elo_diff'] = team1_df['elo_diff'] * -1

    # Step 2: Explode team_2
    team2_df = df[['team_2', 'team_2_exp_score_pct', 'elo_change']].explode('team_2')
    team2_df.columns = ['player', 'expected_score', 'elo_diff']

    # Step 3: Combine both
    all_players_df = pd.concat([team1_df, team2_df])

    output = {}
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0 - >10', '10 - >20', '20 - >30', '30 - >40', '40 - >50', '50 - >60', '60 - >70', '70 - >80',
              '80 - >90', '90 - >100']
    for player, player_df in all_players_df.groupby('player'):
        player_df['win_chance_range'] = pd.cut(player_df['expected_score'], bins=bins, labels=labels, right=False)

        # Create 'won' and 'lost' columns
        player_df['gained'] = player_df['elo_diff'].apply(lambda x: x if x > 0 else 0)
        player_df['lost'] = player_df['elo_diff'].apply(lambda x: x if x < 0 else 0)

        # Group by the new 'win_chance_range' and sum the 'won' and 'lost' columns
        grouped_df = player_df.groupby('win_chance_range', observed=False)[['gained', 'lost']].sum()
        # Group into longshot, unlikely, fair, likely, walkover
        output[player] = grouped_df.to_dict()
    return output


def generate_trendline_data(df_data):
    """Generate the trendline for each player."""
    df = pd.DataFrame(df_data)

    def linear_regression_calc(linear_df, player_name):
        y_bar = linear_df[player_name].mean()
        linear_df['num'] = range(len(linear_df))
        linear_df['y-ybar'] = linear_df[player_name] - y_bar
        linear_df['x-xbar'] = linear_df['num'] - linear_df['num'].mean()
        linear_df['y-ybar * x-xbar'] = linear_df['y-ybar'] * linear_df['x-xbar']
        linear_df['x-xbar ^2'] = linear_df['x-xbar'] ** 2
        gradient = linear_df['y-ybar * x-xbar'].sum() / linear_df['x-xbar ^2'].sum()
        return gradient, y_bar


    output = {}
    new_df_output = []
    for player in players:
        target_column = df[player.name]
        unique_values = target_column.drop_duplicates().reset_index(drop=True)
        unique_values_df = pd.DataFrame(unique_values)
        gradient, y_intercept = linear_regression_calc(unique_values_df, player.name)
        last_10_rows_df = unique_values_df.tail(10).copy()
        gradient_last_ten, _ = linear_regression_calc(last_10_rows_df, player.name)
        output[player.name] = {"Improvement (Overall)": round(gradient, 2), "Estimated Starting Elo": round(y_intercept, 2), "Improvement (Last 10 Games)": round(gradient_last_ten, 2)}
        new_df_output.append({'Player': player.name, "Improvement (Overall)": round(gradient, 2), "Estimated Starting Elo": round(y_intercept, 2), "Improvement (Last 10 Games)": round(gradient_last_ten, 2)})
    trend_df = pd.DataFrame(new_df_output)
    trend_df = trend_df.replace(np.nan, 0)
    trend_df['Improvement (Overall) Rank'] = trend_df["Improvement (Overall)"].rank(method='min', ascending=False).astype(int)
    trend_df['Improvement (Last 10 Games) Rank'] = trend_df["Improvement (Last 10 Games)"].rank(method='min', ascending=False).astype(int)
    trend_df['Estimated Starting Elo Rank'] = trend_df["Estimated Starting Elo"].rank(method='min', ascending=False).astype(int)
    trend_df.set_index('Player', drop=True, inplace=True)

    return trend_df.to_dict(orient='index')


if __name__ == '__main__':
    player_dict = {}
    for player in players:
        player_dict[player] = Constants.starting_elo
    initial_entry = TableEntry(game=None, player_dict=player_dict)
    calculator = Calculator(starting_entry=initial_entry)
    table_entries, game_data = calculator.process_game(games=games)
    output_data = {}
    df_data = generate_dataframe_data(table_entries=table_entries)
    output_data['table'] = df_data

    singles_games = [game for game in games if len(game.team_1) == 1 and len(game.team_2) == 1]
    singles_table_entries, singles_game_data = calculator.process_game(games=singles_games)
    output_data['singles_latest_table'] = generate_dataframe_data(table_entries=[singles_table_entries[-1]])

    doubles_games = [game for game in games if len(game.team_1) == 2 and len(game.team_2) == 2]
    doubles_table_entries, doubles_game_data = calculator.process_game(games=doubles_games)
    output_data['doubles_latest_table'] = generate_dataframe_data(table_entries=[doubles_table_entries[-1]])

    output_data['trends'] = generate_trendline_data(df_data=df_data)

    output_data['games'] = game_data
    output_data['average_expected_score'] = generate_average_expected_score(game_data)
    output_data['points_to_win_percent_bucketed'] = generate_points_to_win_percent_bucketed(game_data)
    scores_df = pd.DataFrame(df_data)
    output_data['player_stats'] = generate_player_stats(scores_df=scores_df)
    output_data['interaction_matrix'] = generate_interaction_matrix()
    with open('master_data.json', 'w') as file:
        try:
            json.dump(output_data, file, indent=4)
        except Exception as e:
            something = 'hello'
