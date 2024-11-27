class GameType:
    NOR = "normal"
    HP = "half_points"


class Game:
    def __init__(self, date, team_1, team_1_score, team_2_score, team_2, type=GameType.NOR):
        self.date = date
        self.team_1 = team_1
        self.team_2 = team_2
        self.team_1_score = team_1_score
        self.team_2_score = team_2_score
        self.type = type


class Player:
    def __init__(self, name, score=1000, track=False):
        self.name = name
        self.score = score
        self.track = track

    def update_score(self, points):
        self.score = self.score + points
        if self.track:
            print(f"Player: {self.name}, Change: {points}, Total: {self.score}")
