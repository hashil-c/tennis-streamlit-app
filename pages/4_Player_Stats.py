import streamlit as st

from data import Players, games
from Current_Rankings import process
from collections import Counter
import pandas as pd


def get_player_matrix(player, players):
    teamups = []
    opponents = []
    for game in games:
        player_team = None
        opponent_team = None
        if player in game.team_1:
            player_team = "team_1"
            opponent_team = "team_2"
        elif player in game.team_2:
            player_team = "team_2"
            opponent_team = "team_1"
        if player_team is not None:
            team_mates = set(getattr(game, player_team)) - {player}
            teamups.extend(list(team_mates))
            opponents.extend(getattr(game, opponent_team))
    teamup_dict = dict(Counter(teamups))
    opponent_dict = dict(Counter(opponents))
    for pl in set(players) - {player}:
        if teamup_dict.get(pl, None) is None:
            teamup_dict[pl] = 0
        if opponent_dict.get(pl, None) is None:
            opponent_dict[pl] = 0
    df_data = {"Teammate": teamup_dict, "Opponent:": opponent_dict}
    return pd.DataFrame(df_data)


players = []
for player in Players.players:
    players.append(player.name)

selected_player = st.multiselect(label="Player", options=players, max_selections=1)
if selected_player:
    selected_player = selected_player[0]
    df = process()
    selected_player_cols = ["Game"]
    for col in df.columns:
        if selected_player in col:
            selected_player_cols.append(col)
    selected_df = df[selected_player_cols].fillna(0)
    data = {
        "Match Participation %": (selected_df[selected_df[f"{selected_player}_Diff"] != 0].shape[0])/selected_df.shape[0] * 100,
        "Highest Elo": selected_df[selected_player].max(),
        "Lowest Elo": selected_df[selected_player].min(),
        "Average Elo": selected_df[selected_df[f"{selected_player}_Diff"] != 0][selected_player].mean(),
        "Best Points Change": selected_df[f"{selected_player}_Diff"].max(),
        "Worst Points Change": selected_df[f"{selected_player}_Diff"].min(),
        "Total Points Lost": selected_df[selected_df[f"{selected_player}_Diff"] < 0][f"{selected_player}_Diff"].sum(),
        "Total Points Gained": selected_df[selected_df[f"{selected_player}_Diff"] > 0][f"{selected_player}_Diff"].sum(),
        "No. Games w Elo Gain": selected_df[selected_df[f"{selected_player}_Diff"] > 0].shape[0],
        "No. Games w Elo Loss": selected_df[selected_df[f"{selected_player}_Diff"] < 0].shape[0],
        "Standard Deviation": selected_df[selected_df[f"{selected_player}_Diff"] != 0][selected_player].std()
    }
    col_1, col_2 = st.columns(2)
    for count, item in enumerate(data.keys()):
        if count % 2 == 0:
            col_2.metric(label=item, value=round(data[item], 2))
        else:
            col_1.metric(label=item, value=round(data[item], 2))

    st.write("Interaction Table:")
    teamup_df = get_player_matrix(player=selected_player, players=players)
    st.dataframe(teamup_df, use_container_width=True)
