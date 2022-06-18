"""The main app to run the dash server to display the results of the bingo simulation with interactive features."""

import dash
from dash import dcc
from dash import html
import dash_daq as daq
import pandas as pd
from dash.dependencies import Input, Output
from plot_bingo import plot_bingo_histo, plot_bingo_pie, FONT_FAMILY
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, assets_folder='assets')

server = app.server

# df = pd.read_csv(bingo_simulator_main.STATS_TRIES_FILENAME)
# df_pie = pd.read_csv(bingo_simulator_main.BINGO_STATS_FILENAME)
df = pd.read_csv("bingo_tries_1m.csv")
df_pie = pd.read_csv("bingo_stats_1m.csv")

num_simulations = df['num_bingo_tries'].sum()

# Dash HTML layout
app.layout = html.Div([
    dcc.Location(id='url'), dcc.Store(id='viewport-container', data={}, storage_type='session'),
    html.Header(
        [html.H1("BINGO Simulator! Statistics on the BINGO game played {:,} times!".format(num_simulations))],
        style={'text-align': 'center', 'text-decoration': 'underline'}
    ),
    html.Div([daq.ToggleSwitch(id='dark-mode-switch', label=dict(label='View Page in Dark Mode:',
                                                                 style={'font-size': '20px'}),
                               value=True, size=50, color='skyblue')]),
    html.Div(
        [
            html.H2("Select Level of Detail for Histogram:", style={'display': 'inline-block', 'color': "red"}),
            dcc.RadioItems(["Small", "Medium", "Large"], inline=True,
                           id="radio_options", value="Large", labelStyle={'margin-left': '15px'},
                           style={'display': 'inline-block'})
        ], style={'text-align': 'center'}
    ),
    dcc.Graph(id="graph1", mathjax='cdn', responsive='auto'),
    html.Hr(),
    html.Div([
        html.H2("Select Level of Detail for Pie:", style={'display': 'inline-block', 'color': "red"}),
        dcc.RadioItems(["Small", "Large", "Separate"], id="radio_options_pie", value="Large", inline=True,
                       labelStyle={'margin-left': '15px'}, style={'display': 'inline-block'})],
        style={'text-align': 'center'}),
    dcc.Graph(id="graph2", responsive='auto'),
    html.Hr(),
    html.Footer(
        [html.Div(['This page was created using python apps: Plotly and Dash - Content developed by Colin Huber'],
                  style={'font-size': '30px'}),
         html.Div(['Contact:'], style={'text-decoration': 'underline', 'color': 'skyblue', 'font-size': '30px'}),
         html.A([html.Img(src='assets/fb.png')], href='https://www.facebook.com/cbhuber/'),
         html.A([html.Img(src='assets/li.png', style={'margin-left': '10px'})],
                href='https://www.linkedin.com/in/cbhuber/')],
        style={'text-align': 'center'},
    ),
    html.Div(['Ⓒ Colin Huber 2022, Distributed under the MIT License'], style={'text-align': 'center'})

], id='main')


# ------------------------------------------------------------------------


def get_pie_chart(screen_size, dark_mode):
    """Returns a pie chart based on the layout desired and current viewport (screen size).
    :param: screen_size (dict) Dictionary of 'height' and 'width' the screen size
    :param: dark_mode (bool) If dark mode plotting is done (True), light mode plotting (False)
    :return: (go.Figure) object of the pie chart"""

    mobile_small_length = 430

    if screen_size['height'] < mobile_small_length:  # Landscape orientation
        fig = plot_bingo_pie(df_pie, False, "subplot_cols", 10, dark_mode)
    elif screen_size['width'] < mobile_small_length:  # Portrait orientation
        fig = plot_bingo_pie(df_pie, False, "subplot_rows", 10, dark_mode)
    else:
        fig = plot_bingo_pie(df_pie, False, dark_mode=dark_mode)

    return fig


# ------------------------------------------------------------------------

@app.callback(Output('main', 'style'), [Input('dark-mode-switch', 'value')])
def update_layout(dark_mode):
    """CALLBACK: Updates the histogram based on the radio-button detail-size selected.
    TRIGGER: Upon page loading and when selecting the toggle for dark mode
    :param: dark_mode (bool) If dark mode plotting is done (True), light mode plotting (False)
    :return: Global style layout as dark or light theme"""

    color_mode = {'font_color': ('black', 'white'),
                  'bg_color': ('white', '#3a3f44')}

    return {'fontFamily': FONT_FAMILY, 'fontSize': 18, 'color': color_mode['font_color'][dark_mode],
            'border': '4px solid skyblue', 'background-color': color_mode['bg_color'][dark_mode]}


# ------------------------------------------------------------------------

@app.callback(Output('graph1', 'figure'), [Input('radio_options', 'value'), Input('dark-mode-switch', 'value')])
def update_histo(detail_size, dark_mode):
    """CALLBACK: Updates the histogram based on the radio-button detail-size selected.
    TRIGGER: Upon page load, toggling the dark mode switch, and when selecting the radio options for the histogram plot.
    :param: detail_size (str) The details put in the histogram plot as: 'small', 'medium', or 'large' (default)
    :param: dark_mode (bool) Whether the plot is done in dark mode or not
    :return: (go.Figure) object to be dynamically updated"""

    if detail_size is None:
        raise PreventUpdate

    fig = plot_bingo_histo(df, detail_size, False, dark_mode)

    fig.update_layout(transition_duration=500)
    return fig


# ------------------------------------------------------------------------

@app.callback(Output('graph2', 'figure'), [Input('radio_options_pie', 'value'), Input('viewport-container', 'data'),
                                           Input('dark-mode-switch', 'value')])
def update_pie(detail_size, screen_size, dark_mode):
    """CALLBACK: Updates the pie chart based on the radio-button detail-size selected.
    TRIGGER: Upon page load, toggling the dark mode switch, and when selecting the radio options for the pie plot.
    :param: detail_size (str) The details put in the pie plot as: 'small' or 'large' (default)
    :param: screen_size (dict) Dictionary of 'height' and 'width' the screen size
    :param: dark_mode (bool) If dark mode plotting is done (True), light mode plotting (False)
    :return: (go.Figure) object to be dynamically updated"""

    if detail_size is None:
        raise PreventUpdate

    # Two pie charts
    if detail_size == "Separate":
        fig = get_pie_chart(screen_size, dark_mode=dark_mode)

    # Single pie chart
    else:
        fig = plot_bingo_pie(df_pie, False, detail_size.lower(), dark_mode=dark_mode)

    fig.update_layout(transition_duration=1000)

    return fig


# ------------------------------------------------------------------------

"""CALLBACK: A client callback to execute JS in a browser session to get the screen width and height.
TRIGGER: Upon page loading.
Results are put in the Store() viewport-container data property."""
app.clientside_callback(
    """
    function(href) {
        var w = screen.width;
        var h = screen.height;
        return {'height': h, 'width': w};
    }
    """,
    Output('viewport-container', 'data'),
    Input('url', 'href')
)

if __name__ == '__main__':
    app.run_server()
