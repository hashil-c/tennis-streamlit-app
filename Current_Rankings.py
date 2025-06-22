import streamlit as st
import json
import pandas as pd

from data import players, games

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


def get_current_table_data(show_inactive):
    """Convert the data to the table format."""
    last_entry = data['table'][-1]
    player_data = {player: score for player, score in last_entry.items() if not player.islower()}
    active_players = {player: score for player, score in player_data.items() if player in get_players(active_only=not show_inactive)}
    df = pd.DataFrame(active_players.items(), columns=['Player', 'Current Elo'])

    # Sort by Score in descending order
    df = df.sort_values(by='Current Elo', ascending=False)

    # Add the Rank column
    df['Position'] = range(1, len(df) + 1)

    # Reorder columns
    df = df[['Position', 'Player', 'Current Elo']]
    df = df.set_index('Position', drop=True)
    return df


def get_chart_data(start_game, end_game, filter_players=[]):
    """Get the data required to draw the line chart"""
    df = pd.DataFrame(data=data['table'])
    df.set_index('game_number', drop=True)
    df = df.drop(columns=['date', 'game_number'])
    df = df.loc[start_game:end_game]
    if not filter_players:
        return df
    else:
        return df[filter_players]


st.title("Tennis League")
st.write(f"Last Game: {len(games)} on {games[-1].date.strftime('%d %B %Y')}")

show_inactive = st.toggle(label="Show inactive players")

st.header("Current Ranking:")
st.table(get_current_table_data(show_inactive=show_inactive))

st.header("Trend")
selected_players = st.multiselect("Choose Players (All by default)", get_players(active_only=not show_inactive))
game_selector_col_1, game_selector_col_2 = st.columns(2)
start_game = game_selector_col_1.number_input("Start Game", 0, len(data['table']))
end_game = game_selector_col_2.number_input("End Game", 0, len(data['table']) - 1, len(data['table']) - 1)
if start_game < end_game:
    st.line_chart(get_chart_data(start_game=start_game, end_game=end_game, filter_players=selected_players), use_container_width=True)

