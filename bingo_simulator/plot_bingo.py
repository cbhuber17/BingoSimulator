"""Functions to plot the statistics from running the BINGO simulator."""

import plotly.offline as pyo
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.optimize import curve_fit
from bingo_card import CARD_LENGTH

FONT_FAMILY = "MV Boli"
FONT_FAMILY2 = "Century Gothic"

HTML_HISTO_FILE = "bingo_histo.html"
HTML_PIE_FILE = "bingo_pie.html"


# ------------------------------------------------------------------------

# Function to model Gauss curve
def gauss_curve(x, a, x0, sigma):
    """Gauss curve model to represent the BINGO histogram.
    :param: x (int) The index of the data frame (x-coordinate, number of bingo balls called)
    :param: a (float) The peak y-value of the histogram
    :param: x0 (float) The x-coordinate mean of the histogram
    :param: sigma (float) The 1-standard deviation of the bell curve
    :return: (float), the y-value of the gauss-curve: a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))"""
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


# ------------------------------------------------------------------------

def get_bar_object(df, df_name, name):
    """Returns a bar object to be plotted.
    :param: df (pd.DataFrame) A data frame of bingo stats
    :param: df_name (str) The key to access a specific column in the df to be plotted
    :param: name (str) The name of the series to be put on the legend in the plot
    :return: (go.Bar) object"""
    return go.Bar(x=df.index, y=df[df_name], name=name, marker_line=dict(width=1, color='white'))


# ------------------------------------------------------------------------


def plot_bingo_histo(df, detail_size="Large", plot_offline=True):
    """Plots the BINGO histogram.
    :param: df (pandas.df) DataFrame containing number of tries for each BINGO win
    :param: detail_size (str) The details put in the histogram plot as: 'small', 'medium', or 'large' (default)
    :param: plot_offline (bool) If an offline plot is to be generated (default: True)
    :return: (go.Figure) object"""

    # Preliminary stats and estimates are required to generate a bell curve
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

    # Get bar graph (stacked) objects
    data_total = get_bar_object(df, 'num_bingo_tries', 'frequency')

    # Done in this order for proper legend presentation
    data_rows = get_bar_object(df, 'num_tries_rows', 'Rows')
    data_row0 = get_bar_object(df, 'num_tries_row0', 'Row 1')
    data_row1 = get_bar_object(df, 'num_tries_row1', 'Row 2')
    data_row2 = get_bar_object(df, 'num_tries_row2', 'Row 3')
    data_row3 = get_bar_object(df, 'num_tries_row3', 'Row 4')
    data_row4 = get_bar_object(df, 'num_tries_row4', 'Row 5')

    data_cols = get_bar_object(df, 'num_tries_cols', 'Columns')
    data_col0 = get_bar_object(df, 'num_tries_col0', 'Column B')
    data_col1 = get_bar_object(df, 'num_tries_col1', 'Column I')
    data_col2 = get_bar_object(df, 'num_tries_col2', 'Column N')
    data_col3 = get_bar_object(df, 'num_tries_col3', 'Column G')
    data_col4 = get_bar_object(df, 'num_tries_col4', 'Column O')

    data_diag = get_bar_object(df, 'num_tries_diag', 'Diagonals')
    data_diag1 = get_bar_object(df, 'num_tries_diag1', 'Diagonal 1')
    data_diag2 = get_bar_object(df, 'num_tries_diag2', 'Diagonal 2')

    data_corners = get_bar_object(df, 'num_tries_corners', 'Corners')

    # Small data is simply num BINGO wins
    # Medium data is details of BINGO wins (rows, cols, diagonals, corners), but not specific like row0, col1, etc.
    # High data is all details of BINGO wins (which row, col, diag. etc.) got a BINGO!
    data_small = data_total
    data_medium = [data_corners, data_diag, data_cols, data_rows]
    data_large = [data_corners, data_diag2, data_diag1, data_col4, data_col3, data_col2, data_col1, data_col0,
                  data_row4, data_row3, data_row2, data_row1, data_row0]

    # Dictionary for data selector based on input to this function
    data_selector = {"Small": data_small, "Medium": data_medium, "Large": data_large}

    # Gauss best-fit curve
    data2 = go.Scatter(x=df.index, y=y_gauss_curve, name="Gauss Fit", line=dict(width=4, color='red'))

    layout = go.Layout(
        title={
            'text': 'Number of bingo balls to win BINGO!<br><sup>Number of samples: <i>N={:,}</i></sup>'.format(
                num_simulations),
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(color='orange')
        },
        barmode="stack",
        xaxis_title={'text': "Number of bingo balls"},
        yaxis_title={'text': "Frequency"},
        legend_title={'text': "Stats"},
        font=dict(
            family=FONT_FAMILY,
            size=30,
            color="yellow"
        ),
        paper_bgcolor='black',
        plot_bgcolor='black',
        spikedistance=1000,
        hoverdistance=100,
        hoverlabel=dict(
            font_size=16,
            font=dict(color="White",
                      family=FONT_FAMILY)

        ))

    # LaTeX format to show the model equation and stat values
    model_equation = r"$\normalsize{\alpha * e^{{{ - ( {x - \mu } )^2 } / {2\sigma ^2 }}}}$"
    model_results = r"$\alpha={:.0f}\\\mu={:.1f}\\\sigma={:.1f}$".format(curve_a, curve_mean, curve_std)
    equation_to_show = r'$\displaylines{' + model_equation[1:-1] + r"\\" + model_results[1:-1] + r'}$'

    # Arrow annotation properties
    arrowhead = 2
    arrowsize = 2
    arrowwidth = 2
    arrowcolor = "red"
    x_arrow_vector = -200
    y_arrow_vector = -50

    # Annotation variables
    x_annotation_point = int(mean_estimate - sigma_estimate)
    y_annotation_point = y_gauss_curve[x_annotation_point]

    # Border of annotation properties
    bordercolor = "red"
    borderwidth = 3
    borderpad = 35
    border_bgcolor = "white"

    # Create figure
    fig = go.Figure(data=data_selector[detail_size], layout=layout)
    fig.add_trace(data2)
    fig.update_traces(hovertemplate='%{x} bingo balls happened %{y:.0f} times<extra></extra>')

    # Arrow annotation of the equation of the curve
    fig.add_annotation(x=x_annotation_point, y=y_annotation_point, text=equation_to_show, showarrow=True,
                       arrowhead=arrowhead, arrowsize=arrowsize, arrowwidth=arrowwidth, arrowcolor=arrowcolor,
                       bordercolor=bordercolor, borderpad=borderpad, borderwidth=borderwidth, bgcolor=border_bgcolor,
                       ax=x_arrow_vector, ay=y_arrow_vector, font=dict(color="navy"))

    if plot_offline:
        pyo.plot(fig, filename=HTML_HISTO_FILE, include_mathjax='cdn', config={'responsive': True})

    return fig


