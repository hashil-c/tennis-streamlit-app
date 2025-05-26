from datetime import datetime

from classes import GameType
from constants import Constants
from data import Players, games


def get_players(players):
    output = []
    for player_code in players:
        player = getattr(Players, player_code, None)
        if player is None:
            raise Exception(f"Player {player_code} not found")
        output.append(player)
    return output


def calculate_elo_change(completeness, game_type_scaling, team_score, opponent_score, team_expected_score):
    team_capture_percent = team_score / (team_score + opponent_score)
    k_factor = Constants.k_factor_base
    if team_score >= 6 or opponent_score >= 6:
        k_factor = Constants.k_factor_full_set
    return k_factor * completeness * game_type_scaling * (team_capture_percent - team_expected_score)


def calculate_expected_score(team_1, team_2):
    team_1_players = get_players(team_1)
    team_1_player_count = len(team_1_players)
    team_2_players = get_players(team_2)
    team_2_player_count = len(team_2_players)


    team_1_average_elo = sum([player.score for player in team_1_players]) / len(team_1_players)
    team_2_average_elo = sum([player.score for player in team_2_players]) / len(team_2_players)

    team_1_expected_score = 1 / (1 + 10 ** ((team_2_average_elo - team_1_average_elo) / Constants.r_factor))
    team_2_expected_score = 1 / (1 + 10 ** ((team_1_average_elo - team_2_average_elo) / Constants.r_factor))

    return {
        "team_1_expected_score": team_1_expected_score,
        "team_2_expected_score": team_2_expected_score,
        "team_1_player_count": team_1_player_count,
        "team_2_player_count": team_2_player_count,
        "team_1_players": team_1_players,
        "team_2_players": team_2_players,
    }


def calculate_elo():
    for player in Players.players:
        player.score = 1000
    output = []
    for count, game in enumerate(games):
        game_type_scaling = 1
        if game.type == GameType.HP:
            game_type_scaling = 0.5

        expected_dict = calculate_expected_score(game.team_1, game.team_2)
        team_1_expected_score = expected_dict["team_1_expected_score"]
        team_2_expected_score = expected_dict["team_2_expected_score"]
        team_1_player_count = expected_dict["team_1_player_count"]
        team_2_player_count = expected_dict["team_2_player_count"]
        team_1_players = expected_dict["team_1_players"]
        team_2_players = expected_dict["team_2_players"]

        total_points = game.team_1_score + game.team_2_score
        if game.type in [GameType.NOR, GameType.HP]:
            completeness = 0.5 ** (max(Constants.normal_game_full_match - total_points, 0))
        elif game.type == GameType.CHA_F:
            completeness = 1
        elif game.type == GameType.CHA_H:
            completeness = 0.5
        elif game.type == GameType.CHA_Q:
            completeness = 0.125

        if team_1_player_count != team_2_player_count:
            completeness = completeness * 0.5

        team_1_elo_change = calculate_elo_change(completeness, game_type_scaling, game.team_1_score, game.team_2_score,
                                                 team_1_expected_score)
        team_1_per_player_change = team_1_elo_change / team_1_player_count
        for player in team_1_players:
            player.update_score(round(team_1_per_player_change, 2))

        team_2_elo_change = calculate_elo_change(completeness, game_type_scaling, game.team_2_score, game.team_1_score,
                                                 team_2_expected_score)
        team_2_per_player_change = team_2_elo_change / team_2_player_count
        for player in team_2_players:
            player.update_score(round(team_2_per_player_change, 2))

        temp_output = {"Game": count}
        for player in Players.players:
            temp_output[player.name] = round(player.score, 2)
        output.append(temp_output)
    return output

