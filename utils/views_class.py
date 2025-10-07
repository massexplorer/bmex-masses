import dash
from dash import dcc, html
import utils.figures as figs
from utils.bmex_views import *

class View:
    def __init__(self, my_dict, graphindex=0):
        for key in my_dict:
            setattr(self, key, my_dict[key])
        self.index = graphindex

    def plot(self, graph_style={}):
        # Determine if BMC footnote should be shown
        show_bmc = (
            len(self.dataset)
            and self.dataset[0] == "BayesianModelCombination"
            and getattr(self, "bmc_models", None) is not None
            and getattr(self, "bmc_coverage", None) is not None
        )

        footnote = None
        if show_bmc:
            footnote = html.Div(
                className="bmc-footnote",
                style={"fontSize": "0.8rem", "opacity": 0.8, "marginTop": "0.25rem"},
                children=[
                    html.Div("Bayesian Model Combination"),
                    html.Div(
                        "Models: " + ", ".join([str(m) for m in self.bmc_models])
                    ),
                    html.Div(
                        "Coverage: "
                        + ", ".join(["{:.3f}".format(c) for c in self.bmc_coverage])
                    ),
                ],
            )

        # Single plot
        if self.dimension == 'single':
            graph = figs.single(
                self.quantity, self.dataset, self.proton, self.neutron, self.wigner
            )
            return html.Div([graph, footnote]) if footnote else graph

        # Landscape plot
        elif self.dimension == 'landscape':
            graph = dcc.Graph(
                className='graph',
                id={'type': 'graph', 'index': self.index},
                style=graph_style,
                figure=figs.landscape(
                    self.quantity, self.dataset, self.colorbar, self.wigner,
                    self.proton, self.neutron, self.nucleon, self.colorbar_range,
                    self.range, self.even_even
                ),
                relayoutData={'dragmode': 'pan'}
            )
            return html.Div([graph, footnote]) if footnote else graph

        # Landscape diff plot
        elif self.dimension == 'landscape_diff':
            graph = dcc.Graph(
                className='graph',
                id={'type': 'graph', 'index': self.index},
                style=graph_style,
                figure=figs.landscape_diff(
                    self.quantity, self.dataset, self.colorbar, self.wigner,
                    self.proton, self.neutron, self.nucleon, self.colorbar_range,
                    self.range, self.even_even
                )
            )
            return html.Div([graph, footnote]) if footnote else graph

        # 1D plot
        elif self.dimension == '1D':
            if {
                'isotopic': self.proton,
                'isotonic': self.neutron,
                'isobaric': self.nucleon,
                'isotopic_diff': self.proton,
                'isotonic_diff': self.neutron
            }[self.chain] is None:
                return html.P(
                    'Please Enter a Valid Chain',
                    style={'padding-left': '180px', 'padding-right': '180px'}
                )

            figure = getattr(figs, self.chain)(
                self.quantity, self.dataset, self.colorbar, self.wigner,
                self.proton, self.neutron, self.nucleon, self.range,
                self.uncertainty, self.even_even
            )

            # Force graph to redraw
            figure["layout"]["uirevision"] = None

            graph = dcc.Graph(
                className='graph',
                id={'type': 'graph', 'index': self.index},
                style=graph_style,
                figure=figure
            )
            return html.Div([graph, footnote]) if footnote else graph
