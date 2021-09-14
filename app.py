import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

from model_setup import *

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Ethiopia Livestock SD model"
server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🐮", className="header-emoji"),
                html.H1(
                    children="[DEMO] Ethiopia Livestock Model", className="header-title"
                ),
                html.P(
                    children=[
                        "Model the behaviour of the Ethiopia livestock system "
                        "using a system dynamics model.",
                        html.Br(), html.Br(),
                        "NOTE: this model is purely a demo, and not intended for "
                        "actual use. It does not use any real-world data."
                    ],
                    className="header-description"
                ),
            ],
            className="header"
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Livestock health", className="menu-title"),
                        dcc.Slider(
                            id="input-var1",
                            min=0.0,
                            max=1.0,
                            step=0.05,
                            value=1.0,
                            marks={
                                0: "0",
                                1: "1"
                            },
                            # className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Livestock fertility (births per year)", className="menu-title"),
                        dcc.Slider(
                            id="input-var2",
                            min=0.0,
                            max=0.5,
                            step=0.01,
                            value=0.3,
                            marks={
                                0: "0",
                                0.5: "0.5"
                            },
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="output-chart1", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="output-chart2", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [
        Output("output-chart1", "figure"),
        Output("output-chart2", "figure")
    ],
    [
        Input("input-var1", "value"),
        Input("input-var2", "value")
    ]
)
def update_model(var1, var2):
    animal_health.equation = float(var1)
    fertility_baseline.equation = float(var2) / 365
    df1 = producer_stock.plot(return_df=True).reset_index()
    df2 = death_rate.plot(return_df=True).reset_index()
    df21 = illness_death_rate.plot(return_df=True).reset_index()
    df3 = birth_rate.plot(return_df=True).reset_index()
    date_label = "Elapsed time (days)"
    chart1_figure = {
        "data": [
            {
                "x": df1.iloc[:, 0],
                "y": df1.iloc[:, 1],
                "type": "lines"
            }
        ],
        "layout": {
            "title": {
                "text": "Producer stock",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {
                "fixedrange": True,
                "title": date_label
            },
            "yaxis": {
                "fixedrange": True,
                "title": "Number of livestock (TLU)"
            },
            "colorway": ["#17B897"],
        }
    }
    chart2_figure = {
        "data": [
            {
                "name": "Death rate",
                "x": df2.iloc[:, 0],
                "y": df2.iloc[:, 1] * 365 + df21.iloc[:, 1] * 365,
                "type": "lines",
                "color": "red"
            },
            {
                "name": "Birth rate",
                "x": df3.iloc[:, 0],
                "y": df3.iloc[:, 1] * 365,
                "type": "lines"
            }
        ],
        "layout": {
            "title": {
                "text": "Birth and death rates",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {
                "title": date_label,
                "fixedrange": True,
            },
            "yaxis": {
                "title": "Rate (TLU/year)",
                "fixedrange": True
            },
            # "colorway": ["#17B897"],
        },
    }
    return chart1_figure, chart2_figure


if __name__ == '__main__':
    app.run_server(debug=True)
