from bingo_simulator import bingo_card as bc
import pandas as pd

STATS_FILENAME = "bingo_stats.csv"

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

        # TODO: Pie chart for above stats

        # Tries to get bingo, histogram
        self.num_bingo_tries = []

        # TODO: Stacked bar chart
        self.num_tries_row = [[], [], [], [], []]

        self.num_tries_col = [[], [], [], [], []]

        self.num_tries_diag = [[], []]

        self.num_tries_corners = []

        # Init histogram
        for i in range(0, bc.CARD_LENGTH * bc.COLUMN_RANGE + 1):

            if i < bc.CARD_LENGTH:
                self.num_line_bingo[0].append(0)  # Rows
                self.num_line_bingo[1].append(0)  # Columns

            self.num_bingo_tries.append(0)
            self.num_tries_corners.append(0)

            for j in range(0, bc.CARD_LENGTH):

                if j in [0, 1]:
                    self.num_tries_diag[j].append(0)

                self.num_tries_row[j].append(0)
                self.num_tries_col[j].append(0)

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

        print("Num total tries:", self.num_bingo_tries)
        print("Num corner tries:", self.num_tries_corners)

        for i in range(0, bc.CARD_LENGTH):
            if i in [0, 1]:
                print(f"Num diag {i + 1} tries: ", self.num_tries_diag[i])
            print(f"Num row {i} tries: ", self.num_tries_row[i])
            print(f"Num col {i} tries: ", self.num_tries_col[i])

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
                        if game_card.check_traditional_bingo(self.stats, num_bingo_balls):
                            got_bingo = True
                            self.stats.num_bingo_tries[num_bingo_balls] += 1

                            # print("Numbers called: {}".format(RandomAll[0:num_bingo_balls]))
                            break

    # ------------------------------------------------------------------------


def get_stats_to_df(stats):

    df = pd.DataFrame({"num_bingo_tries": bingo_game_sim.stats.num_bingo_tries,
                       "num_tries_row0": bingo_game_sim.stats.num_tries_row[0],
                       "num_tries_row1": bingo_game_sim.stats.num_tries_row[1],
                       "num_tries_row2": bingo_game_sim.stats.num_tries_row[2],
                       "num_tries_row3": bingo_game_sim.stats.num_tries_row[3],
                       "num_tries_row4": bingo_game_sim.stats.num_tries_row[4],
                       "num_tries_col0": bingo_game_sim.stats.num_tries_col[0],
                       "num_tries_col1": bingo_game_sim.stats.num_tries_col[1],
                       "num_tries_col2": bingo_game_sim.stats.num_tries_col[2],
                       "num_tries_col3": bingo_game_sim.stats.num_tries_col[3],
                       "num_tries_col4": bingo_game_sim.stats.num_tries_col[4],
                       "num_tries_diag1": bingo_game_sim.stats.num_tries_diag[0],
                       "num_tries_diag2": bingo_game_sim.stats.num_tries_diag[1],
                       "num_tries_corners": bingo_game_sim.stats.num_tries_corners,
                       "num_tries_rows": [a + b + c + d + e for a, b, c, d, e in
                                          zip(bingo_game_sim.stats.num_tries_row[0],
                                              bingo_game_sim.stats.num_tries_row[1],
                                              bingo_game_sim.stats.num_tries_row[2],
                                              bingo_game_sim.stats.num_tries_row[3],
                                              bingo_game_sim.stats.num_tries_row[4])],
                       "num_tries_cols": [a + b + c + d + e for a, b, c, d, e in
                                          zip(bingo_game_sim.stats.num_tries_col[0],
                                              bingo_game_sim.stats.num_tries_col[1],
                                              bingo_game_sim.stats.num_tries_col[2],
                                              bingo_game_sim.stats.num_tries_col[3],
                                              bingo_game_sim.stats.num_tries_col[4])],
                       "num_tries_diag": [a + b for a, b in zip(bingo_game_sim.stats.num_tries_diag[0],
                                                                bingo_game_sim.stats.num_tries_diag[1])]})
    return df


if __name__ == '__main__':
    from bingo_simulator import plot_bingo as pb

    num_simulations = 1000

    bingo_game_sim = BingoSimulator(num_simulations)

    bingo_game_sim.play_bingo(False)

    bingo_game_sim.stats.print_summary()

    df = get_stats_to_df(bingo_game_sim.stats)

    df.to_csv(STATS_FILENAME)

    pb.plot_bingo_histo(df)

    pb.plot_bingo_pie(bingo_game_sim.stats)
