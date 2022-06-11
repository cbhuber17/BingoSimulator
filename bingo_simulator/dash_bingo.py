import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output
from plot_bingo import plot_bingo_histo, plot_bingo_pie

app = dash.Dash()

# df = pd.read_csv(bingo_simulator_main.STATS_TRIES_FILENAME)
# df_pie = pd.read_csv(bingo_simulator_main.BINGO_STATS_FILENAME)
df = pd.read_csv("bingo_tries_1m.csv")
df_pie = pd.read_csv("bingo_stats.csv")

# Dash HTML layout
app.layout = html.Div([
    html.Div(
        [html.H1("BINGO Simulator! Statistics on the BINGO game played 1,000,000 times!")],
        style={'text-align': 'center', 'text-decoration': 'underline'}
    ),
    html.Div(
        [
            html.H2("Select Plot Details:", style={'display': 'inline-block'}),
            dcc.RadioItems(["Histo-small", "Histo-medium", "Histo-large"], value="Histo-large", inline=True,
                           id="radio_options", style={'display': 'inline-block'})
        ], style={'text-align': 'center'}
    ),

    dcc.Graph(id="graph1", style={'height': '95vh'}, mathjax='cdn'),
    html.Hr(),
    dcc.Graph(id="graph2", style={'height': '95vh'}, figure=plot_bingo_pie(df_pie, False)),
    html.Hr(),
    html.Footer('This page was created using python apps: Plotly and Dash - Content developed by Colin Huber',
                style={'text-align': 'center'})

], style={'fontFamily': 'MV Boli', 'fontSize': 18, 'color': 'white', 'border': '2px solid white',
          'background-color': '#3a3f44'})


@app.callback(Output('graph1', 'figure'), [Input('radio_options', 'value')])
def update_histo(detail_size):

    fig = plot_bingo_histo(df, detail_size, False)

    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.run_server()