# ------------------------------------------------------------------------------------------------------------------

def set_labels_and_values(df, label, value, label_str, value_key):
    """Sets the labels and values for pie chart plotting.
    :param: df (pandas.df) DataFrame containing number of tries for each BINGO win
    :param: label (list) a list of strings labelling each piece of the pie chart
    :param: value (list) a list of ints for the value for each piece of the pie chart
    :param: label_str (str) the actual label to append to the label list
    :param: value_key (str) the dict key for the df to retrieve the value to put in the values list
    :return: None
    """
    label.append(f"<b>{label_str}</b>")
    value.append(df[value_key].values[0])


# ------------------------------------------------------------------------------------------------------------------

def get_pie_annotation_dict(text, x, y, font_size):
    """Returns a dictionary of annotations to use with the pie chart.
    :param: text (str) Text to annotate with
    :param: x (int) The x-coordinate of the annotation on the plot
    :param: y (int) The y-coordinate of the annotation on the plot
    :param: font_size (int) The size of the font in the annotation
    :return: (dict) a dictionary filled with annotation properties that is common among the pie charts."""

    # Border of annotation properties
    bordercolor = "black"
    borderwidth = 3
    borderpad = 5
    border_bgcolor = "white"

    return dict(text=f'<b>{text}</b>', x=x, y=y, font_size=font_size, font_color="black",
                font_family=FONT_FAMILY2, showarrow=False, borderwidth=borderwidth,
                borderpad=borderpad, bgcolor=border_bgcolor, bordercolor=bordercolor)


# ------------------------------------------------------------------------------------------------------------------

def get_pie_fig_and_annotation(detail, x1, y1, x2, y2, font_size):
    """Returns the fig and annotation objects to use in the pie charts.
    :param: detail (str) either as "subplot_cols" or "subplot_rows"
    :param: x1 (int) The x-coordinate of the first annotation on the plot
    :param: y1 (int) The y-coordinate of the first annotation on the plot
    :param: x2 (int) The x-coordinate of the second annotation on the plot
    :param: y2 (int) The y-coordinate of the second annotation on the plot
    :param: font_size (int) The size of the font in the annotation
    :return: fig (go.Figure) and annotation (dict)"""

    spec = {'type': 'domain'}

    if detail == "subplot_cols":
        fig = make_subplots(rows=1, cols=2, specs=[[spec, spec]])

    else:
        fig = make_subplots(rows=2, cols=1, specs=[[spec], [spec]])

    annotations = [get_pie_annotation_dict("Detailed<br>Breakdown", x1, y1, font_size),
                   get_pie_annotation_dict("High Level<br>Breakdown", x2, y2, font_size)]

    return fig, annotations


# ------------------------------------------------------------------------------------------------------------------

