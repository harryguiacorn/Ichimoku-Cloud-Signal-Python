import datetime
import pandas_datareader.data as web
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import logging

logger = logging.getLogger(__name__)

# UI
app = dash.Dash()
app.title = "Stock Visualisation"
app.layout = html.Div(
    children=[
        html.H1("Stock Visualisation Dashboard"),
        html.H4("Please enter the stock name"),
        dcc.Input(id="input", value="", type="text"),
        html.Div(id="output-graph"),
    ]
)


def update_value(input_data):
    # Reads stock prices from 1st January 2010
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime.now()

    # Read stock data from yahoo's finance API from start to end
    df = web.DataReader(input_data, "yahoo", start, end)
    logger.debug(
        "Fetched dataframe for %s:\n%s", input_data, df.head().to_string()
    )
    return dcc.Graph(
        id="example",
        figure={
            "data": [
                {
                    "x": df.index,
                    "y": df.Close,
                    "type": "line",
                    "name": input_data,
                },
            ],
            "layout": {"title": input_data},
        },
    )


if __name__ == "__main__":
    app.run_server()
