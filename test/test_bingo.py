import pytest
from bingo_simulator.bingo_card import BingoCard
from bingo_simulator.bingo_card import CARD_LENGTH
from bingo_simulator.bingo_simulator_main import BingoStats

PACKAGE_NAME = "bingo_simulator"


# Helper functions for unit testing
# -------------------------------------------------------------------------------------------------------------

def get_card_and_stats():
    return BingoCard(False), BingoStats(1)


# -------------------------------------------------------------------------------------------------------------

def get_valid_diagonal1():
    card, stats = get_card_and_stats()

    for i in range(0, CARD_LENGTH):
        card.bingo_card[i][i][True] = True

    return card, stats


# -------------------------------------------------------------------------------------------------------------

def get_valid_diagonal2():
    card, stats = get_card_and_stats()

    for i in range(0, CARD_LENGTH):
        card.bingo_card[i][CARD_LENGTH - 1 - i][True] = True

    return card, stats


# -------------------------------------------------------------------------------------------------------------


def get_valid_row(row_num):
    card, stats = get_card_and_stats()

    for i in range(0, CARD_LENGTH):
        card.bingo_card[row_num][i][True] = True

    return card, stats


# -------------------------------------------------------------------------------------------------------------

def get_valid_col(col_num):
    card, stats = get_card_and_stats()

    for i in range(0, CARD_LENGTH):
        card.bingo_card[i][col_num][True] = True

    return card, stats


# -------------------------------------------------------------------------------------------------------------

def get_valid_corners():
    card, stats = get_card_and_stats()
    corner_index = CARD_LENGTH - 1

    card.bingo_card[0][0][True] = True
    card.bingo_card[corner_index][0][True] = True
    card.bingo_card[0][corner_index][True] = True
    card.bingo_card[corner_index][corner_index][True] = True

    return card, stats


# End helper functions
# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------
# Begin tests

def test_valid_diagonal_one():
    card, stats = get_valid_diagonal1()
    assert card._check_diagonal_bingo(1, stats) and stats.num_diag_bingo[0] == 1


# -------------------------------------------------------------------------------------------------------------

def test_valid_diagonal_two():
    card, stats = get_valid_diagonal2()
    assert card._check_diagonal_bingo(2, stats) and stats.num_diag_bingo[1] == 1


# -------------------------------------------------------------------------------------------------------------

bad_diagonal_one_cards = []
diagonal_one_stats = []

for i in range(0, CARD_LENGTH):
    card, stats = get_valid_diagonal1()
    card.bingo_card[i][i][True] = False
    bad_diagonal_one_cards.append(card)
    diagonal_one_stats.append(stats)

cards_and_stats = list(zip(bad_diagonal_one_cards, diagonal_one_stats))


@pytest.mark.parametrize('card_and_stat', cards_and_stats)
def test_bad_diagonal_one(card_and_stat):
    assert not card_and_stat[0]._check_diagonal_bingo(1, card_and_stat[1]) and card_and_stat[1].num_diag_bingo[0] == 0


# -------------------------------------------------------------------------------------------------------------

bad_diagonal_two_cards = []
diagonal_two_stats = []

for i in range(0, CARD_LENGTH):
    card, stats = get_valid_diagonal2()
    card.bingo_card[i][CARD_LENGTH - 1 - i][True] = False
    bad_diagonal_two_cards.append(card)
    diagonal_two_stats.append(stats)

cards_and_stats = list(zip(bad_diagonal_two_cards, diagonal_two_stats))


@pytest.mark.parametrize('card_and_stat', cards_and_stats)
def test_bad_diagonal_two(card_and_stat):
    assert not card_and_stat[0]._check_diagonal_bingo(2, card_and_stat[1]) and card_and_stat[1].num_diag_bingo[1] == 0


# -------------------------------------------------------------------------------------------------------------

good_rows = []
good_row_stats = []
line_num = []

for i in range(0, CARD_LENGTH):
    good_rows.append(get_valid_row(i)[0])
    good_row_stats.append(get_valid_row(i)[1])
    line_num.append(i)

cards_and_stats_and_line_nums = list(zip(good_rows, good_row_stats, line_num))


