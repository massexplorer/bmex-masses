from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import utils.dash_reusable_components as drc
from utils.dropdown_options import dataset_options
from utils.dropdown_options import quantity_options


class Sidebar:
    
    def __init__(self, views_dict={"dimension": 'landscape', "chain": 'isotopic', "quantity": 'BE', "dataset": ['AME2020'], 
           "colorbar": 'linear', "wigner": [0], "proton": [None], "neutron": [None], "nucleon": [None], 
           "range": {"x": [None, None], "y": [None, None]}, "colorbar_range": [None, None], "uncertainty": False},
             series_tab=1, maintabs_length=1):
        for key in views_dict:
            setattr(self, key, views_dict[key])
        if series_tab == "new":
            self.series_n = len(views_dict["dataset"])
        else:
            self.series_n = series_tab
        self.maintabs_length = maintabs_length

    def proton_card(self, index):
        return drc.Card(
            id="protons-card",
            children=[
                html.P("Protons:", style={"padding-left": '.5rem'}),
                dcc.Input(
                    id={'type': 'input-protons','index': index+1},
                    type="number",
                    min=0,
                    max=200,
                    step=1,
                    placeholder="Proton #",
                    value=self.proton[index],
                    className="nucleon-input"
                ),
            ],
        )

    def neutron_card(self, index):
        return drc.Card(
            id="neutrons-card",
            children=[
                html.P("Neutrons:", style={"padding-left": '.5rem'}),
                dcc.Input(
                    id={'type': 'input-neutrons','index': index+1},
                    type="number",
                    min=0,
                    max=200,
                    step=1,
                    placeholder="Neutron #",
                    value=self.neutron[index],
                    className="nucleon-input"
                ),
            ],
        )

    def nucleon_card(self, index):
        if self.dimension == '1D':
            if self.chain[:8] == "isotopic":
                return self.proton_card(index)
            elif self.chain[:8] == "isotonic":
                return self.neutron_card(index)
            elif self.chain == "isobaric":
                return drc.Card(
                    id="nucleons-card",
                    children=[
                        html.P("Nucleons:", style={"padding-left": '.5rem'}),
                        dcc.Input(
                            id={'type': 'input-nucleons','index': index+1},
                            type="number",
                            min=0,
                            max=400,
                            step=1,
                            placeholder="Nucleon #",
                            value=self.nucleon[index],
                            className="nucleon-input"
                        ),
                    ],
                )
            else:
                return html.P("ERROR")

    def get_letter(self):
        if self.chain[:8]=='isotopic':
            return "Z"
        if self.chain[:8]=='isotonic':
            return "N"
        return "A"

    def get_nucleon_count(self, i):
        if self.chain[:8]=='isotopic':
            return self.proton[i]
        if self.chain[:8]=='isotonic':
            return self.neutron[i]
        return self.nucleon[i]

    def show(self):  
        output = [
            drc.Card(id="dimension-card", title='Select a dimensionality of data to analyze', children=[
                drc.NamedDropdown(
                    name="Dimension",
                    id={'type': 'dropdown-dimension','index': 1},
                    options=[
                        {"label": "Single Nucleus", "value": "single", "title": "Shows a quanity for a selected dataset for a single nucleus"},
                        {"label": "1D Chains", "value": "1D", "title": "Shows a quanity for a selected dataset for a single chain of nuclei"},
                        {"label": "Landscape", "value": "landscape", "title": "Shows a quanity for a selected dataset across all nuclei"},
                        {"label": "Landscape EXP Diff", "value": "landscape_diff", "title": "Shows difference between a selected model and the AME2020 dataset across all nuclei"},
                    ],
                    clearable=False,
                    searchable=False,
                    value=self.dimension,
                )
            ])
        ]

        if self.dimension == '1D':
            output.append(
                drc.Card(id="oneD-card", title='Select the type of chain to plot', children=[
                    drc.NamedDropdown(
                        name='1D Chain',
                        id={'type': 'dropdown-1D','index': 1},
                        options=[
                            {"label": "Isotopic Chain", "value": "isotopic", "title": "Shows a quantity for a selected model across an isotopic chain"},
                            {"label": "Isotonic Chain", "value": "isotonic", "title": "Shows a quantity for a selected model across an isotonic chain"},
                            {"label": "Isobaric Chain", "value": "isobaric", "title": "Shows a quantity for a selected model across an isobaric chain"},
                            {"label": "Isotopic EXP Diff", "value": "isotopic_diff", "title": "Shows difference between a selected model and the AME2020 dataset across an isotopic chain"},
                            {"label": "Isotonic EXP Diff", "value": "isotonic_diff", "title": "Shows difference between a selected model and the AME2020 dataset across an isotonic chain"},
                        ],
                        clearable=False,
                        searchable=False,
                        value=self.chain,
                    )
                ])
            )
        
        # Append the quantity dropdown card
        output.append(
            drc.Card(id="quantity-card", title='Select the quantity to be graphed on the selected figure', 
                children=[
                    drc.NamedDropdown(
                        name="Select Quantity",
                        id={'type': 'dropdown-quantity','index': 1},
                        options=quantity_options(self.dataset[self.series_n-1],single=True if self.dimension=='single' else False,
                        selected_beta_type=self.beta_type if hasattr(self, 'beta_type') else "minus"),
                        clearable=False,
                        searchable=False,
                        value=self.quantity,
                        optionHeight=75,
                        maxHeight=380,
                        className="quantity-dropdown"                      
                    )
                ]
            )
        )
        output.append(
            html.Div(
                id={"type": "beta-type-card", "index": 1},
                children=[
                    html.P("Beta Decay Type:"),
                    dcc.Dropdown(
                        id={'type': 'dropdown-beta-type', 'index': 1},
                        options=[
                            {"label": "Beta Minus (β⁻)", "value": "minus"},
                            {"label": "Beta Plus (β⁺)", "value": "plus"},
                        ],
                        clearable=False,
                        searchable=False,
                        value="minus" if self.quantity == "BetaMinusDecay" else "plus",
                    )
                ],
                style={"display": "block"} if self.quantity in ['BetaMinusDecay', 'BetaPlusDecay'] else {"display": "none"}
            )
        )

        tabs_component, series_button_card, uncertainty_card = None, None, [None]
        if self.dimension == '1D':
            tabs = []
            for i in range(len(self.dataset)):
                tabs.append(dcc.Tab(label=self.get_letter()+"="+str(self.get_nucleon_count(i))+" | "+str(self.dataset[i]), value='tab'+str(i+1), className='series-tab', selected_className='series-tab--selected'))
            if len(self.dataset) < 9:
                tabs.append(dcc.Tab(label="+", value='tab0', className='series-tab', selected_className='series-tab--selected'))  
            tabs_component = dcc.Tabs(id={'type': 'series_tabs','index': 1}, value='tab'+str(self.series_n), className='series-tabs', children=tabs)
            if len(self.dataset) > 1:
                series_button_card = drc.Card(id="delete-series-card", children=[
                    html.Button('Delete Series', id={'type': 'delete-series-button','index': 1}, value=None, className='delete-button')
                ])
            uncer_checklist = []
            if self.uncertainty[self.series_n-1]:
                uncer_checklist = ['Include Uncertainties']
            if self.dataset[self.series_n-1] == 'AME2020':
                uncertainty_card = drc.Card(id="uncertainty-card", children=[
                    dcc.Checklist(options=['Include Uncertainties'], value=uncer_checklist, id={'type': 'uncertainty-checklist','index': 1}),
                ]),
            output.append(
                drc.Card(id='series-card', children=[
                    tabs_component,
                    self.nucleon_card(self.series_n-1),
                    drc.Card(id="dataset-card", children=[
                        drc.NamedDropdown(
                            name="Select Dataset",
                            id={'type': 'dropdown-dataset','index': self.series_n},
                            options=dataset_options(self.quantity, EXPdiff=self.chain[-4:]=='diff'),
                            clearable=False,
                            searchable=False,
                            value=self.dataset[self.series_n-1],
                            maxHeight=240,
                        )
                    ]),
                    drc.Card(
                        id="Wigner-card", title='Allows for the adjustment from a Wigner term in the selected figure',
                        children=[
                            drc.NamedDropdown(
                                name="Wigner Adjustment",
                                id={'type': 'radio-wigner','index': 1},
                                options=[{"label": "None", "value": 0, "title": "No Wigner term is added to the selected figure"},
                                         {"label": "Wigner (1)", "value": 1, "title": "= 1.8e^(-380((N-Z)/A)^2) -.84|N-Z|e^((-A/26)^2)"},
                                         {"label": "Wigner (2)", "value": 2, "title": "-47|N-Z|/A"}],
                                clearable=False,
                                searchable=False,
                                value=self.wigner[self.series_n-1],
                            ),
                        ]
                    ),
                    uncertainty_card[0],
                    series_button_card
                ])
            )
        else:
            if self.dimension == 'single':
                output.append(self.proton_card(self.series_n-1))
                output.append(self.neutron_card(self.series_n-1))
            output.append(
                drc.Card(id="dataset-card", title='Select the experiment or model dataset to be used for the selected figure',
                    children=[
                        drc.NamedDropdown(
                            name="Select Dataset",
                            id={'type': 'dropdown-dataset','index': self.series_n},
                            options=dataset_options(self.quantity, EXPdiff=self.dimension[-4:]=='diff'),
                            clearable=False,
                            searchable=False,
                            value=self.dataset[self.series_n-1],
                            maxHeight=240,
                        )
                    ]
                ) 
            )
            output.append(
                drc.Card(
                    id="Wigner-card", title='Allows for the adjustment from a Wigner term in the selected figure',
                    children=[
                        drc.NamedDropdown(
                            name="Wigner Adjustment",
                            id={'type': 'radio-wigner','index': 1},
                            options=[{"label": "None", "value": 0, "title": "No Wigner term is added to the selected figure"},
                                     {"label": "Wigner (1)", "value": 1, "title": "W1 = 1.8e^(-380((N-Z)/A)^2) -.84|N-Z|e^((-A/26)^2)"},
                                     {"label": "Wigner (2)", "value": 2, "title": "W2 = -47|N-Z|/A"}],
                            clearable=False,
                            searchable=False,
                            value=self.wigner[self.series_n-1],
                        ),
                    ]
                ),
            )

        if self.dimension[:9] == 'landscape':
            output.append(
                drc.Card(
                    id="colorbar-card", title='Changes the color scheme of the selected figure',
                    children=[
                        drc.NamedDropdown(
                            name="Colorbar Style",
                            id={'type': 'dropdown-colorbar','index': 1},
                            options=[
                                {"label": "Rainbow", "value": "linear"},
                                {"label": "Extended Rainbow", "value": "extended_linear"},
                                {"label": "Equalized Rainbow", "value": "equal"},
                                {"label": "Monochrome", "value": "monochrome"},
                                {"label": "Diverging", "value": "diverging"},
                            ],
                            clearable=False,
                            searchable=False,
                            value=self.colorbar,
                        )
                    ]
                )
            )
            output.append(
                drc.Card(id="colorbar-input-card", children=[
                    html.P('Colorbar Range', id='colorbar-input-label'),
                    dcc.Input(id={'type': 'cb-input-min','index': 1}, type='number', 
                              value=self.colorbar_range[0], className='colorbar-input',
                              placeholder='min'),
                    dcc.Input(id={'type': 'cb-input-max','index': 1}, type='number', 
                              value=self.colorbar_range[1], className='colorbar-input',
                              placeholder='max')
                ]),
            )
            # output.append(
            #     drc.Card(id="colorbar-slider-card", children=[
            #         dcc.RangeSlider(min=self.colorbar_range[0], max=self.colorbar_range[1], step=(self.colorbar_range[1]-self.colorbar_range[0])/10, id={'type': 'colorbar-slider','index': 1}, className='colorbar-slider'),
            #     ]),
            # )

        if self.maintabs_length > 2:
            output.append(
                drc.Card(id="delete-card", children=[
                    html.Button('Delete Plot', id={'type': 'delete-button','index': 1}, value=None, className='delete-button')
                ])
            )

        return output


