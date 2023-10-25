import json

import dash_bootstrap_components as dbc
import dash_molstar
from dash import html
from dash_molstar.utils import molstar_helper

with open('pages/text.json') as f:
    data = json.load(f)
    desc = data['desc']
    virus_desc = data['virus_desc']
virus_3d = molstar_helper.parse_url("https://molstar.org/demos/states/sars-cov-2_virion.molx", mol=False)

def get_sidebar(active_item=None):
    nav = html.Nav(id="sidebar", className="active", children=[
        html.Div(className="custom-menu", children=[
            html.Button([
                html.I(className="fa fa-bars"),
                html.Span("Toggle Menu", className="sr-only")
            ], type="button", id="sidebarCollapse", className="btn btn-primary")
        ]),
        html.Div(className="flex-column p-4 nav nav-pills", children=[
            html.A([
                html.Img(src='https://webstatic.everburstsun.net/dash-molstar-example/nav.png', alt='', width=48, height=48, className='mx-2'),
                html.Span("SARS-CoV-2", className='fs-4'),
            ], className='d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none', href='/'),
            html.Hr(),
            dbc.NavItem(dbc.NavLink("Overview", href="/", className='text-white', active=True if active_item=='pages.home' else False)),
            dbc.NavItem(dbc.NavLink("Genome & Proteins", href="/proteins", className='text-white', active=True if active_item=='pages.proteins' else False)),
            dbc.NavItem(dbc.NavLink("Therapeutics", href="/drugs", className='text-white', active=True if active_item=='pages.drugs' else False)),
            dbc.NavItem(dbc.NavLink("About", href="/about", className='text-white', active=True if active_item=='pages.about' else False))
        ])
    ])
    return nav

def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='https://webstatic.everburstsun.net/dash-molstar-example/respiratory-droplet-md.png', alt='respiratory droplet', className="banner-image"),
                html.Div([
                    html.Span(['By ', html.I('David S. Goodsell')]),
                    html.H5('Respiratory Droplet')
                ], className='alt-text'),
                html.Div([
                    html.H2("SARS-CoV-2"),
                    html.P(desc)
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])

    layout_components = dbc.Row([
        dbc.Col([
            html.Div(html.P(virus_desc), className='text-justify'),
            html.Div(html.P('You can zoom, rotate the virus model in the 3D Viewer to explore the virus.'), className='text-justify'),
            html.Img(src='https://www.frontiersin.org/files/Articles/815388/fviro-01-815388-HTML/image_m/fviro-01-815388-g001.jpg', alt='Virus', className="img-fluid"),
            html.Div([html.I("Front. Virol.")," 1:815388. doi: 10.3389/fviro.2021.815388"], className='ref text-end')
        ], xs=12, sm=12, md=12, lg=6, xl=6, className='mt-3'),
        dbc.Col([
            dash_molstar.MolstarViewer(id='viewer1', data=virus_3d)
        ], xs=12, sm=12, md=12, lg=6, xl=6, className='mt-3'),
    ], className='mb-4 mt-2 align-items-end')

    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            dbc.Container(layout_components, fluid='md')
        ], className='content')
    ]

    return layout