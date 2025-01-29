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
    df_data = []
    for game in games:
        row = {
            "date": game.date,
            "Team 1": ', '.join(game.team_1),
            "Team 1 Score": game.team_1_score,
            "Team 2 Score": game.team_2_score,
            "Team 2": ', '.join(game.team_2),
        }
        df_data.append(row)
    game_df = pd.DataFrame(df_data)
    combined_df = df.join(game_df)
    last_day_df = combined_df[combined_df['date'] == combined_df['date'].max()]

    last_game = df.iloc[-1]
    people_cols = []
    for column in df.columns.tolist():
        if "Game" not in column and "Diff" not in column:
            people_cols.append(column)
    people_data = [
        (person, last_game[person], last_day_df[f"{person}_Diff"].sum())
        for person in people_cols
    ]

    # Sort by weight in descending order
    ranked_people = sorted(people_data, key=lambda x: x[1], reverse=True)

    ranked_df = pd.DataFrame(ranked_people)
    ranked_df["Ranking"] = ranked_df.index + 1
    ranked_df.set_index("Ranking", drop=True)
    ranked_df = ranked_df.rename(columns={0: 'Player', 1: 'Current Elo', 2: 'Last Session Change'})
    return ranked_df


st.title("Thursday Tennis League")
st.write(f"Last Game: {len(games)} on {games[-1].date.strftime('%d %B %Y')}")
st.header("Current Ranking:")

df = process()
writing = get_ranking(df=df)
st.dataframe(writing, hide_index=True, use_container_width=True, column_order=["Ranking", "Player", "Current Elo", "Last Session Change"])

st.header("Trend")
people_cols = []
for column in df.columns.tolist():
    if "Game" not in column and "Diff" not in column:
        people_cols.append(column)
line_df = deepcopy(df)

players = st.multiselect("Choose Players (All by default)", people_cols)
game_selector_col_1, game_selector_col_2 = st.columns(2)
start_game = game_selector_col_1.number_input("Start Game", 0, line_df.shape[0])
end_game = game_selector_col_2.number_input("End Game", 0, line_df.shape[0] - 1, line_df.shape[0] - 1)
if start_game < end_game:
    if len(players) > 0:
        cols = players
    else:
        cols = people_cols
    line_df["Game"] = line_df["Game"] + 1
    line_df.set_index("Game", drop=True)
    line_df = line_df.loc[start_game:end_game]
    st.line_chart(line_df[cols])

