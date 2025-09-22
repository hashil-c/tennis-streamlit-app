from copy import deepcopy
from constants import Constants
import math

class TableEntry:

    def __init__(self, game, player_dict):
        self.game = game
        for player, score in player_dict.items():
            setattr(self, player.name, {'player': player, 'score': score})


class Player:
    def __init__(self, name, score=1000, track=False, active=True):
        self.name = name
        self.score = score
        self.track = track
        self.active = active

    def update_score(self, points):
        self.score = self.score + points
        if self.track:
            print(f"Player: {self.name}, Change: {points}, Total: {self.score}")

    def __str__(self):
        return self.name


class GameType:
    NOR = "normal"
    HP = "half_points"
    CHA_F = "challenge_full"
    CHA_H = "challenge_half"
    CHA_Q = "challenge_less_than half"


class Game:
    def __init__(self, date, team_1, team_1_score, team_2_score, team_2, type=GameType.NOR):
        self.date = date
        self.team_1 = team_1
        self.team_2 = team_2
        self.team_1_score = team_1_score
        self.team_2_score = team_2_score
        self.type = type


class Calculator:

    def __init__(self, starting_entry):
        self.starting_entry = starting_entry

    def process_game(self, games):
        """Process a game or list of games"""
        table_entries = [self.starting_entry]
        game_data = []
        for game in games:
            last_entry = table_entries[-1]
            exp_score_dict = self.calculate_expected_score(team_1=game.team_1, team_2=game.team_2, entry=last_entry)

            # Isolate matches with too few games played
            single_game_score = 1/(game.team_1_score + game.team_2_score)
            min_expected_score = min(exp_score_dict['team_1_expected_score'], exp_score_dict['team_2_expected_score'])
            if min_expected_score != 0.5:
                required_games = math.ceil(1/min_expected_score)
                lower_ranked_player = 'team_1' if min_expected_score == exp_score_dict['team_1_expected_score'] else 'team_2'
                higher_ranked_player = 'team_1' if lower_ranked_player == 'team_2' else 'team_2'
                lower_ranked_player_score = getattr(game, f"{lower_ranked_player}_score")
                higher_ranked_player_score = getattr(game, f"{higher_ranked_player}_score")
                lower_capture_percent = lower_ranked_player_score/(lower_ranked_player_score + higher_ranked_player_score)
                if min_expected_score < single_game_score and lower_capture_percent < min_expected_score:
                    completeness = 0
            else:
                completeness = 1
                required_games = 1


            updates = self.calculate_new_elo(expected_dict=exp_score_dict, game=game, no_games_completeness=completeness)
            new_entry = deepcopy(last_entry)
            new_entry.game = game
            for player, change in updates.items():
                player_details = getattr(new_entry, player.name)
                new_score = player_details['score'] + change
                new_details = {'player': player_details['player'], 'score': new_score}
                setattr(new_entry, player.name, new_details)
            table_entries.append(new_entry)
            match_data = {
                'date': game.date.strftime("%Y-%m-%d"),
                'team_1': [player.name for player in game.team_1],
                'team_2': [player.name for player in game.team_2],
                'team_1_score': game.team_1_score,
                'team_2_score': game.team_2_score,
                'team_1_exp_score_pct': round(exp_score_dict['team_1_expected_score'] * 100, 2),
                'team_2_exp_score_pct': round(exp_score_dict['team_2_expected_score'] * 100, 2),
                'team_1_elo': exp_score_dict['team_1_combined_elo'],
                'team_2_elo': exp_score_dict['team_2_combined_elo'],
                'team_1_score_pct': round(game.team_1_score / (game.team_1_score + game.team_2_score) * 100, 2),
                'team_2_score_pct': round(game.team_2_score / (game.team_1_score + game.team_2_score) * 100, 2),
                'elo_change': abs(list(updates.values())[0]),
                'required_games': required_games
            }
            game_data.append(match_data)
        return table_entries, game_data


    def calculate_expected_score(self, team_1, team_2, entry):
        team_1_player_count = len(team_1)
        team_2_player_count = len(team_2)

        team_1_average_elo = sum([getattr(entry, player.name)['score'] for player in team_1]) / team_1_player_count
        team_2_average_elo = sum([getattr(entry, player.name)['score'] for player in team_2]) / team_2_player_count

        team_1_expected_score = 1 / (1 + 10 ** ((team_2_average_elo - team_1_average_elo) / Constants.r_factor))
        team_2_expected_score = 1 / (1 + 10 ** ((team_1_average_elo - team_2_average_elo) / Constants.r_factor))

        return {
            "team_1_expected_score": team_1_expected_score,
            "team_2_expected_score": team_2_expected_score,
            "team_1_player_count": team_1_player_count,
            "team_2_player_count": team_2_player_count,
            "team_1_combined_elo": team_1_average_elo,
            "team_2_combined_elo": team_2_average_elo,
        }

    def calculate_new_elo(self, expected_dict, game, no_games_completeness):
        game_type_scaling = 1
        if game.type == GameType.HP:
            game_type_scaling = 0.5

        team_1_expected_score = expected_dict["team_1_expected_score"]
        team_2_expected_score = expected_dict["team_2_expected_score"]
        team_1_player_count = expected_dict["team_1_player_count"]
        team_2_player_count = expected_dict["team_2_player_count"]

        total_points = game.team_1_score + game.team_2_score
        if game.type in [GameType.NOR, GameType.HP]:
            completeness = 0.5 ** (max(Constants.normal_game_full_match - total_points, 0))
        elif game.type == GameType.CHA_F:
            completeness = 1
        elif game.type == GameType.CHA_H:
            completeness = 0.5
        elif game.type == GameType.CHA_Q:
            completeness = 0.125

        completeness = no_games_completeness * completeness

        if team_1_player_count != team_2_player_count:
            completeness = completeness * 0.5

        team_1_elo_change = self.calculate_elo_change(
            completeness, game_type_scaling, game.team_1_score, game.team_2_score, team_1_expected_score
        )
        team_1_per_player_change = team_1_elo_change / team_1_player_count

        updates = {}
        for player in game.team_1:
            updates[player] = team_1_per_player_change

        team_2_elo_change = self.calculate_elo_change(
            completeness, game_type_scaling, game.team_2_score, game.team_1_score, team_2_expected_score
        )
        team_2_per_player_change = team_2_elo_change / team_2_player_count
        for player in game.team_2:
            updates[player] = team_2_per_player_change

        return updates

    def calculate_elo_change(self, completeness, game_type_scaling, team_score, opponent_score, team_expected_score):
        team_capture_percent = team_score / (team_score + opponent_score)
        k_factor = Constants.k_factor_base
        if team_score >= 6 or opponent_score >= 6:
            k_factor = Constants.k_factor_full_set
        return k_factor * completeness * game_type_scaling * (team_capture_percent - team_expected_score)
