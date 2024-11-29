import streamlit as st

from data import Players
from Current_Rankings import process

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
        "Average Elo": selected_df[selected_player].mean(),
        "Best Points Change": selected_df[f"{selected_player}_Diff"].max(),
        "Worst Points Change": selected_df[f"{selected_player}_Diff"].min(),
        "Total Points Lost": selected_df[selected_df[f"{selected_player}_Diff"] < 0][f"{selected_player}_Diff"].sum(),
        "Total Points Gained": selected_df[selected_df[f"{selected_player}_Diff"] > 0][f"{selected_player}_Diff"].sum(),
    }
    col_1, col_2 = st.columns(2)
    for count, item in enumerate(data.keys()):
        if count % 2 == 0:
            col_2.metric(label=item, value=round(data[item], 2))
        else:
            col_1.metric(label=item, value=round(data[item], 2))