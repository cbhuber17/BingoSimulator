import random
import copy


class BingoSimulator:

    def __init__(self, num_simulations):

        self.num_simulations = num_simulations

        # Typical BINGO card layout
        self.card_length = 5  # 5x5 square card
        self.column_range = 15  # 15 numbers per column to choose from

        # How many times a certain row/col got bingo
        # Axis = 0 = row
        # Axis = 1 = column
        self.num_line_bingo = [[], []]

        # Two diagonals
        self.num_diag_bingo = [0, 0]

        # All 4 corners bingo
        self.num_corners_bingo = 0

        # Tries to get bingo, histogram
        self.num_bingo_tries = []

        # TODO: num tries row0-4 bingo, col0-4 bingo, diag, corners, etc.

        # Init histogram
        for i in range(0, self.card_length * self.column_range + 1):

            if i < self.card_length:
                self.num_line_bingo[0].append(0)  # Rows
                self.num_line_bingo[1].append(0)  # Columns

            self.num_bingo_tries.append(0)

    # ------------------------------------------------------------------------

    def check_diagonal_bingo(self, diag_num, card):

        if diag_num not in [1, 2]:
            raise ValueError(f'Diagonal Number must be 1 or 2 in check_diagonal_bingo(): {diag_num}.')

        if diag_num == 1:
            for i in range(0, self.card_length):
                if not card[i][i][True]:
                    return False

        elif diag_num == 2:
            for i in range(0, self.card_length):
                if not card[i][self.card_length - 1 - i][True]:
                    return False

        self.num_diag_bingo[diag_num - 1] += 1
        return True

    # ------------------------------------------------------------------------

    def check_line_bingo(self, axis, line_num, card):

        if axis not in [0, 1]:
            raise ValueError(f'Axis is not 0 (row) or 1 (column): {axis}.')

        if line_num not in list(range(0, self.card_length)):
            raise ValueError(f'Line number for axis {axis} must be 0-4 in check_line_bingo(): {line_num}.')

        if axis == 0:
            for j in range(0, self.card_length):
                if not card[line_num][j][True]:
                    return False
        else:
            for i in range(0, self.card_length):
                if not card[i][line_num][True]:
                    return False

        self.num_line_bingo[axis][line_num] += 1
        return True

    # ------------------------------------------------------------------------

    def check_corners_bingo(self, card):

        if card[0][0][True] and \
                card[self.card_length - 1][0][True] and \
                card[0][self.card_length - 1][True] and \
                card[self.card_length - 1][self.card_length - 1][True]:
            self.num_corners_bingo += 1
            return True

        return False

    # ------------------------------------------------------------------------

    def check_traditional_bingo(self, card):

        if self.check_corners_bingo(card):
            return True

        for i in range(0, self.card_length):

            if i in [1, 2] and self.check_diagonal_bingo(i, card):
                return True

            if self.check_line_bingo(0, i, card) or self.check_line_bingo(1, i, card):
                return True

        return False

    # ------------------------------------------------------------------------

    def print_bingo_card(self, card):

        print('------------------------')
        print('|B | |I | |N | |G | |O |')
        print('------------------------')

        for i in range(0, self.card_length):

            if i > 0:
                print('\n------------------------')
            for j in range(0, self.card_length):
                print('|{:2}|'.format(card[i][j][True]), end=" ")

        print('\n------------------------\n\n')

    # ------------------------------------------------------------------------

    def play_bingo(self):

        # Initialize
        bingo_cell = [0, False]
        bingo_card = [[bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                      [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                      [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                      [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                      [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell]]

        # TODO: Better way to init card
        bingo_card2 = []

        for i in range(0, self.card_length):
            bingo_card2.append(bingo_cell)

        for j in range(0, self.card_length):
            bingo_card2.append(bingo_card2[0])

        under_b = range(1, self.column_range + 1)
        under_i = range(self.column_range + 1, self.column_range * 2 + 1)
        under_n = range(self.column_range * 2 + 1, self.column_range * 3 + 1)
        under_g = range(self.column_range * 3 + 1, self.column_range * 4 + 1)
        under_o = range(self.column_range * 4 + 1, self.column_range * self.card_length + 1)

        under_all = range(1, self.column_range * self.card_length + 1)

        random_b = random.sample(under_b, self.card_length)
        random_i = random.sample(under_i, self.card_length)
        random_n = random.sample(under_n, self.card_length)
        random_g = random.sample(under_g, self.card_length)
        random_o = random.sample(under_o, self.card_length)

        # Create random bingo card:
        for i in range(0, self.card_length):
            for j in range(0, self.card_length):

                if i == 0:
                    bingo_card[j][0] = [random_b[j], False]
                if i == 1:
                    bingo_card[j][1] = [random_i[j], False]
                if i == 2:
                    bingo_card[j][2] = [random_n[j], False]
                if i == 3:
                    bingo_card[j][3] = [random_g[j], False]
                if i == 4:
                    bingo_card[j][4] = [random_o[j], False]

        # TODO: is the middle cell FREE?
        # bingo_card[2][2] = [0, True]

        # print_bingo_card(bingo_card)
        marked_bingo_card = copy.deepcopy(bingo_card)

        # Play bingo
        random_all = random.sample(under_all, self.card_length * self.column_range)
        num_bingo_balls = 0
        got_bingo = False

        for bingo_ball in random_all:

            if got_bingo:
                break

            num_bingo_balls += 1

            for i in range(0, self.card_length):

                if got_bingo:
                    break

                for j in range(0, self.card_length):
                    if bingo_card[i][j][False] == bingo_ball:
                        bingo_card[i][j][True] = True
                        marked_bingo_card[i][j][True] = 'X'

                    # Check for bingos
                    if self.check_traditional_bingo(bingo_card):
                        got_bingo = True
                        # print("BINGO in {} tries".format(num_bingo_balls))
                        self.num_bingo_tries[num_bingo_balls] += 1

                        # print("Numbers called: {}".format(RandomAll[0:num_bingo_balls]))
                        break

        # print_bingo_card(marked_bingo_card)

    # ------------------------------------------------------------------------

    def print_summary(self):

        percentage_factor = float(self.num_simulations / 100.0)
        bingo_ref = {0: 'B', 1: 'I', 2: 'N', 3: 'G', 4: 'O'}

        print("\nSummary:\n")

        row_bingo = 0
        col_bingo = 0
        diag_bingo = 0

        for i in range(0, self.card_length):
            print("Row {} bingo: {}, {}%".format(i, self.num_line_bingo[0][i],
                                                 float(self.num_line_bingo[0][i] / percentage_factor)))

            row_bingo += self.num_line_bingo[0][i]

        print("Row Bingo: {}, {}%\n".format(row_bingo, float(row_bingo / percentage_factor)))

        for i in range(0, self.card_length):
            print("Under {} bingo: {}, {}%".format(bingo_ref[i], self.num_line_bingo[1][i],
                                                   float(self.num_line_bingo[1][i] / percentage_factor)))
            col_bingo += self.num_line_bingo[1][i]

        print("Column Bingo: {}, {}%\n".format(col_bingo, float(col_bingo / percentage_factor)))

        line_bingo = row_bingo + col_bingo
        print("Line Bingo: {}, {}%\n".format(line_bingo, float(line_bingo / percentage_factor)))

        for i in [0, 1]:
            print("Diagonal {} bingo: {}, {}%".format(i+1, self.num_diag_bingo[i],
                                                      float(self.num_diag_bingo[i] / percentage_factor)))
            diag_bingo += self.num_diag_bingo[i]

        print("Diagonal bingo: {}, {}%\n".format(diag_bingo, float(diag_bingo / percentage_factor)))

        print("Corners bingo: {}, {}%\n".format(self.num_corners_bingo,
                                                float(self.num_corners_bingo / percentage_factor)))

        print(self.num_bingo_tries)


# ------------------------------------------------------------------------

if __name__ == '__main__':

    bingo_game = BingoSimulator(1000)

    for _ in range(bingo_game.num_simulations):
        bingo_game.play_bingo()

    bingo_game.print_summary()
