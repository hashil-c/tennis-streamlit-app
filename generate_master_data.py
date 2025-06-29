import datetime
import json

from calculator import Calculator, TableEntry
from constants import Constants
import pandas as pd
from data import games, players


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
            "Highest Elo": processing_df[player.name].max(),
            "Lowest Elo": processing_df[player.name].min(),
            "Average Elo": processing_df[processing_df['diff'] != 0][player.name].mean(),
            "Best Points Change": processing_df["diff"].max(),
            "Worst Points Change": processing_df["diff"].min(),
            "Total Points Lost": processing_df[processing_df["diff"] < 0]["diff"].sum(),
            "Total Points Gained": processing_df[processing_df["diff"] > 0]["diff"].sum(),
            "No. Games w Elo Gain": processing_df[processing_df["diff"] > 0]["diff"].shape[0],
            "No. Games w Elo Loss": processing_df[processing_df["diff"] < 0]["diff"].shape[0],
            "Standard Deviation": processing_df[processing_df["diff"] != 0][player.name].std(),
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
    for player in players:
        target_column = df[player.name]
        unique_values = target_column.drop_duplicates().reset_index(drop=True)
        unique_values_df = pd.DataFrame(unique_values)
        gradient, y_intercept = linear_regression_calc(unique_values_df, player.name)
        last_10_rows_df = unique_values_df.tail(10).copy()
        gradient_last_ten, _ = linear_regression_calc(last_10_rows_df, player.name)
        output[player.name] = {"Improvement (Overall)": round(gradient, 2), "Estimated Starting Elo": round(y_intercept, 2), "Improvement (Last 10 Games)": round(gradient_last_ten, 2)}

    return output


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
    scores_df = pd.DataFrame(df_data)
    output_data['player_stats'] = generate_player_stats(scores_df=scores_df)
    output_data['interaction_matrix'] = generate_interaction_matrix()
    with open('master_data.json', 'w') as file:
        json.dump(output_data, file, indent=4)