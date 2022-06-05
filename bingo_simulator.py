import bingo_card as bc
import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit


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


# Function to model Gauss curve
def gauss_curve(x, a, x0, sigma):
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

# ------------------------------------------------------------------------


if __name__ == '__main__':
    bingo_game_sim = BingoSimulator(10000)

    bingo_game_sim.play_bingo(False)

    bingo_game_sim.stats.print_summary()

    df = pd.DataFrame(bingo_game_sim.stats.num_bingo_tries, columns=["num_bingo_tries"])

    # Preliminary stats and estimates
    N = bingo_game_sim.stats.num_simulations
    mean_estimate = 45.0
    sigma_estimate = 10.0
    p0 = [1., mean_estimate, sigma_estimate]

    # Get curve fit parameters
    curve_param, curve_covariance = curve_fit(gauss_curve, df.index, df['num_bingo_tries'], p0=p0)

    # Generate curve
    y_gauss_curve = gauss_curve(df.index, *curve_param)

    x_annotation_point = int(mean_estimate - sigma_estimate)
    y_annotation_point = y_gauss_curve[x_annotation_point]
    x_stats_annotation_point = 20
    y_stats_annotation_point = y_annotation_point

    x_arrow_vector = -350
    y_arrow_vector = -150

    data1 = go.Bar(
        x=df.index,
        y=df['num_bingo_tries'],
        name="Frequency"
    )

    data2 = go.Scatter(
        x=df.index,
        y=y_gauss_curve,
        name="Gauss Fit",
        texttemplate="Hello."
    )

    layout = go.Layout(
        title={'text': 'Number of tries to win BINGO!',
               'x': 0.5,
               'y': 0.95,
               'xanchor': 'center',
               'yanchor': 'top'},
        xaxis_title={'text': "Number of bingo balls"},
        yaxis_title={'text': "Frequency"},
        legend_title={'text': "Stats"},
        font=dict(
            family="Verdana",
            size=20,
            color="Black"
        ),
        paper_bgcolor='#F5F5F5',
        plot_bgcolor='#D6D6D6',
        spikedistance=1000,
        hoverdistance=100,
        hoverlabel=dict(
            bgcolor="grey",
            font_size=16,
            font=dict(color="White",
                      family="Verdana")

        ))
    fig = go.Figure(layout=layout)
    fig.add_trace(data1)
    fig.add_trace(data2)
    fig.update_traces(hovertemplate='%{x} bingo balls happened %{y:.0f} times<extra></extra>')
    fig.add_annotation(x=x_annotation_point, y=y_annotation_point, text=r"$\Large{\frac{1}{{\sigma \sqrt {2\pi } }}e^{{{ - ( {x - \mu } )^2 } / {2\sigma ^2 }}}}$", showarrow=True, arrowhead=2, arrowsize=2, arrowwidth=2, arrowcolor="red", ax=x_arrow_vector, ay=y_arrow_vector, bordercolor="black", borderwidth=3, borderpad=35, bgcolor="White")
    fig.add_annotation(x=x_stats_annotation_point, y=y_stats_annotation_point, text=r"$\mu={:.1f}, \sigma={:.1f}, N={}$".format(curve_param[1], curve_param[2], N), showarrow=False, bordercolor="black", borderpad=35, borderwidth=3, bgcolor="White")
    pyo.plot(fig, filename='bingo_histo.html', include_mathjax='cdn')
