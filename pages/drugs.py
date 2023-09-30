import dash
import dash_bootstrap_components as dbc
import dash_molstar
from dash import dcc, html, Input, Output, ctx
from dash_molstar.utils import molstar_helper

from .home import get_sidebar

Principles = "The development of effective therapeutics for COVID-19 relies on \
a deep understanding of the virus's replication cycle. If you have read the [*G\
enome & Proteins*](/proteins) page of this website, you may have known that the\
re are some key enzymes involved in the SARS-CoV-2 replication cycle. \n\n**1. \
Entry Inhibition:** The first line of defense is preventing the virus from ente\
ring host cells. Therapies in this category aim to block the interaction betwee\
n the virus's spike protein and cellular receptors, such as ACE2. Neutralizing \
antibodies and small molecules may be used to inhibit this crucial initial step\
. \n\n**2. Viral Replication Inhibition:** Once inside the host cell, the virus\
 must replicate its genetic material. Therapeutics in this stage target viral e\
nzymes involved in replication, such as RNA-dependent RNA polymerase (RdRp).\n\n\
**3. Protein Processing Inhibition:** During replication, the virus produces la\
rge precursor proteins, which are later processed into individual functional pr\
oteins. Inhibitors can target this processing step, preventing the virus from g\
enerating crucial components needed for replication and assembly.\n\nThe [US FD\
A](https://www.fda.gov/consumers/consumer-updates/know-your-treatment-options-c\
ovid-19) approved two drug, ***Veklury*** and ***Paxlovid***, for COVID-19 ther\
apy, each targeting a distinct protein of the virus."
Veklury = "The active ingredient in Veklury is known as ***Remdesivir***. It is\
 a nucleotide analogue that specifically targets the RNA-dependent RNA polymera\
se (RdRp). This essential enzyme is responsible for using nucleotides to replic\
ate viral RNA. In normal circumstances, RNA consists of four primary nucleotide\
s: A, U, C, and G.\n\nYou can visualize RdRp as a zipper pull, guiding the proc\
ess of bringing two RNA strands together. However, when an abnormal nucleotide \
is introduced into either of the RNA chains, it acts like a snag in the zipper.\
 This disruption causes the enzyme to become stuck. Unfortunately for the virus\
, it lacks the mechanism to undo this snag. As a result, the polymerase is perm\
anently disabled, halting the virus's ability to replicate itself."
Paxlovid = "One of the active components in Paxlovid is known as ***Nirmatrelvi\
r***. This potent agent is highly specific in its approach, targeting the main \
proteases of SARS-CoV-2.\n\nWhen the virus infiltrates a human cell, it relies \
on the cell's own organelles to manufacture the components necessary for its re\
plication. Viral proteins undergo a critical post-production process to become \
functional. The proteases cleave polyproteins at multiple sites, yielding multi\
ple functional proteins.\n\nIn a manner similar to nucleotide analogs, Nirmatre\
lvir operates as a peptidomimetic inhibitor. It cleverly mimics a normal peptid\
e during the protease's processing attempt. However, here's where Nirmatrelvir'\
s brilliance shines: it forms strong covalent bonds with the enzyme. These bond\
s are exceptionally strong, resulting in the permanent blockade of the enzyme's\
 active site. In essence, Nirmatrelvir effectively shuts down the enzyme, disru\
pting the virus's ability to process essential proteins, and thereby inhibiting\
 its replication."

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