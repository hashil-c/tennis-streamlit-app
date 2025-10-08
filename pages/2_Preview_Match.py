import json
from copy import deepcopy
from datetime import datetime
import pandas as pd

import streamlit as st
from Current_Rankings import get_players
from calculator import TableEntry
from calculator import Game
import data
from calculator import Calculator

if 'req_num_games' not in st.session_state:
    st.session_state.req_num_games = 0

with open('master_data.json', 'r') as file:
    master_data = json.load(file)

def get_updated_table(team_1, team_2, team_1_score, team_2_score):
    """Get new table with changes."""
    process_matches = deepcopy(st.session_state.matches)
    games = []
    conditions = [
        len(team_1) != 0,
        len(team_2) != 0,
        team_1_score != 0 or team_2_score != 0
    ]
    if all(conditions):
        process_matches.append({
            'team_1': team_1,
            'team_2': team_2,
            'team_1_score': team_1_score,
            'team_2_score': team_2_score
        })
    for match in process_matches:
        team_1 = [getattr(data, player) for player in match['team_1']]
        team_2 = [getattr(data, player) for player in match['team_2']]
        games.append(
            Game(date=datetime.now(), team_1=team_1, team_2=team_2, team_1_score=match['team_1_score'], team_2_score=match['team_2_score'])
        )

    last_entry = master_data['table'][-1]
    player_dict = {getattr(data, player): score for player, score in last_entry.items() if not player.islower()}
    current_scores = TableEntry(game=None, player_dict=player_dict)
    calculator = Calculator(starting_entry=current_scores)
    table_entries, match_data = calculator.process_game(games=games)
    st.session_state.req_num_games = match_data[-1]['required_games']
    latest_table = table_entries[-1].__dict__
    player_data = {player_name: data['score'] for player_name, data in latest_table.items() if not player_name.islower()}
    df = pd.DataFrame(player_data.items(), columns=['Player', 'Current Elo'])
    df['Starting Elo'] = df['Player'].map(last_entry)
    df['Elo Change'] = df['Current Elo'] - df['Starting Elo']

    # Sort by Score in descending order
    df = df.sort_values(by='Current Elo', ascending=False)

    # Add the Rank column
    df['Position'] = range(1, len(df) + 1)

    # Reorder columns
    df = df[['Position', 'Player', 'Current Elo', 'Elo Change']]
    df = df.set_index('Position', drop=True)
    return df


# Initialize a session state to store the matches and their results
if 'matches' not in st.session_state:
    st.session_state.matches = []

# Header and instructions
st.header("Preview Match")
st.write("Simulate multiple matches and see the cumulative impact on rankings below.")

# Match input columns
st_col1, st_col2 = st.columns(2)
team_1 = st_col1.multiselect(label="Team 1", options=get_players(active_only=False), max_selections=3)
team_2 = st_col2.multiselect(label="Team 2", options=get_players(active_only=False), max_selections=3)
team_1_score = st_col1.number_input(label="Team 1 Score", min_value=0, max_value=25)
team_2_score = st_col2.number_input(label="Team 2 Score", min_value=0, max_value=25)

state = False
# Check if teams are valid and prevent player duplication
if len(team_1) == 0 or len(team_2) == 0:
    st.write("Select players for Team 1 and 2 to continue")
elif set(team_1) & set(team_2):
    st.write("A player cannot be in both teams")
elif team_1_score == 0 and team_2_score == 0:
    st.write("Both Scores cannot be 0")
else:
    state = True
    add_match = st.button("Store Match")
    st.write(f"Required Games: {st.session_state.req_num_games}")
    if add_match:
        st.session_state.matches.append({
            'team_1': team_1,
            'team_2': team_2,
            'team_1_score': team_1_score,
            'team_2_score': team_2_score
        })
        team_1 = []
        team_2 = []
        team_2_score = 0
        team_1_score = 0
        st.rerun()
st.divider()

# Show the list of matches
if st.session_state.matches or state == True:
    st.write("Stored Matches:")
    for match in st.session_state.matches:
        team_1_names = ', '.join(match['team_1'])
        team_2_names = ', '.join(match['team_2'])
        match_string = f'{team_1_names} {match["team_1_score"]} - {match["team_2_score"]} {team_2_names}'
        st.write(match_string)
    clear_matches = st.button('Clear Matches')
    if clear_matches:
        st.session_state.matches = []
        st.rerun()
    st.divider()
    st.table(data=get_updated_table(team_1=team_1, team_2=team_2, team_1_score=team_1_score, team_2_score=team_2_score))

