import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output
from plot_bingo import plot_bingo_histo, plot_bingo_pie, FONT_FAMILY
from dash.exceptions import PreventUpdate

app = dash.Dash(assets_folder='assets')

# df = pd.read_csv(bingo_simulator_main.STATS_TRIES_FILENAME)
# df_pie = pd.read_csv(bingo_simulator_main.BINGO_STATS_FILENAME)
df = pd.read_csv("bingo_tries_1m.csv")
df_pie = pd.read_csv("bingo_stats_1m.csv")

num_simulations = df['num_bingo_tries'].sum()
MOBLILE_SMALL_LENGTH = 430

# Dash HTML layout
app.layout = html.Div([
    dcc.Location(id='url'), dcc.Store(id='viewport-container', data={}, storage_type='session'),
    html.Header(
        [html.H1("BINGO Simulator! Statistics on the BINGO game played {:,} times!".format(num_simulations))],
        style={'text-align': 'center', 'text-decoration': 'underline'}
    ),
    html.Div(
        [
            html.H2("Select Level of Detail for Histogram:", style={'display': 'inline-block', 'color': "red"}),
            dcc.RadioItems(["Small", "Medium", "Large"], inline=True,
                           id="radio_options", labelStyle={'margin-left': '15px'}, style={'display': 'inline-block'})
        ], style={'text-align': 'center'}
    ),
    dcc.Graph(id="graph1", mathjax='cdn', responsive='auto'),
    html.Hr(),
    dcc.Graph(id="graph2", responsive='auto'),
    html.Hr(),
    html.Footer('This page was created using python apps: Plotly and Dash - Content developed by Colin Huber',
                style={'text-align': 'center'})

], style={'fontFamily': FONT_FAMILY, 'fontSize': 18, 'color': 'white', 'border': '2px solid white',
          'background-color': '#3a3f44'})


# ------------------------------------------------------------------------

@app.callback(Output('graph1', 'figure'), [Input('radio_options', 'value')])
def update_histo(detail_size):
    """Updates the histogram based on the radio-button detail-size selected.
    :param: detail_size (str) The details put in the histogram plot as: 'small', 'medium', or 'large' (default)
    :return: (go.Figure) object to be dynamically updated"""

    if detail_size is None:
        raise PreventUpdate

    fig = plot_bingo_histo(df, detail_size, False)

    fig.update_layout(transition_duration=500)
    return fig


# ------------------------------------------------------------------------

@app.callback([Output('radio_options', 'value')], [Output('graph2', 'figure')],
              [Input('viewport-container', 'data')])
def get_viewport(screen_size):

    # TODO: Add a radio button for pie to switch between "High" and "Low".
    if screen_size['height'] < MOBLILE_SMALL_LENGTH:    # Landscape orientation
        pie = plot_bingo_pie(df_pie, False, "subplot_cols", 10)
    elif screen_size['width'] < MOBLILE_SMALL_LENGTH:   # Portrait orientation
        pie = plot_bingo_pie(df_pie, False, "subplot_rows", 10)
    else:
        pie = plot_bingo_pie(df_pie, False)

    # Return default graph detail size for the histogram plot, and the desired pie plot
    return "Large", pie


# ------------------------------------------------------------------------

"""A client callback to execute JS in a browser session to get the screen width and height.
Results are put in the Store() viewport-container data property."""
app.clientside_callback(
    """
    function(href) {
        var timestamp = new Date()
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

