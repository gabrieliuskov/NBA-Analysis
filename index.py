import dash_bootstrap_components as dbc

from app import *
from layout import *
from data import *

app.layout = dbc.Container(
    [
        dcc.Location(id="url"),
        dcc.Store(id="home-data"),
        dcc.Store(id="away-data"),
        dcc.Store(id="vs-home-team"),
        dcc.Store(id="vs-away-team"),
        navbar, 
        team_filter, 
        dashboard
        ], 
    fluid=True, class_name="dbc")

if __name__ == "__main__":
    app.run_server(debug=True, port=8051)