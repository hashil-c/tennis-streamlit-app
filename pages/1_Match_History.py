import json

import streamlit as st
import pandas as pd

from data import games

with open('master_data.json', 'r') as file:
    data = json.load(file)


def get_match_data():
    """Return the data for the table."""
    df = pd.DataFrame(data['games'])
    df = df.rename(
        columns={
            'date': 'Date',
            'team_1': 'Team 1',
            'team_2': 'Team 2',
            'team_1_score': 'Team 1 Score',
            'team_2_score': 'Team 2 Score',
            'team_1_exp_score_pct': 'Team 1 Exp Score %',
            'team_2_exp_score_pct': 'Team 2 Exp Score %',
            'team_1_elo': 'Team 1 Elo',
            'team_2_elo': 'Team 2 Elo',
            'team_1_score_pct': 'Team 1 Score %',
            'team_2_score_pct': 'Team 2 Score %',
            'elo_change': "Elo Change"
        })
    df = df[['Date', 'Team 1', 'Team 1 Score', 'Team 2 Score', 'Team 2', 'Team 1 Exp Score %', 'Team 2 Exp Score %',
             'Team 1 Elo', 'Team 2 Elo', 'Team 1 Score %', 'Team 2 Score %', 'Elo Change']]
    df['Game No.'] = range(1, len(df) + 1)
    df = df.set_index('Game No.')
    df = df.sort_index(ascending=False)
    return df


st.header("Matches")

df = pd.DataFrame(data['games'])
st.dataframe(get_match_data(), use_container_width=True)
