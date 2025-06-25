import streamlit as st
import json
import pandas as pd

from data import players


with open('master_data.json', 'r') as file:
    data = json.load(file)


def get_players(active_only=False):
    """Return all the active players"""
    output = []
    for player in players:
        if active_only:
            if player.active:
                output.append(player.name)
        else:
            output.append(player.name)
    return output


def get_player_stats(selected_player):
    """Return the stats for the selected player"""
    return data['player_stats'][selected_player]


def get_interaction_matrix(selected_player):
    """Return the interaction matrix for the selected player"""
    raw_data = data['interaction_matrix'][selected_player]
    df = pd.DataFrame(raw_data)
    return df.T


selected_player = st.multiselect(label="Player", options=get_players(active_only=False), max_selections=1)
if selected_player:
    selected_player = selected_player[0]
    stats = get_player_stats(selected_player=selected_player)
    col_1, col_2 = st.columns(2)
    for count, item in enumerate(stats.keys()):
        if count % 2 == 0:
            col_2.metric(label=item, value=round(stats[item], 2))
        else:
            col_1.metric(label=item, value=round(stats[item], 2))

    st.write("Interaction Table:")
    st.table(get_interaction_matrix(selected_player))
