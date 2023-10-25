import dash
import json
import dash_bootstrap_components as dbc
import dash_molstar
from dash import html, ctx, Input, Output, State, clientside_callback, dcc
from dash_molstar.utils import molstar_helper

from .home import get_sidebar

with open('pages/coords.json') as f:
    image_map = html.MapEl([html.Area(shape="poly", href='#', id=k, title=k, coords=v) for k, v in json.load(f).items()], name='image-map', id='image-map')

def get_description(PDBID=None):
    with open('pages/proteins.json') as f:
        data = json.load(f)
        if not PDBID:
            record = data['initial']
        else:
            record = data[PDBID]
    card = dbc.Card([
        dbc.CardHeader(record['name']),
        dbc.CardBody(html.P(record['description'], className="card-text")),
    ], color="light")
    return card


def layout():
    layout_components = [
        html.H1("An Overview of Proteins"),
        dbc.Row([
            dbc.Col([
                html.Img(src='https://webstatic.everburstsun.net/dash-molstar-example/covid-genome-prots.png', alt='genome proteins', useMap='#image-map', className="img-fluid"),
                image_map
            ], xs=12, sm=12, md=12, lg=12, xl=8, id='genome_proteins_container', className='mt-3'),
            dbc.Col([
                html.Div(get_description(), id='card'),
                dash_molstar.MolstarViewer(id='viewer2', className='mt-2 mb-2')
            ], xs=12, sm=12, md=12, lg=12, xl=4, className='mt-3'),
        ], className='mb-4 mt-2 align-items-center')
    ]

    layout = [
        get_sidebar(__name__),
        html.Div(dbc.Container(layout_components, fluid=True), className='content'),
    ]

    return layout

@dash.callback(
        Output('card', 'children'),
        Output('viewer2', 'data'),
        Input("8CTK", "n_clicks"),
        Input("7K3G", "n_clicks"),
        Input("6XDC", "n_clicks"),
        Input("6VYB", "n_clicks"),
        Input("6WVN", "n_clicks"),
        Input("6WXC", "n_clicks"),
        Input("7N0C", "n_clicks"),
        Input("7NNG", "n_clicks"),
        Input("6YYT", "n_clicks"),
        Input("6WXD", "n_clicks"),
        Input("NSP6", "n_clicks"),
        Input("6LU7", "n_clicks"),
        Input("NSP4", "n_clicks"),
        Input("6WUU", "n_clicks"),
        Input("6W9C", "n_clicks"),
        Input("7MSW", "n_clicks"),
        Input("7K3N", "n_clicks"),
        Input("8FD5", "n_clicks"),
        Input("7JX6", "n_clicks"),
        Input("6Z4U", "n_clicks"),
        Input("7CI3", "n_clicks"),
        Input("7VPG", "n_clicks"),
        prevent_initial_call=True)
def download_structure(*args):
    PDBID = ctx.triggered_id
    if PDBID.startswith("NSP"):
        url = f'https://webstatic.everburstsun.net/dash-molstar-example/{PDBID}.pdb'
    else:
        url = f'https://files.rcsb.org/download/{PDBID}.cif'
    viewer_data = molstar_helper.parse_url(url)
    card_data = get_description(PDBID)
    return card_data, viewer_data

clientside_callback(
    """
    function(imageMapName) {
        const divElement = document.getElementById('genome_proteins_container');
        const originalMapElement = document.querySelector('map[name="image-map"]');
        const mapElement = originalMapElement.cloneNode(true);

        function updateCoords() {
            const imageRatio = 1200 / 909;
            const currentWidth = divElement.clientWidth - parseFloat(getComputedStyle(divElement).paddingLeft) - parseFloat(getComputedStyle(divElement).paddingRight);
            const currentHeight = currentWidth / imageRatio;

            const widthScale = currentWidth / 1200;
            const heightScale = currentHeight / 909;
            
            const originalAreas = originalMapElement.getElementsByTagName('area');
            const areas = mapElement.getElementsByTagName('area');
            for (let i = 0; i < areas.length; i++) {
                const originalCoords = areas[i].getAttribute('coords').split(',');
                const newCoords = originalCoords.map((coord, index) => {
                return index % 2 === 0 ? Math.round(coord * widthScale) : Math.round(coord * heightScale);
                });
                originalAreas[i].setAttribute('coords', newCoords.join(','));
            }
        }

        updateCoords();
        window.addEventListener('resize', updateCoords);
    }
    """,
    Output('image-map', 'style'),
    Input('image-map', 'name')
)

clientside_callback(
    """
    function(yes, name){
        if (name === 'active') {
            return '';
        } else if (name === '') {
            return 'active';
        }
    }
    """,
    Output('sidebar', 'className'),
    Input('sidebarCollapse', 'n_clicks'),
    State('sidebar', 'className')
)