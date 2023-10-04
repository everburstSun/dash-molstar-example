import json
import dash_bootstrap_components as dbc
from dash import dcc, html

from .home import get_sidebar

with open('pages/text.json') as f:
    about = json.load(f)['about']

def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='https://raw.githubusercontent.com/everburstSun/dash-molstar-example/main/static/sars-cov-2-fusion.jpg', alt='sars-cov-2-fusion', className="banner-image"),
                html.Div([
                    html.Span(['By ', html.I('David S. Goodsell')]),
                    html.H5('SARS-CoV-2 Fusion')
                ], className='alt-text'),
                html.Div([
                    html.H1("About This Site"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])
    
    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            dbc.Container(dbc.Row(dbc.Col(dcc.Markdown(about, style={"textAlign": "justify"}), md=5, sm=12, className='mt-4 ms-4')), fluid='md')
        ], className='content')
    ]

    return layout