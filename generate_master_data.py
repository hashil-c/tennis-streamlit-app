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
        processing_df = scores_df[['game_number', 'date', player.name]]
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
    output_data['games'] = game_data
    scores_df = pd.DataFrame(df_data)
    output_data['player_stats'] = generate_player_stats(scores_df=scores_df)
    with open('master_data.json', 'w') as file:
        json.dump(output_data, file, indent=4)