import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output
from bingo_simulator import bingo_simulator_main
from plot_bingo import plot_bingo_histo

app = dash.Dash()

# df = pd.read_csv(bingo_simulator_main.STATS_TRIES_FILENAME)
df = pd.read_csv("bingo_stats_1m.csv")

# Dash HTML layout
app.layout = html.Div([
    dcc.RadioItems(["small", "medium", "large"], value="large", inline=True, id="radio_options"),
    dcc.Graph(id="graph", style={'height': '95vh'}, mathjax='cdn')
])


@app.callback(Output('graph', 'figure'), [Input('radio_options', 'value')])
def update_histo(detail_size):
    fig = plot_bingo_histo(df, detail_size, False)
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.run_server()
