import streamlit as st
import json
import pandas as pd

# (rest of your imports and data loading remain the same)
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


def get_player_trends(selected_player):
    """Return the trends for the selected player"""
    return data['trends'][selected_player]


def get_interaction_matrix(selected_player):
    """Return the interaction matrix for the selected player"""
    raw_data = data['interaction_matrix'][selected_player]
    df = pd.DataFrame(raw_data)
    return df.T

def get_win_chance(selected_player):
    """Return the win chance and rank for the selected player"""
    chance = data['average_expected_score'][selected_player]['expected_win_pct_last_10']
    rank = data['average_expected_score'][selected_player]['rank']
    return chance, rank


@st.dialog("Trend Analysis Explained")
def trend_analysis_explainer():
    st.markdown(
        "This feature uses basic linear regression to attempt to form trends from your data and game history. Here is what each item tells you:")

    st.markdown("**Improvement:**")
    st.markdown(
        """This is measured in Elo Points per Game an is a measure of your rate of improvement compared to the rest of the league. A positive value here indicates that your ability has improved quicker than the league average while a negative value here indicates you are improving slower than the league average. This is presented in two forms: Overall for looking at your all time improvement and Last 10 Matches to show your recent performance compared to your historic performance""")

    st.markdown("**Estimated Starting Elo:**")
    st.markdown(
        "This is measured in Elo Points and uses all your data to estimate your ability when you first joined the league")

@st.dialog("Challenge Explained")
def challenge_explainer():
    st.markdown("This is essentially a measure of match fairness. The closer a player's win change is to 100, the easier their recent games have been. Conversely, the closer a player's win chance is to 0, the more difficult their recent games have been. Players should aim to get this value close to 50")


selected_player = st.multiselect(label="Player", options=get_players(active_only=False), max_selections=1)
if selected_player:
    st.header("Performance Stats")
    selected_player = selected_player[0]
    stats = get_player_stats(selected_player=selected_player)
    trends = get_player_trends(selected_player=selected_player)
    col_1, col_2 = st.columns(2)
    for count, item in enumerate(stats.keys()):
        if count % 2 == 0:
            col_1.metric(label=item, value=round(stats[item], 2))
        else:
            col_2.metric(label=item, value=round(stats[item], 2))

    st.header("Interaction Table")
    st.table(get_interaction_matrix(selected_player))

    st.header("Trend Analysis")
    if st.button("Explain", key='explain_trend'):
        trend_analysis_explainer()
    col_11, col_12 = st.columns(2)
    non_ranking_keys = [key for key in trends.keys() if 'Rank' not in key]
    for count, item in enumerate(non_ranking_keys):
        if count % 2 == 0:
            col_11.metric(label=item, value=f"{round(trends[item], 2)} ({trends[item + ' Rank']})")
        else:
            col_12.metric(label=item, value=f"{round(trends[item], 2)} ({trends[item + ' Rank']})")


    st.header("Challenge")
    if st.button("Explain", key='explain_challenge'):
        challenge_explainer()
    win_chance, rank = get_win_chance(selected_player=selected_player)
    st.metric(label="Win Chance (Last 10)", value=f"{win_chance} ({rank})")