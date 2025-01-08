from calculations import accuskill
import streamlit as st
import pandas as pd

result = accuskill.process_games()

st.table(result)

df = pd.Dataframe(result)
