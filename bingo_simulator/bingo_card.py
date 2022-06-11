import math
import random
import copy

# Typical BINGO card layout
CARD_LENGTH = 5  # 5x5 square card
COLUMN_RANGE = 15  # 15 numbers per column to choose from


class BingoCard:

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

        stats.df_num_bingo[f'num_diag{diag_num}_bingo'] += 1
        stats.df_num_bingo['num_diag_bingo'] += 1
        return True

    # ------------------------------------------------------------------------

    def _check_line_bingo(self, axis, line_num, stats):

        if axis not in [0, 1]:
            raise ValueError(f'Axis is not 0 (row) or 1 (column): {axis}.')

        if line_num not in list(range(0, CARD_LENGTH)):
            raise ValueError(f'Line number for axis {axis} must be 0-4 in check_line_bingo(): {line_num}.')

        axis_enum = {0: "row", 1: "col"}

        if axis == 0:
            for j in range(0, CARD_LENGTH):
                if not self.bingo_card[line_num][j][True]:
                    return False
        else:
            for i in range(0, CARD_LENGTH):
                if not self.bingo_card[i][line_num][True]:
                    return False

        stats.df_num_bingo[f'num_bingo_{axis_enum[axis]}{line_num}'] += 1
        stats.df_num_bingo[f'num_{axis_enum[axis]}_bingo'] += 1
        stats.df_num_bingo['num_line_bingo'] += 1
        return True

    # ------------------------------------------------------------------------

    def _check_corners_bingo(self, stats):

        if self.bingo_card[0][0][True] and \
                self.bingo_card[CARD_LENGTH - 1][0][True] and \
                self.bingo_card[0][CARD_LENGTH - 1][True] and \
                self.bingo_card[CARD_LENGTH - 1][CARD_LENGTH - 1][True]:
            stats.df_num_bingo['num_corners_bingo'] += 1
            return True

        return False

    # ------------------------------------------------------------------------

    def check_traditional_bingo(self, stats, num_bingo_balls):

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
