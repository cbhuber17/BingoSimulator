from bingo_simulator import bingo_card as bc


class BingoStats:

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

    def _print_bingo_result(self, item, num_result):
        print("{} bingo:  {}, {}%".format(item, num_result, self._compute_percentage(num_result)))

    # ------------------------------------------------------------------------

    def _compute_percentage(self, numerator):
        percentage_factor = float(self.num_simulations / 100.0)

        return float(numerator / percentage_factor)

    # ------------------------------------------------------------------------

    def print_summary(self):

        bingo_ref = {0: 'B', 1: 'I', 2: 'N', 3: 'G', 4: 'O'}
        axis_ref = {0: "Row", 1: "Column"}

        axis_bingo = [0, 0]  # Row, column
        line_bingo = 0
        diag_bingo = 0

        print("\nSummary:\n")

        for axis in [0, 1]:
            for i in range(0, bc.CARD_LENGTH):
                if axis == 0:
                    self._print_bingo_result(f"{axis_ref[axis]} {i}", self.num_line_bingo[axis][i])
                else:
                    self._print_bingo_result(f"{axis_ref[axis]} {bingo_ref[i]}", self.num_line_bingo[axis][i])

                axis_bingo[axis] += self.num_line_bingo[axis][i]

            self._print_bingo_result(f"{axis_ref[axis]}", axis_bingo[axis])
            line_bingo += axis_bingo[axis]

        self._print_bingo_result("Line", line_bingo)

        for i in [0, 1]:
            self._print_bingo_result(f"Diagonal {i + 1}", self.num_diag_bingo[i])
            diag_bingo += self.num_diag_bingo[i]

        self._print_bingo_result("Diagonal", diag_bingo)

        self._print_bingo_result("Corners", self.num_corners_bingo)

        print(self.num_bingo_tries)

    # ------------------------------------------------------------------------


class BingoSimulator:

    def __init__(self, num_simulations):

        self.stats = BingoStats(num_simulations)

    # ------------------------------------------------------------------------

    def play_bingo(self, free_cell):

        for _ in range(self.stats.num_simulations):

            game_card = bc.BingoCard(free_cell)

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

                        # Check for bingos
                        if game_card.check_traditional_bingo(self.stats):
                            got_bingo = True
                            self.stats.num_bingo_tries[num_bingo_balls] += 1

                            # print("Numbers called: {}".format(RandomAll[0:num_bingo_balls]))
                            break

    # ------------------------------------------------------------------------


if __name__ == '__main__':
    from bingo_simulator import plot_bingo_histo as pbh

    num_simulations = 1000

    bingo_game_sim = BingoSimulator(num_simulations)

    bingo_game_sim.play_bingo(False)

    bingo_game_sim.stats.print_summary()

    pbh.plot_bingo_histo(bingo_game_sim.stats.num_bingo_tries)
