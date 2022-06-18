"""Contains classes to run BINGO several times, plus keeping statistics of each BINGO win."""

from bingo_simulator import bingo_card as bc
import pandas as pd

# Global filenames
STATS_TRIES_FILENAME = "bingo_tries.csv"
BINGO_STATS_FILENAME = "bingo_stats.csv"


class BingoStats:
    """A class holding statistics from the outcome of each BINGO, including:
    - Number of BINGO simulations
    - How many times a certain row/col/diagonal/corners got BINGO
    - How many bingo balls (tries) it took to get a certain row/col/diagonal/corners BINGO"""

    def __init__(self, num_simulations):

        self.num_simulations = num_simulations

        self.df_num_bingo = pd.DataFrame()

        # How many times a certain row/col got bingo
        for i in range(0, bc.CARD_LENGTH):
            self.df_num_bingo[f'num_bingo_row{i}'] = pd.Series([0])
            self.df_num_bingo[f'num_bingo_col{i}'] = pd.Series([0])

        self.df_num_bingo['num_row_bingo'] = pd.Series([0])
        self.df_num_bingo['num_col_bingo'] = pd.Series([0])
        self.df_num_bingo['num_line_bingo'] = pd.Series([0])

        # Two diagonals
        self.df_num_bingo['num_diag1_bingo'] = pd.Series([0])
        self.df_num_bingo['num_diag2_bingo'] = pd.Series([0])
        self.df_num_bingo['num_diag_bingo'] = pd.Series([0])

        # All 4 corners bingo
        self.df_num_bingo['num_corners_bingo'] = pd.Series([0])

        self.df_tries = pd.DataFrame()

        # Tries to get bingo, histogram
        self.df_tries['num_bingo_tries'] = pd.DataFrame(0, index=range(bc.CARD_LENGTH * bc.COLUMN_RANGE),
                                                        columns=range(1))

        for i in range(0, bc.CARD_LENGTH):
            self.df_tries[f'num_tries_row{i}'] = pd.DataFrame(0, index=range(bc.CARD_LENGTH * bc.COLUMN_RANGE),
                                                              columns=range(1))
            self.df_tries[f'num_tries_col{i}'] = pd.DataFrame(0, index=range(bc.CARD_LENGTH * bc.COLUMN_RANGE),
                                                              columns=range(1))

        self.df_tries['num_tries_rows'] = pd.DataFrame(0, index=range(bc.CARD_LENGTH * bc.COLUMN_RANGE),
                                                       columns=range(1))
        self.df_tries['num_tries_cols'] = pd.DataFrame(0, index=range(bc.CARD_LENGTH * bc.COLUMN_RANGE),
                                                       columns=range(1))

        self.df_tries['num_tries_diag1'] = pd.DataFrame(0, index=range(bc.CARD_LENGTH * bc.COLUMN_RANGE),
                                                        columns=range(1))
        self.df_tries['num_tries_diag2'] = pd.DataFrame(0, index=range(bc.CARD_LENGTH * bc.COLUMN_RANGE),
                                                        columns=range(1))
        self.df_tries['num_tries_diag'] = pd.DataFrame(0, index=range(bc.CARD_LENGTH * bc.COLUMN_RANGE),
                                                       columns=range(1))

        self.df_tries['num_tries_corners'] = pd.DataFrame(0, index=range(bc.CARD_LENGTH * bc.COLUMN_RANGE),
                                                          columns=range(1))

    # ------------------------------------------------------------------------

    def _print_bingo_result(self, item, num_result):
        """Prints a single BINGO result.
        :param: item (str) The description of the item being printed (e.g. row, col, diag, etc.)
        :param: num_result (pd.Series) The number of BINGO(s) that occurred.
        :return: None"""

        print("{} bingo:  {}, {}%".format(item, int(num_result.values), self._compute_percentage(num_result)))

    # ------------------------------------------------------------------------

    def _compute_percentage(self, numerator):
        """Computes the percentage of the BINGO result.
        :param: numerator (int) The numerator (number of BINGO(s)) that occurred.
        :return: (float) The percentage of BINGO(s) that occurred."""

        percentage_factor = float(self.num_simulations / 100.0)
        return float(numerator / percentage_factor)

    # ------------------------------------------------------------------------

    def print_summary(self):
        """Prints a summary of the BINGO results to the console.
        :param: None
        :return: None"""

        bingo_ref = {0: 'B', 1: 'I', 2: 'N', 3: 'G', 4: 'O'}

        print("\nSummary:\n")

        for i in range(0, bc.CARD_LENGTH):
            self._print_bingo_result(f"Row {i}", self.df_num_bingo[f'num_bingo_row{i}'])
            self._print_bingo_result(f"Column {bingo_ref[i]}", self.df_num_bingo[f'num_bingo_col{i}'])

        self._print_bingo_result("Row", self.df_num_bingo[f'num_row_bingo'])
        self._print_bingo_result("Column", self.df_num_bingo[f'num_col_bingo'])
        self._print_bingo_result("Line", self.df_num_bingo[f'num_line_bingo'])

        for i in [1, 2]:
            self._print_bingo_result(f"Diagonal {i}", self.df_num_bingo[f'num_diag{i}_bingo'])

        self._print_bingo_result("Diagonal", self.df_num_bingo[f'num_diag_bingo'])

        self._print_bingo_result("Corners", self.df_num_bingo['num_corners_bingo'])

        print("Num total tries:", self.df_tries['num_bingo_tries'].values)
        print("Num corner tries:", self.df_tries['num_tries_corners'].values)

        for i in range(0, bc.CARD_LENGTH):
            if i in [1, 2]:
                print(f"Num diag {i} tries: ", self.df_tries[f'num_tries_diag{i}'].values)
            print(f"Num row {i} tries: ", self.df_tries[f'num_tries_row{i}'].values)
            print(f"Num col {i} tries: ", self.df_tries[f'num_tries_col{i}'].values)

    # ------------------------------------------------------------------------


