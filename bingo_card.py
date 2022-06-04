import random
import copy

# Typical BINGO card layout
CARD_LENGTH = 5  # 5x5 square card
COLUMN_RANGE = 15  # 15 numbers per column to choose from


class BingoCard:

    def __init__(self, free_cell):

        bingo_cell = [0, False]

        self.bingo_card = [[bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                           [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                           [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                           [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                           [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell]]

        column_ranges = [[], [], [], [], []]
        column_random = [[], [], [], [], []]

        for i in range(0, CARD_LENGTH):
            column_ranges[i] = range(COLUMN_RANGE*i + 1, COLUMN_RANGE*(i+1) + 1)
            column_random[i] = random.sample(column_ranges[i], CARD_LENGTH)

        self.under_all = range(1, COLUMN_RANGE * CARD_LENGTH + 1)

        # Create random bingo card:
        for i in range(0, CARD_LENGTH):
            for j in range(0, CARD_LENGTH):
                self.bingo_card[j][i] = [column_random[i][j], False]

        # Is the middle cell FREE?
        if free_cell:
            self.bingo_card[2][2] = [0, True]

        # TODO: May need to remove marked card

    # ------------------------------------------------------------------------

    def print_bingo_card(self):

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

        if diag_num not in [1, 2]:
            raise ValueError(f'Diagonal Number must be 1 or 2 in check_diagonal_bingo(): {diag_num}.')

        if diag_num == 1:
            for i in range(0, CARD_LENGTH):
                if not self.bingo_card[i][i][True]:
                    return False

        else:
            for i in range(0, CARD_LENGTH):
                if not self.bingo_card[i][CARD_LENGTH - 1 - i][True]:
                    return False

        stats.num_diag_bingo[diag_num - 1] += 1
        return True

    # ------------------------------------------------------------------------

    def _check_line_bingo(self, axis, line_num, stats):

        if axis not in [0, 1]:
            raise ValueError(f'Axis is not 0 (row) or 1 (column): {axis}.')

        if line_num not in list(range(0, CARD_LENGTH)):
            raise ValueError(f'Line number for axis {axis} must be 0-4 in check_line_bingo(): {line_num}.')

        if axis == 0:
            for j in range(0, CARD_LENGTH):
                if not self.bingo_card[line_num][j][True]:
                    return False
        else:
            for i in range(0, CARD_LENGTH):
                if not self.bingo_card[i][line_num][True]:
                    return False

        stats.num_line_bingo[axis][line_num] += 1
        return True

    # ------------------------------------------------------------------------

    def _check_corners_bingo(self, stats):

        if self.bingo_card[0][0][True] and \
                self.bingo_card[CARD_LENGTH - 1][0][True] and \
                self.bingo_card[0][CARD_LENGTH - 1][True] and \
                self.bingo_card[CARD_LENGTH - 1][CARD_LENGTH - 1][True]:
            stats.num_corners_bingo += 1
            return True

        return False

    # ------------------------------------------------------------------------

    def check_traditional_bingo(self, stats):

        if self._check_corners_bingo(stats):
            return True

        for i in range(0, CARD_LENGTH):

            if i in [1, 2] and self._check_diagonal_bingo(i, stats):
                return True

            if self._check_line_bingo(0, i, stats) or self._check_line_bingo(1, i, stats):
                return True

        return False
