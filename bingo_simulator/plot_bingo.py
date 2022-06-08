import plotly.offline as pyo
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from bingo_card import CARD_LENGTH


# ------------------------------------------------------------------------

# Function to model Gauss curve
def gauss_curve(x, a, x0, sigma):
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


# ------------------------------------------------------------------------


def plot_bingo_histo(num_bingo_tries):
    df = pd.DataFrame(num_bingo_tries, columns=["num_bingo_tries"])

    # Preliminary stats and estimates
    num_simulations = sum(df['num_bingo_tries'])
    peak_estimate = max(df['num_bingo_tries'])
    mean_estimate = 45.0  # 5x5 bingo card with 15 columns will have this approx mean
    sigma_estimate = 10.0  # Ditto for the standard deviation
    p0 = [peak_estimate, mean_estimate, sigma_estimate]

    # Get curve fit parameters
    curve_param, curve_covariance = curve_fit(gauss_curve, df.index, df['num_bingo_tries'], p0=p0)

    curve_a, curve_mean, curve_std = curve_param

    # Generate curve model
    y_gauss_curve = gauss_curve(df.index, *curve_param)

    data1 = go.Bar(
        x=df.index,
        y=df['num_bingo_tries'],
        name="Frequency",
        marker_line=dict(width=1, color='black')
    )

    data2 = go.Scatter(
        x=df.index,
        y=y_gauss_curve,
        name="Gauss Fit",
        line=dict(width=4)
    )

    layout = go.Layout(
        title={
            'text': 'Number of bingo balls to win BINGO!<br><sup>Number of samples: <i>N={:,}</i></sup>'.format(num_simulations),
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
        },
        xaxis_title={'text': "Number of bingo balls"},
        yaxis_title={'text': "Frequency"},
        legend_title={'text': "Stats"},
        font=dict(
            family="MV Boli",
            size=30,
            color="Black"
        ),
        paper_bgcolor='#F5F5F5',
        plot_bgcolor='#D6D6D6',
        spikedistance=1000,
        hoverdistance=100,
        hoverlabel=dict(
            font_size=16,
            font=dict(color="White",
                      family="Verdana")

        ))

    # LaTeX format to show the model equation and stat values
    model_equation = r"$\Large{\frac{1}{{\sigma \sqrt {2\pi } }}e^{{{ - ( {x - \mu } )^2 } / {2\sigma ^2 }}}}$"
    model_results = r"$a={:.1f}, \mu={:.1f}, \sigma={:.1f}$".format(curve_a, curve_mean, curve_std)

    # Arrow properties
    arrowhead = 2
    arrowsize = 2
    arrowwidth = 2
    arrowcolor = "red"

    # Border of annotation properties
    bordercolor = "black"
    borderwidth = 3
    borderpad = 35
    border_bgcolor = "white"

    # Annotation variables
    x_annotation_point = int(mean_estimate - sigma_estimate)
    y_annotation_point = y_gauss_curve[x_annotation_point]
    x_stats_annotation_point = 17
    y_stats_annotation_point = y_annotation_point

    x_arrow_vector = -350
    y_arrow_vector = -150

    # TODO: Figure this out for LaTeX, this may be a plotly bug
    box_width = 170
    box_height = 100

    fig = go.Figure(layout=layout)
    fig.add_trace(data1)
    fig.add_trace(data2)
    fig.update_traces(hovertemplate='%{x} bingo balls happened %{y:.0f} times<extra></extra>')

    # Arrow annotation of the equation of the curve
    fig.add_annotation(x=x_annotation_point, y=y_annotation_point, text=model_equation, showarrow=True,
                       arrowhead=arrowhead, arrowsize=arrowsize, arrowwidth=arrowwidth, arrowcolor=arrowcolor,
                       ax=x_arrow_vector, ay=y_arrow_vector, bordercolor=bordercolor, borderwidth=borderwidth,
                       borderpad=borderpad, bgcolor=border_bgcolor)

    # Annotation of the curve parameters
    fig.add_annotation(x=x_stats_annotation_point, y=y_stats_annotation_point, text=model_results, showarrow=False,
                       bordercolor=bordercolor, borderpad=borderpad, borderwidth=borderwidth, bgcolor=border_bgcolor,
                       align="left", valign="top")

    pyo.plot(fig, filename='bingo_histo.html', include_mathjax='cdn')


def plot_bingo_pie(stats):
    bingo_ref = {0: 'B', 1: 'I', 2: 'N', 3: 'G', 4: 'O'}

    labels1 = []
    values1 = []

    for i in range(0, CARD_LENGTH):
        labels1.append(f"<b>Column {bingo_ref[i]}</b>")
        values1.append(stats.num_line_bingo[1][i])

    labels1.append("<b>Corners</b>")
    values1.append(stats.num_corners_bingo)

    for i in range(0, 2):
        labels1.append(f"<b>Diagonal {i + 1}</b>")
        values1.append(stats.num_diag_bingo[i])

    for i in range(0, CARD_LENGTH):
        labels1.append(f"<b>Row {i}</b>")
        values1.append(stats.num_line_bingo[0][i])

    labels2 = []
    values2 = []

    labels2.append("<b>Columns</b>")
    values2.append(sum(stats.num_line_bingo[1]))

    labels2.append("<b>Corners</b>")
    values2.append(stats.num_corners_bingo)

    labels2.append("<b>Diagonals</b>")
    values2.append(sum(stats.num_diag_bingo))

    labels2.append("<b>Rows</b>")
    values2.append(sum(stats.num_line_bingo[0]))

    # Border of annotation properties
    bordercolor = "black"
    borderwidth = 3
    borderpad = 5
    border_bgcolor = "white"

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

    fig.add_trace(go.Pie(labels=labels1, values=values1, name="Bingo Low Level Breakdown", textfont=dict(family="Century Gothic")), 1, 1)
    fig.add_trace(go.Pie(labels=labels2, values=values2, name="Bingo High Level Breakdown", textfont=dict(family="Century Gothic")), 1, 2)

    fig.update_traces(hovertemplate='%{value} samples<extra></extra>', textinfo='label+percent', textfont_size=20,
                      textposition="auto", hole=.4, direction='clockwise', sort=False,
                      marker=dict(line=dict(color='#000000', width=5)))

    fig.update_layout(
        title={'text': 'Detailed type of BINGO win!<br><sup>Number of samples: <i>N={:,}</i></sup>'.format(stats.num_simulations),
               'x': 0.5,
               'y': 0.95,
               'xanchor': 'center',
               'yanchor': 'top'}, paper_bgcolor="grey",
        font=dict(
            family="MV Boli",
            size=40,
            color="white"
        ),
        showlegend=False,
        hoverlabel=dict(
            font_size=30,
            bordercolor="black",
            font=dict(color="White")
        ),
        annotations=[dict(text='<b>Detailed Breakdown</b>', x=0.165, y=0.5, font_size=20, font_color="black", font_family="Century Gothic", showarrow=False, borderwidth=borderwidth,
                       borderpad=borderpad, bgcolor=border_bgcolor, bordercolor=bordercolor),
                     dict(text='<b>High Level Breakdown</b>', x=0.845, y=0.5, font_size=20, font_color="black", font_family="Century Gothic", showarrow=False, borderwidth=borderwidth,
                       borderpad=borderpad, bgcolor=border_bgcolor, bordercolor=bordercolor)])

    pyo.plot(fig, filename='bingo_pie.html')
