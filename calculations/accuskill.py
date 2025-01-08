import math
import statistics

from classes import Game
from data import games

RFactor = 400
KFactor = 300


class Player:

    def __init__(self, name):
        self.name = name
        self.scores = [1000]

    def get_mean_score(self):
        return sum(self.scores) / len(self.scores)

    def get_reported_score(self):
        mean = statistics.mean(self.scores)
        try:
            std_dev = statistics.stdev(self.scores)
        except Exception as e:
            std_dev = 0
        return mean - std_dev

    def add_score(self, score):
        """Add score to score collection"""
        self.scores.append(score)


class Players:
    DEE = Player("DEE")
    SAH = Player("SAH")
    HAS = Player("HAS")
    ANJ = Player("ANJ")
    ASH = Player("ASH")
    JIM = Player("JIM")
    EST = Player("EST")
    MIS = Player("MIS")
    BHA = Player("BHA")
    SON = Player("SON")
    DIV = Player("DIV")

    players = [DEE, SAH, HAS, ANJ, ASH, JIM, EST, MIS, BHA, SON, DIV]


def get_players(players):
    output = []
    for player_code in players:
        player = getattr(Players, player_code, None)
        if player is None:
            raise Exception(f"Player {player_code} not found")
        output.append(player)
    return output


def process_games():
    """Process games using the Accuskill method"""
    output = []
    for count, game in enumerate(games):
        team_1 = get_players(players=game.team_1)
        team_2 = get_players(players=game.team_2)

        team_1_elos = [player.get_mean_score() for player in team_1]
        team_2_elos = [player.get_mean_score() for player in team_2]

        team_1_average_elo = sum(team_1_elos) / len(team_1_elos)
        team_2_average_elo = sum(team_2_elos) / len(team_2_elos)

        team_1_expected_score = 1 / (1 + 10 ** ((team_2_average_elo - team_1_average_elo) / RFactor))
        team_2_expected_score = 1 / (1 + 10 ** ((team_1_average_elo - team_2_average_elo) / RFactor))

        team_1_actual_score = game.team_1_score / (game.team_1_score + game.team_2_score)
        team_2_actual_score = game.team_2_score / (game.team_1_score + game.team_2_score)

        ratio = max(team_1_actual_score, 0.5) / max(team_2_actual_score, 0.5)

        diff = math.log(ratio, 10) * RFactor

        if team_1_actual_score > team_2_actual_score:
            diff = abs(diff)
        else:
            diff = -abs(diff)
        points_change = diff / 2

        team_1_per_player_points_change = points_change / len(team_1)
        team_2_per_player_points_change = points_change / len(team_2)

        for player in team_1:
            player.add_score(player.get_mean_score() + team_1_per_player_points_change)
        for player in team_2:
            player.add_score(player.get_mean_score() - team_2_per_player_points_change)
        game_line = {"game": count}
        for player in Players.players:
            game_line[f"{player.name}_reported"] = player.get_reported_score()
            game_line[f"{player.name}_real"] = player.get_mean_score()
        output.append(game_line)
    return output
