import streamlit as st

from constants import Constants
from data import Players
from Current_Rankings import process

st.header("Expected Scores")

players = []
for player in Players.players:
    players.append(player.name)

st_col1, st_col2 = st.columns(2)
team_1 = st_col1.multiselect(label="Team 1", options=players, max_selections=3)
team_2 = st_col2.multiselect(label="Team 2", options=players, max_selections=3)


def calculate_latest_expected_score(team_1_players, team_2_players):
    df = process()
    last_row = df.iloc[-1]

    team_1_average_elo = sum([last_row[player] for player in team_1_players]) / len(team_1_players)
    team_2_average_elo = sum([last_row[player] for player in team_2_players]) / len(team_2_players)

    team_1_expected_score = 1 / (1 + 10 ** ((team_2_average_elo - team_1_average_elo) / Constants.r_factor))
    team_2_expected_score = 1 / (1 + 10 ** ((team_1_average_elo - team_2_average_elo) / Constants.r_factor))

    return {
        'team_1_expected_score': team_1_expected_score,
        'team_2_expected_score': team_2_expected_score
    }


if len(team_1) > 0 and len(team_2) > 0:
    team1_set = set(team_1)
    team2_set = set(team_2)
    if len(team1_set.intersection(team2_set)) > 0:
        st.write("A player cannot be on both teams")
    else:
        data = calculate_latest_expected_score(team_1, team_2)
        st_col1.metric("T1 win points %", round(data['team_1_expected_score'], 2))
        st_col2.metric("T2 win points %", round(data['team_2_expected_score'], 2))