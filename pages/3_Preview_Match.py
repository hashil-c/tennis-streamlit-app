import streamlit as st

from constants import Constants
from data import Players
from Current_Rankings import process
from calculations import calculate_elo_change
import pandas as pd

st.header("Preview Match")
st.write("Simulate a match. The impact on rankings will be displayed below.")

players = []
for player in Players.players:
    players.append(player.name)

st_col1, st_col2 = st.columns(2)
team_1 = st_col1.multiselect(label="Team 1", options=players, max_selections=3)
team_2 = st_col2.multiselect(label="Team 2", options=players, max_selections=3)
team_1_score = st_col1.number_input(label="Team 1 Score", min_value=0, max_value=25)
team_2_score = st_col2.number_input(label="Team 2 Score", min_value=0, max_value=25)


def get_change(df):
    """Get the change in elo after the simulated match."""
    last_row = dict(df.iloc[-1])

    new_dict = {}
    # Set Diff column to 0
    for key in last_row.keys():
        if "Diff" in key:
            new_dict[key] = 0
        else:
            new_dict[key] = last_row[key]

    team_1_average_elo = sum([last_row[player] for player in team_1]) / len(team_1)
    team_2_average_elo = sum([last_row[player] for player in team_2]) / len(team_2)

    team_1_capture_percent = team_1_score/(team_1_score + team_2_score)
    team_2_capture_percent = team_2_score / (team_1_score + team_2_score)

    completeness = 0.5 ** (max(Constants.full_match - (team_1_score + team_2_score), 0))

    if len(team_1) != len(team_2):
        completeness = completeness * 0.5

    team_1_expected_score = 1 / (1 + 10 ** ((team_2_average_elo - team_1_average_elo) / Constants.r_factor))
    team_2_expected_score = 1 / (1 + 10 ** ((team_1_average_elo - team_2_average_elo) / Constants.r_factor))

    team_1_elo_change = round(calculate_elo_change(completeness, 1, team_1_capture_percent, team_1_expected_score)/len(team_1), 2)
    team_2_elo_change = round(calculate_elo_change(completeness, 1, team_2_capture_percent, team_2_expected_score)/len(team_2), 2)

    for player in team_1:
        new_dict[player] = new_dict[player] + team_1_elo_change
        new_dict[f'{player}_Diff'] = team_1_elo_change
    for player in team_2:
        new_dict[player] = new_dict[player] + team_2_elo_change
        new_dict[f'{player}_Diff'] = team_2_elo_change

    people_cols = []
    for key in new_dict.keys():
        if "Game" not in key and "Diff" not in key:
            people_cols.append(key)
    people_data = [
        (person, new_dict[person], new_dict[f"{person}_Diff"])
        for person in people_cols
    ]

    # Sort by weight in descending order
    ranked_people = sorted(people_data, key=lambda x: x[1], reverse=True)

    ranked_df = pd.DataFrame(ranked_people)
    ranked_df["Ranking"] = ranked_df.index + 1
    ranked_df.set_index("Ranking", drop=True)
    ranked_df = ranked_df.rename(columns={0: 'Player', 1: 'Current Elo', 2: 'Latest Change'})

    data = {
        "Team 1 Average Elo": round(team_1_average_elo, 2),
        "Team 2 Average Elo": round(team_2_average_elo, 2),
        "Team 1 Expected Score": round(team_1_expected_score, 2),
        "Team 2 Expected Score": round(team_2_expected_score, 2),
        "Team 1 Capture Percent": round(team_1_capture_percent, 2),
        "Team_2 Capture Percent": round(team_2_capture_percent, 2)
    }

    return ranked_df, data


df = process()
if set(team_1) & set(team_2):
    st.write("A player cannot be in both teams")
else:
    output_conditions = [
        len(team_1) > 0,
        len(team_2) > 0,
        team_1_score != 0 or team_2_score != 0
    ]
    if all(output_conditions):
        output_df, data = get_change(df)
        st.dataframe(output_df, hide_index=True, use_container_width=True, column_order=["Ranking", "Player", "Current Elo", "Latest Change"])
        acol_1, acol_2 = st.columns(2)
        for count, key in enumerate(data.keys()):
            if count % 2 == 0:
                acol_2.metric(key, data[key])
            else:
                acol_1.metric(key, data[key])
