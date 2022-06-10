import plotly.offline as pyo
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.optimize import curve_fit
from bingo_card import CARD_LENGTH


# ------------------------------------------------------------------------

# Function to model Gauss curve
def gauss_curve(x, a, x0, sigma):
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


# ------------------------------------------------------------------------


def plot_bingo_histo(df, detail_size="large", plot_offline=True):

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

    data1a = go.Bar(
        x=df.index,
        y=df['num_tries_rows'],
        name="Rows",
        marker_line=dict(width=1, color='black')
    )

    data1aa = go.Bar(
        x=df.index,
        y=df['num_tries_row0'],
        name="Row 1",
        marker_line=dict(width=1, color='black')
    )
    data1ab = go.Bar(
        x=df.index,
        y=df['num_tries_row1'],
        name="Row 2",
        marker_line=dict(width=1, color='black')
    )
    data1ac = go.Bar(
        x=df.index,
        y=df['num_tries_row2'],
        name="Row 3",
        marker_line=dict(width=1, color='black')
    )
    data1ad = go.Bar(
        x=df.index,
        y=df['num_tries_row3'],
        name="Row 4",
        marker_line=dict(width=1, color='black')
    )
    data1ae = go.Bar(
        x=df.index,
        y=df['num_tries_row4'],
        name="Row 5",
        marker_line=dict(width=1, color='black')
    )

    data1b = go.Bar(
        x=df.index,
        y=df['num_tries_cols'],
        name="Columns",
        marker_line=dict(width=1, color='black')
    )

    data1ba = go.Bar(
        x=df.index,
        y=df['num_tries_col0'],
        name="Column B",
        marker_line=dict(width=1, color='black')
    )
    data1bb = go.Bar(
        x=df.index,
        y=df['num_tries_col1'],
        name="Column I",
        marker_line=dict(width=1, color='black')
    )
    data1bc = go.Bar(
        x=df.index,
        y=df['num_tries_col2'],
        name="Column N",
        marker_line=dict(width=1, color='black')
    )
    data1bd = go.Bar(
        x=df.index,
        y=df['num_tries_col3'],
        name="Column G",
        marker_line=dict(width=1, color='black')
    )
    data1be = go.Bar(
        x=df.index,
        y=df['num_tries_col4'],
        name="Column O",
        marker_line=dict(width=1, color='black')
    )

    data1c = go.Bar(
        x=df.index,
        y=df['num_tries_diag'],
        name="Diagonals",
        marker_line=dict(width=1, color='black')
    )

    data1ca = go.Bar(
        x=df.index,
        y=df['num_tries_diag2'],
        name="Diagonal 2",
        marker_line=dict(width=1, color='black')
    )
    data1cb = go.Bar(
        x=df.index,
        y=df['num_tries_diag1'],
        name="Diagonal 1",
        marker_line=dict(width=1, color='black')
    )

    data1d = go.Bar(
        x=df.index,
        y=df['num_tries_corners'],
        name="Corners",
        marker_line=dict(width=1, color='black')
    )

    data_small = data1
    data_medium = [data1d, data1c, data1b, data1a]
    data_large = [data1d, data1cb, data1ca, data1be, data1bd, data1bc, data1bb, data1ba, data1ae, data1ad,
                          data1ac, data1ab, data1aa]

    data_selector = {"small": data_small, "medium": data_medium, "large": data_large}

    data2 = go.Scatter(
        x=df.index,
        y=y_gauss_curve,
        name="Gauss Fit",
        line=dict(width=4)
    )

    layout = go.Layout(
        title={
            'text': 'Number of bingo balls to win BINGO!<br><sup>Number of samples: <i>N={:,}</i></sup>'.format(
                num_simulations),
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
        },
        barmode="stack",
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

    fig = go.Figure(data=data_selector[detail_size], layout=layout)
    # fig.add_trace(data1)
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

    if plot_offline:
        pyo.plot(fig, filename='bingo_histo.html', include_mathjax='cdn')

    return fig

# ------------------------------------------------------------------------------------------------------------------


def plot_bingo_pie(num_simulations, df):
    bingo_ref = {0: 'B', 1: 'I', 2: 'N', 3: 'G', 4: 'O'}

    labels1 = []
    values1 = []

    for i in range(0, CARD_LENGTH):
        labels1.append(f"<b>Column {bingo_ref[i]}</b>")
        values1.append(df[f'num_bingo_col{i}'].values[0])

    labels1.append("<b>Corners</b>")
    values1.append(df['num_corners_bingo'].values[0])

    for i in [1, 2]:
        labels1.append(f"<b>Diagonal {i}</b>")
        values1.append(df[f'num_diag{i}_bingo'].values[0])

    for i in range(0, CARD_LENGTH):
        labels1.append(f"<b>Row {i + 1}</b>")
        values1.append(df[f'num_bingo_row{i}'].values[0])

    labels2 = []
    values2 = []

    labels2.append("<b>Columns</b>")
    values2.append(df['num_col_bingo'].values[0])

    labels2.append("<b>Corners</b>")
    values2.append(df['num_corners_bingo'].values[0])

    labels2.append("<b>Diagonals</b>")
    values2.append(df['num_diag_bingo'].values[0])

    labels2.append("<b>Rows</b>")
    values2.append(df['num_row_bingo'].values[0])

    # Border of annotation properties
    bordercolor = "black"
    borderwidth = 3
    borderpad = 5
    border_bgcolor = "white"

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

    fig.add_trace(go.Pie(labels=labels1, values=values1, name="Bingo Low Level Breakdown",
                         textfont=dict(family="Century Gothic")), 1, 1)
    fig.add_trace(go.Pie(labels=labels2, values=values2, name="Bingo High Level Breakdown",
                         textfont=dict(family="Century Gothic")), 1, 2)

    fig.update_traces(hovertemplate='%{value} samples<extra></extra>', textinfo='label+percent', textfont_size=20,
                      textposition="auto", hole=.4, direction='clockwise', sort=False,
                      marker=dict(line=dict(color='#000000', width=5)))

    fig.update_layout(
        title={'text': 'Detailed type of BINGO win!<br><sup>Number of samples: <i>N={:,}</i></sup>'.format(
            num_simulations),
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
        annotations=[dict(text='<b>Detailed Breakdown</b>', x=0.165, y=0.5, font_size=20, font_color="black",
                          font_family="Century Gothic", showarrow=False, borderwidth=borderwidth,
                          borderpad=borderpad, bgcolor=border_bgcolor, bordercolor=bordercolor),
                     dict(text='<b>High Level Breakdown</b>', x=0.845, y=0.5, font_size=20, font_color="black",
                          font_family="Century Gothic", showarrow=False, borderwidth=borderwidth,
                          borderpad=borderpad, bgcolor=border_bgcolor, bordercolor=bordercolor)])

    pyo.plot(fig, filename='bingo_pie.html')

    return fig