@pytest.mark.parametrize('cards_and_stats_and_line_num', cards_and_stats_and_line_nums)
def test_valid_rows(cards_and_stats_and_line_num):
    assert cards_and_stats_and_line_num[0]._check_line_bingo(0, cards_and_stats_and_line_num[2],
                                                             cards_and_stats_and_line_num[1]) \
           and cards_and_stats_and_line_num[1].num_line_bingo[0][cards_and_stats_and_line_num[2]] == 1


# -------------------------------------------------------------------------------------------------------------

good_cols = []
good_col_stats = []
line_num = []

for i in range(0, CARD_LENGTH):
    good_cols.append(get_valid_col(i)[0])
    good_col_stats.append(get_valid_col(i)[1])
    line_num.append(i)

cards_and_stats_and_line_nums = list(zip(good_cols, good_col_stats, line_num))


@pytest.mark.parametrize('cards_and_stats_and_line_num', cards_and_stats_and_line_nums)
def test_valid_cols(cards_and_stats_and_line_num):
    assert cards_and_stats_and_line_num[0]._check_line_bingo(1, cards_and_stats_and_line_num[2],
                                                             cards_and_stats_and_line_num[1]) \
           and cards_and_stats_and_line_num[1].num_line_bingo[1][cards_and_stats_and_line_num[2]] == 1


# -------------------------------------------------------------------------------------------------------------

bad_rows = []
bad_row_stats = []
line_num = []

for bad_col in range(0, CARD_LENGTH):
    for i in range(0, CARD_LENGTH):
        card, stats = get_valid_row(i)
        card.bingo_card[i][bad_col][True] = False
        bad_rows.append(card)
        bad_row_stats.append(stats)
        line_num.append(i)

cards_and_stats_and_line_nums = list(zip(bad_rows, bad_row_stats, line_num))


@pytest.mark.parametrize('cards_and_stats_and_line_num', cards_and_stats_and_line_nums)
def test_invalid_rows(cards_and_stats_and_line_num):
    assert not cards_and_stats_and_line_num[0]._check_line_bingo(0, cards_and_stats_and_line_num[2],
                                                                 cards_and_stats_and_line_num[1]) \
           and cards_and_stats_and_line_num[1].num_line_bingo[0][cards_and_stats_and_line_num[2]] == 0


# -------------------------------------------------------------------------------------------------------------

bad_cols = []
bad_col_stats = []
line_num = []

for bad_row in range(0, CARD_LENGTH):
    for i in range(0, CARD_LENGTH):
        card, stats = get_valid_col(i)
        card.bingo_card[bad_row][i][True] = False
        bad_cols.append(card)
        bad_col_stats.append(stats)
        line_num.append(i)

cards_and_stats_and_line_nums = list(zip(bad_cols, bad_col_stats, line_num))


@pytest.mark.parametrize('cards_and_stats_and_line_num', cards_and_stats_and_line_nums)
def test_invalid_cols(cards_and_stats_and_line_num):
    assert not cards_and_stats_and_line_num[0]._check_line_bingo(1, cards_and_stats_and_line_num[2],
                                                                 cards_and_stats_and_line_num[1]) \
           and cards_and_stats_and_line_num[1].num_line_bingo[1][cards_and_stats_and_line_num[2]] == 0


# -------------------------------------------------------------------------------------------------------------

def test_valid_corners():
    card, stats = get_valid_corners()
    assert card._check_corners_bingo(stats) and stats.num_corners_bingo == 1


# -------------------------------------------------------------------------------------------------------------

def test_invalid_corner1():
    card, stats = get_valid_corners()
    card.bingo_card[0][0][True] = False
    assert not card._check_corners_bingo(stats) and stats.num_corners_bingo == 0


# -------------------------------------------------------------------------------------------------------------

def test_invalid_corner2():
    card, stats = get_valid_corners()
    card.bingo_card[CARD_LENGTH - 1][0][True] = False
    assert not card._check_corners_bingo(stats) and stats.num_corners_bingo == 0


# -------------------------------------------------------------------------------------------------------------

def test_invalid_corner3():
    card, stats = get_valid_corners()
    card.bingo_card[0][CARD_LENGTH - 1][True] = False
    assert not card._check_corners_bingo(stats) and stats.num_corners_bingo == 0


# -------------------------------------------------------------------------------------------------------------

def test_invalid_corner4():
    card, stats = get_valid_corners()
    card.bingo_card[CARD_LENGTH - 1][CARD_LENGTH - 1][True] = False
    assert not card._check_corners_bingo(stats) and stats.num_corners_bingo == 0
