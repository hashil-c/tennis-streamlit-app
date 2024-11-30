import streamlit as st

from constants import Constants
from data import Players
from Current_Rankings import process

st.header("Expected Scores")

st.write("How it works:")
st.write(
    """The expected scores displayed here represent the percentage of points players are 
    expected to capture in a game to maintain their elo. This percentage needs to be multiplied
    by the number of games going to be player to get the number of games that a player must win 
    to maintain their elo. Keep in mind that the player should always round up.""")
st.write("Example:")
st.write(
    """If Player A has a win points % of 59% and Player B has one of 41% and they plan to play 11 games, 
    Player A must capture 11 * 0.59 = 6.49 games to win. Since a fraction of a game is not possible, Player A
    must win at least 7 out of the 11 games to not drop any elo points""")

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
        'team_1_expected_score': team_1_expected_score * 100,
        'team_2_expected_score': team_2_expected_score * 100
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