from copy import deepcopy

from calculations import calculate_elo
import pandas as pd
import streamlit as st

from data import Players, games


@st.cache_data
def process():
    data = calculate_elo()
    df = pd.DataFrame(data)
    for person in df.columns[1:]:  # Skip the 'Game' column
        df[f'{person}_Diff'] = df[person].diff()
    return df


def get_ranking(df):
    last_game = df.iloc[-1]
    people_cols = []
    for column in df.columns.tolist():
        if "Game" not in column and "Diff" not in column:
            people_cols.append(column)
    people_data = [
        (person, last_game[person], last_game[f"{person}_Diff"])
        for person in people_cols
    ]

    # Sort by weight in descending order
    ranked_people = sorted(people_data, key=lambda x: x[1], reverse=True)

    ranked_df = pd.DataFrame(ranked_people)
    ranked_df["Ranking"] = ranked_df.index + 1
    ranked_df.set_index("Ranking", drop=True)
    ranked_df = ranked_df.rename(columns={0: 'Player', 1: 'Current Elo', 2: 'Latest Change'})
    return ranked_df


st.title("Thursday Tennis League")
st.write(f"Last Game: {len(games)} on {games[-1].date.strftime('%d %B %Y')}")
st.header("Current Ranking:")

df = process()
writing = get_ranking(df=df)
st.dataframe(writing, hide_index=True, use_container_width=True, column_order=["Ranking", "Player", "Current Elo", "Latest Change"])

st.header("Trend")
people_cols = []
for column in df.columns.tolist():
    if "Game" not in column and "Diff" not in column:
        people_cols.append(column)
line_df = deepcopy(df)
data = st.multiselect("Choose Players (All by default)", people_cols)
if len(data) > 0:
    cols = data
else:
    cols = people_cols
line_df["Game"] = line_df["Game"] + 1
line_df.set_index("Game", drop=True)
st.line_chart(df[cols])

