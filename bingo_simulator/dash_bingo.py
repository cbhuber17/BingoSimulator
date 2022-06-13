import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output
from plot_bingo import plot_bingo_histo, plot_bingo_pie, FONT_FAMILY

app = dash.Dash(assets_folder='assets')

# df = pd.read_csv(bingo_simulator_main.STATS_TRIES_FILENAME)
# df_pie = pd.read_csv(bingo_simulator_main.BINGO_STATS_FILENAME)
df = pd.read_csv("bingo_tries_1m.csv")
df_pie = pd.read_csv("bingo_stats_1m.csv")

viewport = {}



# layout = [
#     html.Div(id="size"),  # Set style so that it is hidden!  # TODO: Update CSS!
#     dcc.Location(id="url")
# ]

app.layout = html.Div([
    dcc.Location(id='url'),
    dcc.Store(id='viewport-container', data={}, storage_type='session'),
    html.Div(id='temp')
])


# Dash HTML layout
# app.layout = html.Div([
#     # dcc.Location(id='url'), dcc.Store(id='viewport-container', data={}, storage_type='session'), html.Div(id='temp'),
#     html.Header(
#         [html.H1("BINGO Simulator! Statistics on the BINGO game played 1,000,000 times!")],
#         style={'text-align': 'center', 'text-decoration': 'underline'}
#     ),
#     html.Div(
#         [
#             html.H2("Select Level of Detail for Histogram:", style={'display': 'inline-block', 'color': "red"}),
#             dcc.RadioItems(["Small", "Medium", "Large"], value="Large", inline=True,
#                            id="radio_options", labelStyle={'margin-left': '15px'}, style={'display': 'inline-block'})
#         ], style={'text-align': 'center'}
#     ),
#     dcc.Graph(id="graph1", mathjax='cdn', responsive='auto'),
#     html.Hr(),
#     dcc.Graph(id="graph2", responsive='auto', figure=plot_bingo_pie(df_pie, False)),
#     html.Hr(),
#     html.Footer('This page was created using python apps: Plotly and Dash - Content developed by Colin Huber',
#                 style={'text-align': 'center'})
#
# ], style={'fontFamily': FONT_FAMILY, 'fontSize': 18, 'color': 'white', 'border': '2px solid white',
#           'background-color': '#3a3f44'})


# ------------------------------------------------------------------------

@app.callback(Output('temp', 'children'), [Input('viewport-container', 'data')])
def get_viewport(data):
    print(data)
    global viewport
    viewport = data
    return data


# ------------------------------------------------------------------------

@app.callback(Output('graph1', 'figure'), [Input('radio_options', 'value')])
def update_histo(detail_size):
    """Updates the histogram based on the radio-button detail-size selected.
    :param: detail_size (str) The details put in the histogram plot as: 'small', 'medium', or 'large' (default)
    :return: (go.Figure) object to be dynamically updated"""

    fig = plot_bingo_histo(df, detail_size, False)

    fig.update_layout(transition_duration=500)
    return fig


# ------------------------------------------------------------------------


app.clientside_callback(
    """
    function(href) {
        var w = window.innerWidth;
        var h = window.innerHeight;
        return {'height': h, 'width': w};
    }
    """,
    Output('viewport-container', 'data'),
    Input('url', 'href')
)

if __name__ == '__main__':
    app.run_server()
    print(viewport)