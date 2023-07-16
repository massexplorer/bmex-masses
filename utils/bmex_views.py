from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import utils.dash_reusable_components as drc
import utils.views_class as views


def masses_view():
    
    return html.Div(
        id="body",
        className="container scalable",
        children=[
            html.Div(
                id="app-container",
                children=[
                    html.Div(
                        id="left-column",
                        children=[
                            dcc.Tabs(id="main-tabs", value='tab1', children=[
                                dcc.Tab(label='1', value='tab1', className='custom-tab', selected_className='custom-tab--selected'),
                                dcc.Tab(label='+', value='tab0', className='custom-tab', selected_className='custom-tab--selected'),
                            ]),
                            html.Div(id='tabs_output', children=[])
                        ]
                    ),
                    html.Div(
                        id='center-column',
                        children=[
                            # dcc.Loading(id="loading-1", style={'width':'100%'},
                            # children=[
                                html.Div(id="div-graphs")
                            # ])
                        ]),
                    html.Div(
                        id="right-column",
                        children=[
                            drc.Card(id="copy-card", title='Copy link to this exact view', children=[
                                html.P("Share View", id="clipboard-title"),
                                dcc.Clipboard(id="clipboard", content=""),
                            ]),
                            drc.Card(id="download-card", children=[
                                html.Button("Export Pub. PDFs", id="download-button", title='Download all displayed figures as PDFs'),
                            ]),
                            # drc.Card(
                            #     id="range-card", 
                            #     children=[
                            #         html.P("Neutrons Range:"),
                            #         dcc.Input(id="nmin", type="number", placeholder="N min", min=0, max=300),
                            #         dcc.Input(id="nmax", type="number", placeholder="N max", min=0, max=300),
                            #         html.P("Protons Range:", style={'marginTop': 25}),
                            #         dcc.Input(id="zmin", type="number", placeholder="Z min", min=0, max=200),
                            #         dcc.Input(id="zmax", type="number", placeholder="Z max", min=0, max=200),
                            #     ]
                            # ),
                            # drc.Card(id="colorbar-button-card", children=[
                            #     html.Button("Link Colorbars", id="link-colorbar-button", 
                            #                 title='Matches colorbars of multiple figures, retaining the furthest extrema of the original colorbars'),
                            # ]),
                            drc.Card(id="link-view-card", title='Linked figures will mirror zooms upon interaction with one', children=[
                                html.Button("Link Views", id="link-view-button"),
                                dcc.Checklist([], id='link-view-checklist', inline=True, )
                                            #   persistence=True, persistence_type='memory')
                            ]),
                            drc.Card(id="even-even-card", title='Show only even-even nuclei', children=[
                                dcc.Checklist(options=['Even-Even Nuclei'], value=[], id='even-even-checklist', inline=True, )
                                            #   persistence=True, persistence_type='memory')
                            ]),
                            drc.Card(id="colorbar-scale-card", children=[
                                html.Button("Rescale Colorbar", id={'type': 'rescale-colorbar-button','index': 1}, className='rescale-colorbar-button', 
                                            title='Rescales the colorbar of the selected figure based on the min and max of its currently visable values'),
                            ]),
                            drc.Card(id="reset-card", children=[
                                html.Button('Reset Page', id='reset-button', className='reset-button', title='Erases all user selections'),
                            ]),
                        ]
                    )                   
                ],              
            )
        ],
    )