class BingoSimulator:
    """A class that runs a BINGO card multiple times and keeps track of statistics of each BINGO win."""

    def __init__(self, num_simulations):
        self.stats = BingoStats(num_simulations)

    # ------------------------------------------------------------------------

    def play_bingo(self, free_cell):
        """Plays BINGO num_simulations times!
        :param: free_cell (bool) Is the center cell considered free?  True marks it free (already marked/dabbed),
        False makes it unmarked.  Only applicable for BINGO cards that have an odd-number dimensions.
        :return: None"""

        for _ in range(self.stats.num_simulations):

            game_card = bc.BingoCard(free_cell)

            # Play bingo
            random_all = bc.random.sample(game_card.under_all, bc.CARD_LENGTH * bc.COLUMN_RANGE)
            num_bingo_balls = 0
            got_bingo = False

            # Grab a random bingo ball and stop playing if BINGO is found
            for bingo_ball in (bingo_ball for bingo_ball in random_all if not got_bingo):
                num_bingo_balls += 1

                # Go through each bingo cell to check if the bingo ball is on the bingo card
                for i in (i for i in range(0, bc.CARD_LENGTH) if not got_bingo):
                    for j in range(0, bc.CARD_LENGTH):
                        if game_card.bingo_card[i][j][False] == bingo_ball:
                            game_card.bingo_card[i][j][True] = True

                        # Check for BINGO
                        if game_card.check_traditional_bingo(self.stats, num_bingo_balls):
                            got_bingo = True
                            self.stats.df_tries['num_bingo_tries'][num_bingo_balls] += 1
                            break

    # ------------------------------------------------------------------------


# Plotting is only to be done if this module is called directly
if __name__ == '__main__':
    from bingo_simulator import plot_bingo as pb

    num_simulations = 1000

    bingo_game_sim = BingoSimulator(num_simulations)
    bingo_game_sim.play_bingo(False)
    bingo_game_sim.stats.print_summary()

    # Save data from simulation in csv files
    bingo_game_sim.stats.df_tries.to_csv(STATS_TRIES_FILENAME)
    bingo_game_sim.stats.df_num_bingo.to_csv(BINGO_STATS_FILENAME)

    # Plot results in histogram and pie chart
    pb.plot_bingo_histo(bingo_game_sim.stats.df_tries, dark_mode=True)
    pb.plot_bingo_pie(bingo_game_sim.stats.df_num_bingo, detail="subplot_cols", dark_mode=True)
