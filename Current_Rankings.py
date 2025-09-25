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

def format_numeric_display(x):
    if isinstance(x, (int, float)):
        return f'{x:g}'
    return x

def get_singles_doubles_leaderboard(mode, show_inactive):
    if mode == 'singles':
        entry_data = data['singles_latest_table'][0]
    if mode == 'doubles':
        entry_data = data['doubles_latest_table'][0]
    player_data = {player: score for player, score in entry_data.items() if not player.islower()}
    active_players = {player: score for player, score in player_data.items() if
                      player in get_players(active_only=not show_inactive)}
    df = pd.DataFrame(active_players.items(), columns=['Player', 'Current Elo'])

    # Sort by Score in descending order
    df = df.sort_values(by='Current Elo', ascending=False)

    # Add the Rank column
    df['Position'] = range(1, len(df) + 1)

    # Reorder columns
    df = df[['Position', 'Player', 'Current Elo']]
    df = df.set_index('Position', drop=True)
    df = df.round(2)
    for col in ['Current Elo',]:
        if col in df.columns:
            df[col] = df[col].apply(format_numeric_display)
    return df

def get_last_session_change():
    latest_entries = data['table'][-10:]
    change_df = pd.DataFrame(latest_entries)
    change_df['date'] = pd.to_datetime(change_df['date'])
    daily_closing_balances = change_df.groupby('date').last()

    unique_dates = daily_closing_balances.index.sort_values()

    if len(unique_dates) < 2:
        raise ValueError("Not enough unique dates to calculate a change in balance. Extend the lookback window")

    last_day = unique_dates[-1]
    second_to_last_day = unique_dates[-2]

    # 4. Get the balances for these two days
    balances_last_day = daily_closing_balances.loc[last_day]
    balances_second_to_last_day = daily_closing_balances.loc[second_to_last_day]

    # 5. Calculate the change in balance for each person
    #    Exclude 'transaction_id' from the calculation
    person_columns = [col for col in change_df.columns if not col.islower()]

    change_in_balance = balances_last_day[person_columns] - balances_second_to_last_day[person_columns]
    return change_in_balance.to_dict()


def get_current_table_data(show_inactive):
    """Convert the data to the table format."""
    latest_change = get_last_session_change()
    last_entry = data['table'][-1]
    player_data = {player: score for player, score in last_entry.items() if not player.islower()}
    active_players = {player: score for player, score in player_data.items() if player in get_players(active_only=not show_inactive)}
    df = pd.DataFrame(active_players.items(), columns=['Player', 'Current Elo'])
    df['Last Session Change'] = df['Player'].map(latest_change)

    # Sort by Score in descending order
    df = df.sort_values(by='Current Elo', ascending=False)

    # Add the Rank column
    df['Position'] = range(1, len(df) + 1)

    # Reorder columns
    df = df[['Position', 'Player', 'Current Elo', 'Last Session Change']]
    df = df.set_index('Position', drop=True)
    df = df.round(2)
    for col in ['Current Elo', 'Last Session Change']:
        if col in df.columns:
            df[col] = df[col].apply(format_numeric_display)
    return df


def get_chart_data(start_game, end_game, show_inactive, filter_players=[],):
    """Get the data required to draw the line chart"""
    df = pd.DataFrame(data=data['table'])
    df.set_index('game_number', drop=True)
    df = df.drop(columns=['date', 'game_number'])
    df = df.loc[start_game:end_game]
    df = df[get_players(active_only=not show_inactive)]
    if not filter_players:
        return df
    else:
        return df[filter_players]


st.title("Tennis League")
st.write(f"Last Game: {len(games)} on {games[-1].date.strftime('%d %B %Y')}")

show_inactive = st.toggle(label="Show inactive players")

st.header("Current Ranking:")

overall_tab, singles_tab, doubles_tab = st.tabs(["Overall", "Singles", "Doubles"])
with overall_tab:
    st.table(get_current_table_data(show_inactive=show_inactive))
with singles_tab:
    st.table(get_singles_doubles_leaderboard(mode='singles', show_inactive=show_inactive))
with doubles_tab:
    st.table(get_singles_doubles_leaderboard(mode='doubles', show_inactive=show_inactive))

st.header("Trend")
selected_players = st.multiselect("Choose Players (All by default)", get_players(active_only=not show_inactive))
game_selector_col_1, game_selector_col_2 = st.columns(2)
start_game = game_selector_col_1.number_input("Start Game", 0, len(data['table']))
end_game = game_selector_col_2.number_input("End Game", 0, len(data['table']) - 1, len(data['table']) - 1)
if start_game < end_game:
    st.line_chart(get_chart_data(start_game=start_game, end_game=end_game, filter_players=selected_players, show_inactive=show_inactive), use_container_width=True)

