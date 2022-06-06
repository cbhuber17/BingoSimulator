from bingo_simulator.bingo_card import BingoCard
from bingo_simulator.bingo_simulator_main import BingoStats

PACKAGE_NAME = "bingo_simulator"


def test_bingo_card():
    assert True


def test_diagonal():
    card = BingoCard(False)
    stats = BingoStats(1)

    card.bingo_card[0][0][True] = True
    card.bingo_card[1][1][True] = True
    card.bingo_card[2][2][True] = True
    card.bingo_card[3][3][True] = True
    card.bingo_card[4][4][True] = True

    assert card._check_diagonal_bingo(1, stats) and stats.num_diag_bingo[0] == 1
