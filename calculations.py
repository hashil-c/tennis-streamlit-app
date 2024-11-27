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


def calculate_elo_change(completeness, game_type_scaling, team_capture_percent, team_expected_score):
    return Constants.k_factor * completeness * game_type_scaling * (team_capture_percent - team_expected_score)


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
        completeness = 0.5 ** (max(Constants.full_match - total_points, 0))

        team_1_capture_percentage = game.team_1_score / total_points
        team_2_capture_percentage = game.team_2_score / total_points

        team_1_elo_change = calculate_elo_change(completeness, game_type_scaling, team_1_capture_percentage,
                                                 team_1_expected_score)
        team_1_per_player_change = team_1_elo_change / team_1_player_count
        for player in team_1_players:
            player.update_score(round(team_1_per_player_change, 2))

        team_2_elo_change = calculate_elo_change(completeness, game_type_scaling, team_2_capture_percentage,
                                                 team_2_expected_score)
        team_2_per_player_change = team_2_elo_change / team_2_player_count
        for player in team_2_players:
            player.update_score(round(team_2_per_player_change, 2))

        temp_output = {}
        temp_output["Game"] = count
        for player in Players.players:
            temp_output[player.name] = round(player.score, 2)
        output.append(temp_output)
    return output

