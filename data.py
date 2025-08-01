import datetime

from calculator import Game, Player, GameType

DEE = Player("DEE")
SAH = Player("SAH")
HAS = Player("HAS")
ANJ = Player("ANJ")
ASH = Player("ASH")
JIM = Player("JIM", active=False)
EST = Player("EST")
HAN = Player("HAN")
MIS = Player("MIS")
BHA = Player("BHA")
SON = Player("SON", active=False)
DIV = Player("DIV")
DER = Player("DER")
AKS = Player("AKS")
HIT = Player("HIT")

players = [DEE, SAH, HAS, ANJ, ASH, JIM, EST, MIS, BHA, SON, DIV, DER, AKS, HIT, HAN]

games = [
    # Game(datetime.datetime(2024, 5, 16), [DEE], 1, 4, [HAS]),
    # Game(datetime.datetime(2024, 5, 16), [DEE], 4, 1, [HAS]),
    Game(datetime.datetime(2024, 5, 16), [DEE], 9, 8, [HAS]),
    Game(datetime.datetime(2024, 6, 17), [SAH], 6, 4, [HAS]),
    Game(datetime.datetime(2024, 6, 20), [HAS, ANJ], 3, 6, [ASH, JIM]),
    Game(datetime.datetime(2024, 6, 20), [MIS, ANJ], 6, 4, [SAH, DEE]),
    Game(datetime.datetime(2024, 7, 18), [SAH, ANJ], 6, 4, [HAS, DEE, BHA]),
    Game(datetime.datetime(2024, 7, 18), [SAH, ANJ, DEE], 4, 1, [HAS, BHA]),
    Game(datetime.datetime(2024, 7, 23), [SAH], 12, 1, [HAS]),
    Game(datetime.datetime(2024, 7, 25), [SAH, HAS], 3, 6, [MIS, DEE]),
    Game(datetime.datetime(2024, 7, 25), [SAH], 0, 4, [MIS]),
    Game(datetime.datetime(2024, 7, 25), [ANJ, HAS], 3, 3, [BHA, ASH]),
    # Game(datetime.datetime(2024, 7, 30), [SAH], 6, 3, [HAS]),
    # Game(datetime.datetime(2024, 7, 30), [SAH], 1, 2, [HAS]),
    Game(datetime.datetime(2024, 7, 30), [SAH], 7, 5, [HAS]),
    Game(datetime.datetime(2024, 8, 4), [SAH, BHA], 6, 2, [HAS, ANJ]),
    Game(datetime.datetime(2024, 8, 4), [SAH, ANJ], 0, 1, [HAS]),
    Game(datetime.datetime(2024, 8, 7), [SAH, DEE], 3, 0, [HAS, ANJ]),
    Game(datetime.datetime(2024, 8, 7), [SAH, ANJ], 3, 2, [HAS, DEE]),
    Game(datetime.datetime(2024, 8, 7), [SAH, HAS], 2, 0, [ANJ, DEE]),
    # Game(datetime.datetime(2024, 8, 15), [HAS], 6, 1, [BHA], type=GameType.HP),
    # Game(datetime.datetime(2024, 8, 15), [HAS], 2, 1, [BHA], type=GameType.HP),
    Game(datetime.datetime(2024, 8, 15), [HAS], 8, 2, [BHA], type=GameType.HP),
    Game(datetime.datetime(2024, 8, 22), [HAS, ASH], 4, 1, [DEE, ANJ]),
    Game(datetime.datetime(2024, 8, 22), [HAS, ANJ], 3, 1, [DEE, ASH]),
    Game(datetime.datetime(2024, 8, 29), [SAH], 5, 5, [HAS]),
    Game(datetime.datetime(2024, 8, 29), [ANJ], 1, 10, [DEE]),
    Game(datetime.datetime(2024, 9, 5), [MIS, HAS], 2, 2, [SAH, DEE]),
    Game(datetime.datetime(2024, 9, 5), [ANJ, MIS], 1, 3, [BHA, SAH]),
    Game(datetime.datetime(2024, 9, 5), [ANJ, HAS], 2, 2, [BHA, DEE]),
    Game(datetime.datetime(2024, 9, 5), [SAH, HAS], 3, 1, [MIS, DEE]),
    Game(datetime.datetime(2024, 9, 7), [HAS], 3, 1, [JIM]),
    Game(datetime.datetime(2024, 9, 7), [JIM], 4, 0, [EST]),
    Game(datetime.datetime(2024, 9, 7), [HAS], 3, 1, [EST]),
    Game(datetime.datetime(2024, 9, 19), [HAS], 3, 2, [JIM]),
    Game(datetime.datetime(2024, 9, 19), [ASH], 1, 3, [JIM]),
    Game(datetime.datetime(2024, 9, 19), [ASH], 0, 4, [HAS]),
    Game(datetime.datetime(2024, 9, 26), [ASH], 3, 2, [HAS]),
    Game(datetime.datetime(2024, 9, 27), [SAH], 6, 4, [HAS]),
    Game(datetime.datetime(2024, 10, 3), [SAH, DEE], 4, 6, [MIS]),
    Game(datetime.datetime(2024, 10, 17), [SAH, HAS], 1, 2, [MIS, ASH]),
    Game(datetime.datetime(2024, 10, 17), [SAH, ANJ], 0, 3, [MIS, HAS]),
    Game(datetime.datetime(2024, 10, 17), [ANJ, ASH], 0, 4, [MIS, HAS]),
    Game(datetime.datetime(2024, 10, 17), [ANJ, ASH], 0, 2, [MIS, SAH], type=GameType.HP),
    # Game(datetime.datetime(2024, 10, 18), [HAS], 2, 6, [SAH]),
    # Game(datetime.datetime(2024, 10, 18), [HAS], 2, 0, [SAH]),
    Game(datetime.datetime(2024, 10, 18), [HAS], 4, 6, [SAH]),
    Game(datetime.datetime(2024, 10, 24), [HAS, ANJ], 3, 6, [SAH, BHA]),
    Game(datetime.datetime(2024, 10, 24), [HAS, BHA], 3, 1, [SAH, ANJ]),
    Game(datetime.datetime(2024, 10, 29), [HAS, EST], 3, 6, [SAH, JIM]),
    Game(datetime.datetime(2024, 10, 29), [HAS, SAH], 4, 0, [JIM, EST]),
    Game(datetime.datetime(2024, 11, 6), [HAS], 3, 4, [SAH]),
    Game(datetime.datetime(2024, 11, 14), [HAS, ANJ], 0, 10, [SAH, MIS]),
    Game(datetime.datetime(2024, 11, 28), [HAS, SAH], 3, 2, [MIS, BHA]),
    Game(datetime.datetime(2024, 11, 28), [HAS, MIS], 3, 1, [SAH, DEE]),
    Game(datetime.datetime(2024, 11, 28), [DEE, SAH], 1, 3, [MIS, BHA]),
    Game(datetime.datetime(2024, 12, 5), [BHA], 4, 3, [HAS]),
    Game(datetime.datetime(2024, 12, 7), [ASH], 3, 3, [HAS]),
    # Game(datetime.datetime(2024, 12, 9), [ANJ], 2, 6, [SAH]),
    # Game(datetime.datetime(2024, 12, 9), [ANJ], 0, 4, [SAH]),
    Game(datetime.datetime(2024, 12, 9), [ANJ], 2, 10, [SAH]),
    Game(datetime.datetime(2024, 12, 12), [SAH], 6, 2, [DEE]),
    Game(datetime.datetime(2024, 12, 19), [SAH], 4, 0, [HAS, ANJ]),
    Game(datetime.datetime(2024, 12, 23), [HAS], 1, 1, [BHA]),
    Game(datetime.datetime(2024, 12, 23), [HAS, ANJ], 1, 3, [BHA, SAH]),
    Game(datetime.datetime(2024, 12, 23), [HAS, SAH], 4, 0, [BHA, ANJ]),
    Game(datetime.datetime(2024, 12, 23), [HAS, BHA], 4, 0, [SAH, ANJ]),
    Game(datetime.datetime(2024, 12, 27), [SAH, HAS], 3, 1, [ASH, DIV]),
    Game(datetime.datetime(2024, 12, 27), [SAH, HAS], 2, 2, [MIS, SON]),
    Game(datetime.datetime(2024, 12, 27), [ASH, DIV], 0, 4, [MIS, SON]),
    Game(datetime.datetime(2024, 12, 27), [SON, SAH], 1, 3, [MIS, HAS]),
    Game(datetime.datetime(2025, 1, 2), [SAH], 4, 4, [HAS]),
    Game(datetime.datetime(2025, 1, 8), [SAH, BHA], 4, 0, [HAS, ANJ]),
    Game(datetime.datetime(2025, 1, 9), [HAS, BHA], 4, 0, [SAH, ANJ]),
    Game(datetime.datetime(2025, 1, 9), [HAS, SAH], 4, 0, [BHA, ANJ]),
    Game(datetime.datetime(2025, 1, 9), [BHA, SAH], 3, 1, [HAS, ANJ]),
    Game(datetime.datetime(2025, 1, 16), [SON, SAH], 3, 2, [HAS, ANJ]),
    Game(datetime.datetime(2025, 1, 16), [BHA, SAH], 3, 1, [SON, MIS]),
    Game(datetime.datetime(2025, 1, 16), [BHA, ANJ], 1, 3, [HAS, MIS]),
    Game(datetime.datetime(2025, 1, 16), [BHA, ANJ], 1, 3, [HAS, MIS]),
    Game(datetime.datetime(2025, 1, 22), [SAH], 1, 9, [MIS]),
    Game(datetime.datetime(2025, 1, 30), [SAH, ANJ], 3, 1, [MIS, SON]),
    Game(datetime.datetime(2025, 1, 31), [ANJ], 3, 1, [HAS]),
    Game(datetime.datetime(2025, 2, 6), [MIS, BHA], 4, 0, [HAS, SAH]),
    Game(datetime.datetime(2025, 2, 6), [MIS, DER], 3, 0, [HAS, SAH]),
    Game(datetime.datetime(2025, 2, 7), [HAS], 9, 4, [AKS]),
    Game(datetime.datetime(2025, 2, 9), [HAS, DER], 1, 3, [AKS, SAH]),
    Game(datetime.datetime(2025, 2, 9), [HAS, MIS], 2, 4, [AKS, SAH]),
    Game(datetime.datetime(2025, 2, 9), [BHA], 5, 1, [DER]),
    Game(datetime.datetime(2025, 2, 9), [BHA, DER], 2, 2, [AKS, SAH]),
    Game(datetime.datetime(2025, 2, 9), [HAS], 1, 6, [MIS]),
    Game(datetime.datetime(2025, 2, 10), [SAH], 3, 1, [AKS]),
    Game(datetime.datetime(2025, 2, 10), [SAH], 4, 0, [DEE]),
    Game(datetime.datetime(2025, 2, 10), [DEE], 3, 1, [AKS]),
    Game(datetime.datetime(2025, 2, 21), [HAS, SAH], 3, 1, [AKS, ANJ]),
    Game(datetime.datetime(2025, 2, 21), [HAS, SAH], 2, 3, [MIS, AKS]),
    Game(datetime.datetime(2025, 2, 21), [BHA, ANJ], 1, 3, [AKS, MIS]),
    Game(datetime.datetime(2025, 2, 21), [BHA, ANJ], 1, 3, [HAS, SAH]),
    Game(datetime.datetime(2025, 2, 21), [BHA, ANJ], 1, 3, [HAS, MIS]),
    Game(datetime.datetime(2025, 2, 21), [SAH, AKS], 2, 3, [ANJ, MIS]),
    Game(datetime.datetime(2025, 2, 24), [SAH, ANJ], 0, 4, [HAS, DEE]),
    Game(datetime.datetime(2025, 2, 24), [SAH, DEE], 3, 1, [HAS, ANJ]),
    Game(datetime.datetime(2025, 2, 24), [SAH, DEE], 4, 0, [BHA, AKS]),
    Game(datetime.datetime(2025, 2, 27), [SAH, DER], 0, 4, [HAS, ANJ]),
    Game(datetime.datetime(2025, 2, 27), [SAH, BHA], 2, 2, [HAS, ANJ]),
    Game(datetime.datetime(2025, 2, 27), [SAH, BHA], 2, 2, [HAS, DER]),
    Game(datetime.datetime(2025, 2, 27), [SAH, ANJ], 2, 2, [HAS, DER]),
    Game(datetime.datetime(2025, 3, 2), [ANJ], 1, 3, [HAS]),
    Game(datetime.datetime(2025, 3, 2), [ANJ], 0, 4, [SAH]),
    Game(datetime.datetime(2025, 3, 2), [HAS], 0, 1, [SAH]),
    Game(datetime.datetime(2025, 3, 3), [AKS, DEE], 1, 3, [SAH, MIS]),
    Game(datetime.datetime(2025, 3, 3), [SAH, AKS], 0, 4, [HAS, MIS]),
    Game(datetime.datetime(2025, 3, 3), [SAH, DEE], 0, 4, [HAS, MIS]),
    Game(datetime.datetime(2025, 3, 3), [AKS, HAS], 0, 4, [DEE, MIS]),
    Game(datetime.datetime(2025, 3, 6), [ANJ, HAS], 3, 1, [SAH, BHA]),
    Game(datetime.datetime(2025, 3, 6), [BHA, HAS], 0, 4, [SAH, MIS]),
    Game(datetime.datetime(2025, 3, 6), [BHA, HAS], 0, 4, [ANJ, MIS]),
    # Game(datetime.datetime(2025, 3, 6), [SAH], 21, 29, [MIS], type=GameType.CHA_F),
    Game(datetime.datetime(2025, 3, 6), [SAH], 3, 4, [MIS]),
    Game(datetime.datetime(2025, 3, 9), [BHA, AKS], 3, 1, [HAS, DER]),
    Game(datetime.datetime(2025, 3, 9), [BHA, HAS], 3, 1, [AKS, DER]),
    Game(datetime.datetime(2025, 3, 9), [BHA, DER], 1, 3, [HAS, AKS]),
    Game(datetime.datetime(2025, 3, 10), [AKS], 3, 1, [DEE]),
    Game(datetime.datetime(2025, 3, 10), [AKS], 1, 3, [SAH]),
    Game(datetime.datetime(2025, 3, 10), [DEE], 0, 4, [SAH]),
    Game(datetime.datetime(2025, 3, 12), [BHA], 4, 6, [HAS]),
    Game(datetime.datetime(2025, 4, 9), [HAS], 6, 2, [HIT]),
    Game(datetime.datetime(2025, 4, 10), [HAS], 3, 3, [HIT]),
    Game(datetime.datetime(2025, 4, 10), [HAS, BHA], 1, 3, [AKS, SAH]),
    Game(datetime.datetime(2025, 4, 10), [ANJ, BHA], 1, 3, [AKS, SAH]),
    Game(datetime.datetime(2025, 4, 10), [ANJ, BHA], 0, 4, [AKS, HAS]),
    Game(datetime.datetime(2025, 4, 16), [HAS], 5, 3, [HIT]),
    Game(datetime.datetime(2025, 4, 17), [HAS], 3, 1, [HIT]),
    Game(datetime.datetime(2025, 4, 17), [HAS, SAH], 4, 1, [HIT, MIS]),
    Game(datetime.datetime(2025, 4, 17), [DER, SAH], 6, 4, [BHA, MIS]),
    Game(datetime.datetime(2025, 4, 17), [DER, SAH], 2, 3, [BHA, MIS]),
    Game(datetime.datetime(2025, 4, 20), [HIT], 3, 3, [HAS]),
    Game(datetime.datetime(2025, 4, 24), [SAH, AKS], 7, 5, [MIS, DER]),
    Game(datetime.datetime(2025, 4, 30), [HAS], 1, 3, [MIS]),
    Game(datetime.datetime(2025, 4, 30), [HIT], 0, 4, [MIS]),
    Game(datetime.datetime(2025, 4, 30), [HIT, HAS], 1, 3, [MIS]),
    Game(datetime.datetime(2025, 5, 2), [HAS], 6, 7, [AKS]),
    Game(datetime.datetime(2025, 5, 5), [SAH], 3, 1, [MIS]),
    Game(datetime.datetime(2025, 5, 6), [HAS], 6, 1, [HIT]),
    Game(datetime.datetime(2025, 5, 8), [MIS], 8, 2, [SAH]),
    Game(datetime.datetime(2025, 5, 18), [MIS], 7, 1, [SAH], type=GameType.HP),
    Game(datetime.datetime(2025, 5, 22), [BHA, ANJ], 0, 4, [SAH, DER]),
    Game(datetime.datetime(2025, 5, 22), [BHA, DER], 0, 4, [SAH, ANJ]),
    Game(datetime.datetime(2025, 5, 22), [BHA, DER], 3, 1, [SAH, HAS]),
    Game(datetime.datetime(2025, 5, 25), [SAH], 3, 1, [MIS]),
    Game(datetime.datetime(2025, 5, 28), [HAS], 2, 6, [HIT]),
    Game(datetime.datetime(2025, 5, 29), [HAS, SAH], 3, 2, [BHA, MIS]),
    Game(datetime.datetime(2025, 5, 29), [HAS, SAH], 1, 3, [DER, MIS]),
    Game(datetime.datetime(2025, 5, 29), [BHA, SAH], 3, 2, [DER, MIS]),
    Game(datetime.datetime(2025, 6, 5), [HIT], 3, 11, [HAS]),
    Game(datetime.datetime(2025, 6, 5), [HIT, BHA], 2, 2, [SAH, ANJ]),
    Game(datetime.datetime(2025, 6, 5), [HIT, SAH], 3, 3, [BHA, DER]),
    Game(datetime.datetime(2025, 6, 8), [HAS], 0, 6, [MIS]),
    Game(datetime.datetime(2025, 6, 8), [SAH], 5, 7, [MIS], type=GameType.HP),
    Game(datetime.datetime(2025, 6, 8), [HAS], 0, 6, [MIS]),
    Game(datetime.datetime(2025, 6, 12), [SAH, BHA], 6, 1, [HAS, HIT]),
    Game(datetime.datetime(2025, 6, 12), [SAH, HAS], 6, 0, [HIT, BHA]),
    Game(datetime.datetime(2025, 6, 14), [HAS], 4, 3, [AKS]),
    Game(datetime.datetime(2025, 6, 15), [HAS], 3, 2, [HIT]),
    Game(datetime.datetime(2025, 6, 15), [HAS, ASH], 2, 2, [HIT, DIV]),
    Game(datetime.datetime(2025, 6, 22), [HAS], 2, 2, [ANJ]),
    Game(datetime.datetime(2025, 6, 24), [HAS], 3, 7, [HIT]),
    Game(datetime.datetime(2025, 6, 28), [HAS], 7, 5, [HIT]),
    Game(datetime.datetime(2025, 6, 29), [HAS], 12, 3, [HIT]),
    Game(datetime.datetime(2025, 6, 29), [HAS], 6, 3, [HIT]),
    Game(datetime.datetime(2025, 6, 30), [SAH], 12, 0, [HIT]),
    Game(datetime.datetime(2025, 7, 3), [SAH, MIS], 6, 0, [HAS, ANJ]),
    Game(datetime.datetime(2025, 7, 3), [SAH, HAS], 6, 7, [MIS, ANJ]),
    Game(datetime.datetime(2025, 7, 4), [HAS], 6, 2, [AKS]),
    Game(datetime.datetime(2025, 7, 6), [HAS, DIV], 0, 6, [SAH], type=GameType.HP),
    Game(datetime.datetime(2025, 7, 9), [HAS, HIT], 1, 6, [SAH, MIS]),
    Game(datetime.datetime(2025, 7, 9), [HAS, AKS], 0, 6, [SAH, MIS]),
    Game(datetime.datetime(2025, 7, 9), [ANJ], 4, 3, [HIT]),
    Game(datetime.datetime(2025, 7, 9), [HAS, MIS], 2, 2, [SAH, AKS]),
    Game(datetime.datetime(2025, 7, 9), [HIT, MIS], 2, 6, [SAH, AKS]),
    Game(datetime.datetime(2025, 7, 10), [DEE], 0, 6, [SAH]),
    Game(datetime.datetime(2025, 7, 17), [MIS], 6, 2, [SAH]),
    Game(datetime.datetime(2025, 7, 20), [HAS], 3, 2, [HIT]),
    Game(datetime.datetime(2025, 7, 23), [HAS], 3, 6, [SAH]),
    Game(datetime.datetime(2025, 7, 24), [MIS], 12, 1, [HAS]),
    Game(datetime.datetime(2025, 7, 26), [HAS], 3, 6, [HIT]),
    Game(datetime.datetime(2025, 7, 28), [AKS], 3, 2, [HIT]),
    Game(datetime.datetime(2025, 7, 28), [SAH], 9, 2, [AKS]),
    Game(datetime.datetime(2025, 7, 30), [SAH, HAS], 2, 6, [HIT, MIS]),
    Game(datetime.datetime(2025, 7, 31), [HIT], 3, 2, [HAS]),
    Game(datetime.datetime(2025, 7, 31), [ANJ], 6, 0, [HAN]),
    Game(datetime.datetime(2025, 7, 31), [SAH, HIT], 5, 7, [HAS, MIS]),
]
