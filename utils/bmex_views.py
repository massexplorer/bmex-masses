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
                            drc.Card(
                                id="range-card", 
                                children=[
                                    html.P("Neutrons Range:"),
                                    dcc.Input(id="nmin", type="number", placeholder="N min", min=0, max=300),
                                    dcc.Input(id="nmax", type="number", placeholder="N max", min=0, max=300),
                                    html.P("Protons Range:", style={'marginTop': 25}),
                                    dcc.Input(id="zmin", type="number", placeholder="Z min", min=0, max=200),
                                    dcc.Input(id="zmax", type="number", placeholder="Z max", min=0, max=200),
                                ]
                            ),
                            drc.Card(id="colorbar-button-card", children=[
                                html.Button("Link Colorbars", id="link-colorbar-button", title='Matches colorbars of multiple figures, retaining the furthest extrema of the original colorbars'),
                            ]),
                            drc.Card(id="link-view-card", title='Linked figures will mirror zooms upon interaction with one', children=[
                                html.Button("Link Views", id="link-view-button"),
                                dcc.Checklist([], id='link-view-checklist', inline=True, )
                                            #   persistence=True, persistence_type='memory')
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

def gpe_view():
    return html.Div(
        id="body",
        className="container scalable",
        children=[
            html.Div(
                id="app-container",
                # className="row",
                children=[
                    html.Div(
                        # className="three columns",
                        id="left-column",
                        children=[
                            drc.Card(
                                id="first-card",
                                children=[
                                    drc.NamedDropdown(
                                        name="Compute For",
                                        id="dropdown-iso-chain",
                                        options=[
                                            {"label": "Single Nucleus", "value": "single"},
                                            {"label": "Isotopic Chain", "value": "isotopic"},
                                            #{"label": "Isotonic Chain", "value": "isotonic"},
                                        ],
                                        clearable=False,
                                        searchable=False,
                                        value="single",
                                    ),
                                ]
                            ),
                            drc.Card(
                                id="quantity-single",
                                children=[
                                    drc.NamedDropdown(
                                        name="Select Quantity",
                                        id="dropdown-select-quantity",
                                        options=[
                                            #{"label": "All", "value": "All"},
                                            #{"label": "Binding Energy", "value": "BE"},
                                            #{"label": "One Neutron Separation Energy", "value": "OneNSE",},
                                            #{"label": "One Proton Separation Energy", "value": "OnePSE",},
                                            {"label": "Two Neutron Separation Energy", "value": "TwoNSE",},
                                            #{"label": "Two Proton Separation Energy", "value": "TwoPSE",},
                                            #{"label": "Alpha Separation Energy", "value": "AlphaSE",},
                                            #{"label": "Two Proton Shell Gap", "value": "TwoNSGap",},
                                            #{"label": "Two Neutron Shell Gap", "value": "TwoPSGap",},
                                            #{"label": "Double Mass Difference", "value": "DoubleMDiff",},
                                            #{"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED",},
                                            #{"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED",},
                                            #{"label": "Single-Neutron Energy Splitting", "value": "SNESplitting",},
                                            #{"label": "Single-Proton Energy Splitting", "value": "SPESplitting",},
                                            #{"label": "Wigner Energy Coefficient", "value": "WignerEC",},
                                        ],
                                        clearable=False,
                                        searchable=False,
                                        value="TwoNSE",
                                    ),
                                ]
                            ),
                            drc.Card(
                                id="data-card",
                                children=[
                                    drc.NamedDropdown(
                                        name="Select Dataset",
                                        id="dropdown-select-dataset",
                                        options=[
                                            {"label": "FRDM", "value": "FRDM"},
                                            #{"label": "SkMs", "value": "SkMs"},
                                        ],
                                        clearable=False,
                                        searchable=False,
                                        value="FRDM",
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="gp-card",
                                children=[
                                    drc.NamedInput(
                                        name="Eta",
                                        id="eta",
                                        type="number",
                                        min=0.0,
                                        max=5.0,
                                        #step=0.01,
                                        placeholder="Eta",
                                        style={'width':'100%'},
                                        value=0.9,
                                    ),
                                    drc.NamedInput(
                                        name="RhoN",
                                        id="rhon",
                                        type="number",
                                        min=0,
                                        max=5,
                                        #step=0.01,
                                        placeholder="RhoN",
                                        style={'width':'100%'},
                                        value=1.529,
                                    ),
                                    drc.NamedInput(
                                        name="RhoZ",
                                        id="rhoz",
                                        type="number",
                                        min=0,
                                        max=5,
                                        #step=0.01,
                                        placeholder="RhoZ",
                                        style={'width':'100%'},
                                        value=0.2533,
                                    ),
                                    html.Button('Train!', id='submit-gpe', n_clicks=0, style={"color":"#e76f51"}),
                                ]
                            ),
                            drc.Card(
                                id="protons-card",
                                children=[
                                    drc.NamedInput(
                                        name="Protons",
                                        id="protons",
                                        type="number",
                                        min=0,
                                        max=200,
                                        step=1,
                                        placeholder="Proton #",
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="neutrons-card",
                                children=[
                                    drc.NamedInput(
                                        name="Neutrons",
                                        id="neutrons",
                                        type="number",
                                        min=0,
                                        max=200,
                                        step=1,
                                        placeholder="Neutron #",
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="zmin-card",
                                children=[
                                    drc.NamedInput(
                                        name="Minimum Z",
                                        id="zmin",
                                        type="number",
                                        min=0,
                                        max=200,
                                        step=1,
                                        placeholder="Z Min",
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="zmax-card",
                                children=[
                                    drc.NamedInput(
                                        name="Maximum Z",
                                        id="zmax",
                                        type="number",
                                        min=0,
                                        max=200,
                                        step=1,
                                        placeholder="Z Max",
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="nmin-card",
                                children=[
                                    drc.NamedInput(
                                        name="Minimum N",
                                        id="nmin",
                                        type="number",
                                        min=0,
                                        max=200,
                                        step=1,
                                        placeholder="N Min",
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="nmax-card",
                                children=[
                                    drc.NamedInput(
                                        name="Maximum N",
                                        id="nmax",
                                        type="number",
                                        min=0,
                                        max=200,
                                        step=1,
                                        placeholder="N Max",
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # html.Div(
                    #     id="div-graphs-loading",
                    #     children=[
                    #         dcc.Loading(
                    #             id="loading-1",
                    #             children=[
                    #                 html.Div(
                    #                     id="div-graphs-gpe",
                    #                     children=[
                    #                         dcc.Graph(
                    #                             id="graph-sklearn-svm",
                    #                             figure=dict(
                    #                                 layout=dict(
                    #                                     plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                    #                                 )
                    #                             ),
                    #                         ),
                    #                     ],
                    #                 ),
                    #             ],
                    #         ),
                    #     ],
                    # ),
                    
                    html.Div(id='div-right',children=
                    dcc.Loading(
                        id="loading-1",
                        children =html.Div(id="div-graphs-loading",style={'width':'100%'},children=[html.Div(
                        id="div-graphs-gpe",
                        children=[
                            dcc.Graph(
                                id="graph-sklearn-svm",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                    )
                                ),
                            ),
                        ],
                    ),]))),
                ],
            )
        ],
    )

def pesnet_view():
    return html.Div(
        id="body",
        className="container scalable",
        children=[
            html.Div(
                id="app-container",
                # className="row",
                children=[
                    html.Div(
                        # className="three columns",
                        id="left-column",
                        children=[
                            drc.Card(
                                id="first-card",
                                children=[
                                    drc.NamedDropdown(
                                        name="Compute For",
                                        id="dropdown-iso-chain",
                                        options=[
                                            {"label": "Single Nucleus", "value": "single"},
                                            #{"label": "Isotonic Chain", "value": "isotonic"},
                                        ],
                                        clearable=False,
                                        searchable=False,
                                        value="single",
                                    ),
                                ]
                            ),
                            drc.Card(
                                id="quantity-single",
                                children=[
                                    drc.NamedDropdown(
                                        name="Select Quantity",
                                        id="dropdown-select-quantity",
                                        options=[
                                            #{"label": "All", "value": "All"},
                                            #{"label": "Binding Energy", "value": "BE"},
                                            #{"label": "One Neutron Separation Energy", "value": "OneNSE",},
                                            #{"label": "One Proton Separation Energy", "value": "OnePSE",},
                                            {"label": "Potential Energy Surface", "value": "PES",},
                                            #{"label": "Two Proton Separation Energy", "value": "TwoPSE",},
                                            #{"label": "Alpha Separation Energy", "value": "AlphaSE",},
                                            #{"label": "Two Proton Shell Gap", "value": "TwoNSGap",},
                                            #{"label": "Two Neutron Shell Gap", "value": "TwoPSGap",},
                                            #{"label": "Double Mass Difference", "value": "DoubleMDiff",},
                                            #{"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED",},
                                            #{"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED",},
                                            #{"label": "Single-Neutron Energy Splitting", "value": "SNESplitting",},
                                            #{"label": "Single-Proton Energy Splitting", "value": "SPESplitting",},
                                            #{"label": "Wigner Energy Coefficient", "value": "WignerEC",},
                                        ],
                                        clearable=False,
                                        searchable=False,
                                        value="PES",
                                    ),
                                ]
                            ),
                            drc.Card(
                                id="data-card",
                                children=[
                                    drc.NamedDropdown(
                                        name="Select Dataset",
                                        id="dropdown-select-dataset",
                                        options=[
                                            {"label": "UNEDF1", "value": "UNEDF1"},
                                            #{"label": "SkMs", "value": "SkMs"},
                                        ],
                                        clearable=False,
                                        searchable=False,
                                        value="UNEDF1",
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="protons-card",
                                children=[
                                    drc.NamedInput(
                                        name="Protons",
                                        id="protons",
                                        type="number",
                                        min=0,
                                        max=200,
                                        step=1,
                                        placeholder="Proton #",
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="neutrons-card",
                                children=[
                                    drc.NamedInput(
                                        name="Neutrons",
                                        id="neutrons",
                                        type="number",
                                        min=0,
                                        max=250,
                                        step=1,
                                        placeholder="Neutron #",
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # html.Div(
                    #     id="div-graphs-loading",
                    #     children=[
                    #         dcc.Loading(
                    #             id="loading-1",
                    #             children=[
                    #                 html.Div(
                    #                     id="div-graphs-gpe",
                    #                     children=[
                    #                         dcc.Graph(
                    #                             id="graph-sklearn-svm",
                    #                             figure=dict(
                    #                                 layout=dict(
                    #                                     plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                    #                                 )
                    #                             ),
                    #                         ),
                    #                     ],
                    #                 ),
                    #             ],
                    #         ),
                    #     ],
                    # ),
                    html.Div(id='div-right',children=
                    dcc.Loading(
                        id="loading-1",
                        children =html.Div(id="div-graphs-loading",style={'width':'100%'},children=[html.Div(
                        id="div-graphs-pesnet",
                        children=[
                            dcc.Graph(
                                id="graph-sklearn-svm",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                    )
                                ),
                            ),
                        ],
                    ),]))),
                ],
            )
        ],
    )

def emu_view():
    return html.Div(
        id="body",
        className="container scalable",
        children=[
            html.Div(
                id="app-container",
                # className="row",
                children=[
                    html.Div(
                        # className="three columns",
                        id="left-column",
                        children=[
                            drc.Card(
                                id="first-card",
                                children=[
                                    drc.NamedDropdown(
                                        name="Compute For",
                                        id="dropdown-nuc",
                                        options=[
                                            {"label": "16O", "value": "16O"},
                                            {"label": "40Ca", "value": "40Ca"},
                                            {"label": "48Ca", "value": "48Ca"},
                                            {"label": "68Ni", "value": "68Ni"},
                                            {"label": "90Zr", "value": "90Zr"},
                                            {"label": "100Sn", "value": "100Sn"},
                                            {"label": "116Sn", "value": "116Sn"},
                                            {"label": "132Sn", "value": "132Sn"},
                                            {"label": "144Sm", "value": "144Sm"},
                                            {"label": "208Pb", "value": "208Pb"},
                                        ],
                                        clearable=False,
                                        searchable=False,
                                        value="16O",
                                    ),
                                ]
                            ),
                            drc.Card(
                                id="data-card",
                                children=[
                                    drc.NamedDropdown(
                                        name="Select Model",
                                        id="dropdown-select-dataset",
                                        options=[
                                            {"label": "Covariant EDF", "value": "rmf"},
                                            #{"label": "SkMs", "value": "SkMs"},
                                        ],
                                        clearable=False,
                                        searchable=False,
                                        value="rmf",
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="msigma-card",
                                children=[
                                    drc.NamedInput(
                                        name="Mass of Sigma Meson",
                                        id="Msigma",
                                        type="number",
                                        min=480,
                                        max=505,
                                        # step=1,
                                        placeholder=488.0,
                                        value=488.0,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="rho-card",
                                children=[
                                    drc.NamedInput(
                                        name="Saturation Density",
                                        id="Rho",
                                        type="number",
                                        min=0.147,
                                        max=0.159,
                                        # step=1,
                                        placeholder=0.151,
                                        value=0.151,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="e-card",
                                children=[
                                    drc.NamedInput(
                                        name="BE at Saturation",
                                        id="BE",
                                        type="number",
                                        min=-16.50,
                                        max=-16.00,
                                        # step=1,
                                        placeholder=-16.35,
                                        value=-16.35,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="mstar-card",
                                children=[
                                    drc.NamedInput(
                                        name="Effective Nucleon Mass",
                                        id="Mstar",
                                        type="number",
                                        min=0.55,
                                        max=0.62,
                                        # step=1,
                                        placeholder=0.59,
                                        value=0.59,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),                            
                            drc.Card(
                                id="k-card",
                                children=[
                                    drc.NamedInput(
                                        name="Incompressibility Coefficient (K)",
                                        id="K",
                                        type="number",
                                        min=200,
                                        max=255,
                                        # step=1,
                                        placeholder=225.0,
                                        value=225.0,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="j-card",
                                children=[
                                    drc.NamedInput(
                                        name="Symmetry Energy (J)",
                                        id="J",
                                        type="number",
                                        min=30,
                                        max=42,
                                        # step=1,
                                        placeholder=36.0,
                                        value=36.0,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="l-card",
                                children=[
                                    drc.NamedInput(
                                        name="Slope of Symmetry Energy (L)",
                                        id="L",
                                        type="number",
                                        min=50,
                                        max=200,
                                        # step=1,
                                        placeholder=80.0,
                                        value=80.0,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="zeta-card",
                                children=[
                                    drc.NamedInput(
                                        name="Quartic Vector Coupling",
                                        id="zeta",
                                        type="number",
                                        min=0.0,
                                        max=0.06,
                                        # step=1,
                                        placeholder=0.04,
                                        value=0.04,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        id="div-emu",
                        children=[
                            dcc.Graph(
                                id="graph-sklearn-svm",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                    )
                                ),
                            ),
                        ],
                    ),
                ],
            )
        ],
    )

