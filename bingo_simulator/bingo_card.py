"""Contains a class to host a bingo card, plus checking for each type of bingo win."""

import math
import random
import copy

# Typical BINGO card layout
CARD_LENGTH = 5  # 5x5 square card
COLUMN_RANGE = 15  # 15 numbers per column to choose from


class BingoCard:
    """A bingo card class, defined by the constants CARD_LENGTH and COLUMN_RANGE.  Contains a bingo card, plus
    all the available BINGO numbers to select from.  Each cell in a 2D bingo card is a list[int, bool], where
    the int is the random number for the bingo cell and the bool is if this cell is marked (dabbed, True) or not
    (False)"""

    def __init__(self, free_cell):

        bingo_cell = [0, False]

        self.bingo_card = []
        bingo_row = []

        column_ranges = []
        column_random = []

        for i in range(0, CARD_LENGTH):
            self.bingo_card.append([])
            column_ranges.append([])
            column_random.append([])
            bingo_row.append(copy.deepcopy(bingo_cell))

        for i in range(0, CARD_LENGTH):
            self.bingo_card[i] = copy.deepcopy(bingo_row)
            column_ranges[i] = range(COLUMN_RANGE*i + 1, COLUMN_RANGE*(i+1) + 1)
            column_random[i] = random.sample(column_ranges[i], CARD_LENGTH)

        self.under_all = range(1, COLUMN_RANGE * CARD_LENGTH + 1)

        # Create random bingo card:
        for i in range(0, CARD_LENGTH):
            for j in range(0, CARD_LENGTH):
                self.bingo_card[j][i] = [column_random[i][j], False]

        # Is the middle cell FREE?  Only applicable to bingo cards that have odd dimensions
        mid_index = math.floor(CARD_LENGTH)
        if free_cell and CARD_LENGTH % 2 == 1:
            self.bingo_card[mid_index][mid_index] = [0, True]

    # ------------------------------------------------------------------------

    def print_bingo_card(self):
        """Prints the BINGO card to console.
        :param: None
        :return: None"""

        print('------------------------')
        print('|B | |I | |N | |G | |O |')
        print('------------------------')

        for i in range(0, CARD_LENGTH):

            if i > 0:
                print('\n------------------------')
            for j in range(0, CARD_LENGTH):
                print('|{:2}|'.format(self.bingo_card[i][j][True]), end=" ")

        print('\n------------------------\n\n')

    # ------------------------------------------------------------------------

    def _check_diagonal_bingo(self, diag_num, stats):
        """Checks if the card has a diagonal BINGO. Increments the stats counter for diagonals if so.
        :param: diag_num (int) as 1 or 2
        :param: stats (BingoStats) class
        :return: True if diagonal 1 or diagonal 2 have BINGO, False otherwise.

        There are two diagonals for BINGO:
        Diagonal 1:
        ------------------------
        |B | |I | |N | |G | |O |
        ------------------------
        |X | |  | |  | |  | |  |
        |  | |X | |  | |  | |  |
        |  | |  | |X | |  | |  |
        |  | |  | |  | |X | |  |
        |  | |  | |  | |  | |X |
        ------------------------

         Diagonal 2:
        ------------------------
        |B | |I | |N | |G | |O |
        ------------------------
        |  | |  | |  | |  | |X |
        |  | |  | |  | |X | |  |
        |  | |  | |X | |  | |  |
        |  | |X | |  | |  | |  |
        |X | |  | |  | |  | |  |
        ------------------------"""

        # Check valid input
        if diag_num not in [1, 2]:
            raise ValueError(f'Diagonal Number must be 1 or 2 in check_diagonal_bingo(): {diag_num}.')

        # Check Diag 1
        if diag_num == 1:
            for i in range(0, CARD_LENGTH):
                if not self.bingo_card[i][i][True]:
                    return False

        # Check Diag 2
        else:
            for i in range(0, CARD_LENGTH):
                if not self.bingo_card[i][CARD_LENGTH - 1 - i][True]:
                    return False

        # Apply stats to specific diagonal and total diagonal
        stats.df_num_bingo[f'num_diag{diag_num}_bingo'] += 1
        stats.df_num_bingo['num_diag_bingo'] += 1
        return True

    # ------------------------------------------------------------------------

    def _check_line_bingo(self, axis, line_num, stats):
        """Checks if the card has a row/column BINGO. Increments the stats counter for the specific row/col if so.
        :param: axis (int) as 0 (row) or 1 (col)
        :param: line_num (int) a number between 0 and CARD_LENGTH, e.g. as row0, row1, column0, column1, etc.
        :param: stats (BingoStats) class
        :return: True if any row or column have BINGO, False otherwise.

        Example Row 1 BINGO:
        ------------------------
        |B | |I | |N | |G | |O |
        ------------------------
        |  | |  | |  | |  | |  |
        |X | |X | |X | |X | |X |
        |  | |  | |  | |  | |  |
        |  | |  | |  | |  | |  |
        |  | |  | |  | |  | |  |
        ------------------------

        Example Column G (column 3) BINGO:
        ------------------------
        |B | |I | |N | |G | |O |
        ------------------------
        |  | |  | |  | |X | |  |
        |  | |  | |  | |X | |  |
        |  | |  | |  | |X | |  |
        |  | |  | |  | |X | |  |
        |  | |  | |  | |X | |  |
        ------------------------"""

        # Check inputs
        if axis not in [0, 1]:
            raise ValueError(f'Axis is not 0 (row) or 1 (column): {axis}.')
        if line_num not in list(range(0, CARD_LENGTH)):
            raise ValueError(f'Line number for axis {axis} must be 0-{CARD_LENGTH-1} in check_line_bingo(): {line_num}')

        # Check row/col for BINGO
        if axis == 0:
            for j in range(0, CARD_LENGTH):
                if not self.bingo_card[line_num][j][True]:
                    return False
        else:
            for i in range(0, CARD_LENGTH):
                if not self.bingo_card[i][line_num][True]:
                    return False

        axis_enum = {0: "row", 1: "col"}

        # Increment stats
        stats.df_num_bingo[f'num_bingo_{axis_enum[axis]}{line_num}'] += 1
        stats.df_num_bingo[f'num_{axis_enum[axis]}_bingo'] += 1
        stats.df_num_bingo['num_line_bingo'] += 1
        return True

    # ------------------------------------------------------------------------

    def _check_corners_bingo(self, stats):
        """Checks if the card has a corners BINGO. Increments the stats counter for corners if so.
        :param: stats (BingoStats) class
        :return: True if the corners have BINGO, False otherwise.

        Corners BINGO:
        ------------------------
        |B | |I | |N | |G | |O |
        ------------------------
        |X | |  | |  | |  | |X |
        |  | |  | |  | |  | |  |
        |  | |  | |  | |  | |  |
        |  | |  | |  | |  | |  |
        |X | |  | |  | |  | |X |
        ------------------------"""

        if self.bingo_card[0][0][True] and \
                self.bingo_card[CARD_LENGTH - 1][0][True] and \
                self.bingo_card[0][CARD_LENGTH - 1][True] and \
                self.bingo_card[CARD_LENGTH - 1][CARD_LENGTH - 1][True]:
            stats.df_num_bingo['num_corners_bingo'] += 1
            return True

        return False

    # ------------------------------------------------------------------------

    def check_traditional_bingo(self, stats, num_bingo_balls):
        """Checks if the card has any BINGO. Increments the stats counter for corners if so.
        :param: stats (BingoStats) class
        :param: num_bingo_balls (int), the current number of bingo balls called so far
        :return: True if any BINGO was found, False otherwise."""

        if self._check_corners_bingo(stats):
            stats.df_tries['num_tries_corners'][num_bingo_balls] += 1
            return True

        for i in range(0, CARD_LENGTH):

            if i in [1, 2] and self._check_diagonal_bingo(i, stats):
                stats.df_tries[f'num_tries_diag{i}'][num_bingo_balls] += 1
                stats.df_tries[f'num_tries_diag'][num_bingo_balls] += 1
                return True

            if self._check_line_bingo(0, i, stats):
                stats.df_tries[f'num_tries_row{i}'][num_bingo_balls] += 1
                stats.df_tries[f'num_tries_rows'][num_bingo_balls] += 1
                return True

            if self._check_line_bingo(1, i, stats):
                stats.df_tries[f'num_tries_col{i}'][num_bingo_balls] += 1
                stats.df_tries[f'num_tries_cols'][num_bingo_balls] += 1
                return True

        return False
