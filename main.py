# import dash_molstar
from flask import Flask
from dash import Dash, callback, html, Input, Output, State, dcc, ctx
# import dash
# import pandas as pd
# import plotly.express as px
# from dash_molstar.utils import molstar_helper
# from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
app = Flask(__name__, instance_relative_config=True)
dash_app = Dash(__name__,
        server=app,
        use_pages=True,
        assets_folder='static'
    )


# Define sidebar content
sidebar = html.Div(
    [
        html.H2("SARS-CoV-2 Information", className="display-4"),
        html.Hr(),
        html.P(
            "Select a topic to learn more about SARS-CoV-2:",
            className="lead",
        ),
        dbc.Nav(
            [
                dbc.NavLink("SARS-CoV-2 Genome", href="/genome", id="genome-link"),
                dbc.NavLink("How the Virus Infects", href="/infect", id="infect-link"),
                dbc.NavLink("How Drugs Work", href="/drugs", id="drugs-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="bg-light sidebar sidebar-offcanvas",
)

# Define content for each page
content = html.Div(id="page-content", className="content")
with app.app_context():
    # Define layout
    dash_app.layout = html.Div(dbc.Row([dcc.Location(id="url"), sidebar, content]), className='container-fluid')

    # Callback to update content based on URL
    @dash_app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )
    def display_page(pathname):
        if pathname == "/genome":
            return html.H1("SARS-CoV-2 Genome Information")
        elif pathname == "/infect":
            return html.H1("How the Virus Infects")
        elif pathname == "/drugs":
            return html.H1("How Drugs Work")
        else:
            return html.H1("Welcome to SARS-CoV-2 Information")
if __name__ == "__main__":
    app.run(debug=True)