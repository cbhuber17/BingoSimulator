import bingo_card as bc


class BingoSimulator:

    def __init__(self, num_simulations):

        self.num_simulations = num_simulations

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
        for i in range(0, bc.CARD_LENGTH * bc.COLUMN_RANGE + 1):

            if i < bc.CARD_LENGTH:
                self.num_line_bingo[0].append(0)  # Rows
                self.num_line_bingo[1].append(0)  # Columns

            self.num_bingo_tries.append(0)

    # ------------------------------------------------------------------------

    def check_diagonal_bingo(self, diag_num, card):

        if diag_num not in [1, 2]:
            raise ValueError(f'Diagonal Number must be 1 or 2 in check_diagonal_bingo(): {diag_num}.')

        if diag_num == 1:
            for i in range(0, bc.CARD_LENGTH):
                if not card[i][i][True]:
                    return False

        elif diag_num == 2:
            for i in range(0, bc.CARD_LENGTH):
                if not card[i][bc.CARD_LENGTH - 1 - i][True]:
                    return False

        self.num_diag_bingo[diag_num - 1] += 1
        return True

    # ------------------------------------------------------------------------

    def check_line_bingo(self, axis, line_num, card):

        if axis not in [0, 1]:
            raise ValueError(f'Axis is not 0 (row) or 1 (column): {axis}.')

        if line_num not in list(range(0, bc.CARD_LENGTH)):
            raise ValueError(f'Line number for axis {axis} must be 0-4 in check_line_bingo(): {line_num}.')

        if axis == 0:
            for j in range(0, bc.CARD_LENGTH):
                if not card[line_num][j][True]:
                    return False
        else:
            for i in range(0, bc.CARD_LENGTH):
                if not card[i][line_num][True]:
                    return False

        self.num_line_bingo[axis][line_num] += 1
        return True

    # ------------------------------------------------------------------------

    def check_corners_bingo(self, card):

        if card[0][0][True] and \
                card[bc.CARD_LENGTH - 1][0][True] and \
                card[0][bc.CARD_LENGTH - 1][True] and \
                card[bc.CARD_LENGTH - 1][bc.CARD_LENGTH - 1][True]:
            self.num_corners_bingo += 1
            return True

        return False

    # ------------------------------------------------------------------------

    def check_traditional_bingo(self, card):

        if self.check_corners_bingo(card):
            return True

        for i in range(0, bc.CARD_LENGTH):

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

        for i in range(0, bc.CARD_LENGTH):

            if i > 0:
                print('\n------------------------')
            for j in range(0, bc.CARD_LENGTH):
                print('|{:2}|'.format(card[i][j][True]), end=" ")

        print('\n------------------------\n\n')

    # ------------------------------------------------------------------------

    def play_bingo(self):

        game_card = bc.BingoCard()

        # Play bingo
        random_all = bc.random.sample(game_card.under_all, bc.CARD_LENGTH * bc.COLUMN_RANGE)
        num_bingo_balls = 0
        got_bingo = False

        for bingo_ball in random_all:

            if got_bingo:
                break

            num_bingo_balls += 1

            for i in range(0, bc.CARD_LENGTH):

                if got_bingo:
                    break

                for j in range(0, bc.CARD_LENGTH):
                    if game_card.bingo_card[i][j][False] == bingo_ball:
                        game_card.bingo_card[i][j][True] = True
                        game_card.marked_bingo_card[i][j][True] = 'X'

                    # Check for bingos
                    if self.check_traditional_bingo(game_card.bingo_card):
                        got_bingo = True
                        # print("BINGO in {} tries".format(num_bingo_balls))
                        self.num_bingo_tries[num_bingo_balls] += 1

                        # print("Numbers called: {}".format(RandomAll[0:num_bingo_balls]))
                        break

        # print_bingo_card(marked_bingo_card)

    # ------------------------------------------------------------------------

    def print_bingo_result(self, item, num_result):
        print("{} bingo:  {}, {}%".format(item, num_result, self.compute_percentage(num_result)))

    # ------------------------------------------------------------------------

    def compute_percentage(self, numerator):
        percentage_factor = float(self.num_simulations / 100.0)

        return float(numerator / percentage_factor)

    # ------------------------------------------------------------------------

    def print_summary(self):

        bingo_ref = {0: 'B', 1: 'I', 2: 'N', 3: 'G', 4: 'O'}
        axis_ref = {0: "Row", 1: "Column"}

        print("\nSummary:\n")

        axis_bingo = [0, 0]  # Row, column
        line_bingo = 0
        diag_bingo = 0

        for axis in [0, 1]:
            for i in range(0, bc.CARD_LENGTH):
                if axis == 0:
                    self.print_bingo_result(f"{axis_ref[axis]} {i}", self.num_line_bingo[axis][i])
                else:
                    self.print_bingo_result(f"{axis_ref[axis]} {bingo_ref[i]}", self.num_line_bingo[axis][i])

                axis_bingo[axis] += self.num_line_bingo[axis][i]

            self.print_bingo_result(f"{axis_ref[axis]}", axis_bingo[axis])
            line_bingo += axis_bingo[axis]

        self.print_bingo_result("Line", line_bingo)

        for i in [0, 1]:
            self.print_bingo_result(f"Diagonal {i+1}", self.num_diag_bingo[i])
            diag_bingo += self.num_diag_bingo[i]

        self.print_bingo_result("Diagonal", diag_bingo)

        self.print_bingo_result("Corners", self.num_corners_bingo)

        print(self.num_bingo_tries)


# ------------------------------------------------------------------------

if __name__ == '__main__':

    bingo_game = BingoSimulator(1000)

    for _ in range(bingo_game.num_simulations):
        bingo_game.play_bingo()

    bingo_game.print_summary()
