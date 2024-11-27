import streamlit as st
import pandas as pd

from data import games

st.header("All Games in this League")

df_data = []
for count, game in enumerate(reversed(games)):
    row = {
        "No.": len(games) - count - 1,
        "date": game.date.strftime('%d %B %Y'),
        "Team 1": ', '.join(game.team_1),
        "Team 1 Score": game.team_1_score,
        "Team 2 Score": game.team_2_score,
        "Team 2": ', '.join(game.team_2),
    }
    df_data.append(row)
df = pd.DataFrame(df_data)
st.table(df)
