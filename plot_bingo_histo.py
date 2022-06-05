import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit


# ------------------------------------------------------------------------

# Function to model Gauss curve
def gauss_curve(x, a, x0, sigma):
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

# ------------------------------------------------------------------------


def plot_bingo_histo(num_bingo_tries):

    df = pd.DataFrame(num_bingo_tries, columns=["num_bingo_tries"])

    # Preliminary stats and estimates
    num_simulations = sum(df['num_bingo_tries'])
    mean_estimate = 45.0  # 5x5 bingo card with 15 columns will have this approx mean
    sigma_estimate = 10.0  # Ditto
    p0 = [1., mean_estimate, sigma_estimate]

    # Get curve fit parameters
    curve_param, curve_covariance = curve_fit(gauss_curve, df.index, df['num_bingo_tries'], p0=p0)

    curve_a, curve_mean, curve_std = curve_param

    # Generate curve model
    y_gauss_curve = gauss_curve(df.index, *curve_param)

    # Annotation variables
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

    # LaTeX format to show the model equation and stat values
    model_equation = r"$\Large{\frac{1}{{\sigma \sqrt {2\pi } }}e^{{{ - ( {x - \mu } )^2 } / {2\sigma ^2 }}}}$"
    model_results = r"$a={:.1f}, \mu={:.1f}, \sigma={:.1f}, N={}$".format(curve_a, curve_mean, curve_std,
                                                                          num_simulations)
    # Arrow properties
    arrowhead = 2
    arrowsize = 2
    arrowwidth = 2
    arrowcolor = "red"

    # Border of annotation properties
    bordercolor = "black"
    borderwidth = 3
    borderpad = 1
    border_bgcolor = "white"

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
