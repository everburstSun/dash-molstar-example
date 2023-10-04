import json

import dash
import dash_bootstrap_components as dbc
import dash_molstar
from dash import Input, Output, ctx, dcc, html
from dash_molstar.utils import molstar_helper

from .home import get_sidebar

with open('pages/text.json') as f:
    data = json.load(f)
    Principles = data['Principles']
    Veklury = data['Veklury']
    Paxlovid = data['Paxlovid']

def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='https://cdn.rcsb.org/news/2020/zoom_6lu7_crystal.jpg', alt='Main Protease', className="banner-image"),
                html.Div([
                    html.H2("SARS-CoV-2 Main Protease"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])

    layout_components = dbc.Row([
        dbc.Col([
            dbc.Tabs(
                [
                    dbc.Tab([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Markdown(Principles, className="card-text text-justify"),
                            ]), className='drug-tab mt-2')
                    ], label="The Principles", tab_id='tab_1'),
                    dbc.Tab([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Markdown(Veklury, className="card-text text-justify"),
                                html.Span([
                                    dbc.Button("Focus", size="sm", id="focus_remdesivir"),
                                    html.P("on Remdesivir to see where it get the enzyme stuck.", className='ps-1 m-0')
                                ], className="d-flex align-items-center card-text text-justify"),
                            ]), className='drug-tab mt-2')
                    ], label="Veklury", tab_id='tab_2'),
                    dbc.Tab([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Markdown(Paxlovid, className="card-text text-justify"),
                                html.Span([
                                    dbc.Button("Focus", size="sm", id="focus_nirmatrelvir"),
                                    html.P("on Nirmatrelvir to see where it get the enzyme blocked.", className='ps-1 m-0')
                                ], className="d-flex align-items-center card-text text-justify"),
                            ]), className='drug-tab mt-2')
                    ], label="Paxlovid", tab_id='tab_3'),
                ], id="tabs")
        ], xs=12, sm=12, md=12, lg=6, xl=6, className='mt-3'),
        dbc.Col([
            dash_molstar.MolstarViewer(id='viewer1')
        ], xs=12, sm=12, md=12, lg=6, xl=6, className='mt-3'),
    ], className='mb-4 mt-2 align-items-start')

    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            dbc.Container(layout_components, fluid='md')
        ], className='content')
    ]

    return layout

@dash.callback(
        Output("viewer1", "data"),
        Input("tabs", "active_tab"))
def switch_tab(at):
    if at == "tab_2":
        url = 'https://files.rcsb.org/download/7B3C.cif'
        viewer_data = molstar_helper.parse_url(url)
    elif at == "tab_3":
        url = 'https://files.rcsb.org/download/7U28.cif'
        chain_A = molstar_helper.get_targets("A")
        surface = molstar_helper.create_component("Chain A", chain_A, 'molecular-surface')
        viewer_data = molstar_helper.parse_url(url, component=surface)
    else:
        return dash.no_update
    return viewer_data

@dash.callback(
        Output('viewer1', 'selection'),
        Output("viewer1", "focus"),
        Input("focus_remdesivir", "n_clicks"),
        Input("focus_nirmatrelvir", "n_clicks"),
        prevent_initial_call=True)
def focus_on(*yes):
    if ctx.triggered_id == "focus_remdesivir":
        remdesivir = molstar_helper.get_targets("P", 12, True)
        focus = molstar_helper.get_focus(remdesivir)
        selection = molstar_helper.get_selection(remdesivir)
    else:
        nirmatrelvir = molstar_helper.get_targets("A", 401, True)
        focus = molstar_helper.get_focus(nirmatrelvir)
        selection = molstar_helper.get_selection(nirmatrelvir, select=False)
    return selection, focus