def add_trace(fig, label, value, detail, row, col):
    """Adds a trace to the figure.
    :param: fig (go.Figure) The figure to be updated
    :param: label (str) as "High" or "Low'
    :param: row (int) as 1 or 2 (location in subplot)
    :param: col (int) as 1 or 2 (location in subplot)
    :return: None (fig is automatically updated by reference)"""

    fig.add_trace(go.Pie(labels=label, values=value, name=f"Bingo {detail} Level Breakdown",
                         textfont=dict(family=FONT_FAMILY2)), row, col)


# ------------------------------------------------------------------------------------------------------------------

def plot_bingo_pie(df, plot_offline=True, detail="subplot_cols", font_size=20):
    """Plots the BINGO pie charts.
    :param: df (pandas.df) DataFrame containing number of tries for each BINGO win
    :param: plot_offline (bool) If an offline plot is to be generated (default: True)
    :param: detail (str) One of the following: "subplot_rows", "subplot_cols", "high", "low" (default: "subplot_cols")
            - "subplot_rows" - Plots both the high detail and low detail pie charts in a 2x1 subplot
            - "subplot_cols" - Plots both the high detail and low detail pie chars in a 1x2 subplot
            - "large" - Plots a single high detail pie chart
            - "small" - Plots a single low detail pie chart
    :return: (go.Figure) object"""

    # Total number of simulations
    num_simulations = int(df['num_line_bingo'].values + df['num_diag_bingo'].values + df['num_corners_bingo'].values)

    bingo_ref = {0: 'B', 1: 'I', 2: 'N', 3: 'G', 4: 'O'}

    # Labels and values for first pie chart
    labels1 = []
    values1 = []

    # Done in this order for proper legend presentation
    for i in range(0, CARD_LENGTH):
        set_labels_and_values(df, labels1, values1, f"Column {bingo_ref[i]}", f"num_bingo_col{i}")

    set_labels_and_values(df, labels1, values1, "Corners", "num_corners_bingo")

    for i in [1, 2]:
        set_labels_and_values(df, labels1, values1, f"Diagonal {i}", f"num_diag{i}_bingo")

    for i in range(0, CARD_LENGTH):
        set_labels_and_values(df, labels1, values1, f"Row {i + 1}", f"num_bingo_row{i}")

    # Labels and values for second pie chart
    labels2 = []
    values2 = []

    set_labels_and_values(df, labels2, values2, "Columns", "num_col_bingo")
    set_labels_and_values(df, labels2, values2, "Corners", "num_corners_bingo")
    set_labels_and_values(df, labels2, values2, "Diagonals", "num_diag_bingo")
    set_labels_and_values(df, labels2, values2, "Rows", "num_row_bingo")

    # 2 pie charts in subplots, as rows or cols, or single plot as high or low details
    if detail == "subplot_cols":
        fig, annotations = get_pie_fig_and_annotation(detail, 0.18, 0.5, 0.82, 0.5, font_size)

    elif detail == "subplot_rows":
        fig, annotations = get_pie_fig_and_annotation(detail, 0.5, 0.82, 0.5, 0.18, font_size)

    elif detail == "large":
        fig = go.Figure(data=[go.Pie(labels=labels1, values=values1, textinfo='label+percent')])
        annotations = [get_pie_annotation_dict("Detailed<br>Breakdown", 0.5, 0.5, font_size)]

    else:
        fig = go.Figure(data=[go.Pie(labels=labels2, values=values2, textinfo='label+percent')])
        annotations = [get_pie_annotation_dict("High Level<br>Breakdown", 0.5, 0.5, font_size)]

    if detail == "subplot_cols" or detail == "subplot_rows":
        add_trace(fig, labels1, values1, "Low", 1, 1)

        if detail == "subplot_cols":
            add_trace(fig, labels2, values2, "High", 1, 2)

        else:
            add_trace(fig, labels2, values2, "High", 2, 1)

    fig.update_traces(hovertemplate='%{value} samples<extra></extra>', textinfo='label+percent', textfont_size=20,
                      textposition="auto", hole=.4, direction='clockwise', sort=False,
                      marker=dict(line=dict(color='#000000', width=5)))

    # Layout
    fig.update_layout(
        title={'text': 'Detailed type of BINGO win!<br><sup>Number of samples: <i>N={:,}</i></sup>'.format(
            num_simulations),
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top'}, paper_bgcolor="grey",
        font=dict(
            family=FONT_FAMILY2,
            size=40,
            color="white"
        ),
        showlegend=False,
        hoverlabel=dict(
            font_size=30,
            bordercolor="black",
            font=dict(family=FONT_FAMILY2, color="White")
        ),
        annotations=annotations,
        margin=dict(t=170))

    if plot_offline:
        pyo.plot(fig, filename=HTML_PIE_FILE)

    return fig
