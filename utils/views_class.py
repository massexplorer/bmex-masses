import dash
from dash import dcc
from dash import html
import utils.figures as figs
from utils.bmex_views import *


class View:
    def __init__(self, my_dict, graphindex=0):
        for key in my_dict:
            setattr(self, key, my_dict[key])
        self.index = graphindex


    def plot(self, graph_style={}):
        if self.dimension == 'single':
            return figs.single(self.quantity, self.dataset, self.proton, self.neutron, self.wigner)
        elif self.dimension == 'landscape':
            # try:
            return dcc.Graph(className='graph', id={'type': 'graph','index': self.index}, style=graph_style,
                                figure=figs.landscape(self.quantity, self.dataset, self.colorbar, self.wigner, self.proton, \
                                                    self.neutron, self.nucleon, self.colorbar_range, self.range, self.even_even, include_bmc=getattr(self, "include_bmc", False)),\
                                relayoutData={'dragmode': 'pan'})
            # except:
            #     return html.P('This particular plot is not available', style={'fontSize': 20,'paddingLeft': '180px', 'paddingRight': '180px'})
        elif self.dimension == 'landscape_diff':
             return dcc.Graph(className='graph', id={'type': 'graph','index': self.index}, style=graph_style, \
                              figure=figs.landscape_diff(self.quantity, self.dataset, self.colorbar, self.wigner, self.proton, \
                                                    self.neutron, self.nucleon, self.colorbar_range, self.range, self.even_even))
        elif self.dimension == '1D':
            if {'isotopic':self.proton,'isotonic':self.neutron,'isobaric':self.nucleon,'isotopic_diff':self.proton,'isotonic_diff':self.neutron}[self.chain] == None:
                return html.P('Please Enter a Valid Chain', style={'paddingLeft': '180px', 'paddingRight': '180px'})
            include_bmc = getattr(self, "include_bmc", False)
            figure = getattr(figs, self.chain)(
                self.quantity, self.dataset, self.colorbar, self.wigner,
                self.proton, self.neutron, self.nucleon, self.range,
                self.uncertainty, self.even_even,
                include_bmc=include_bmc
            )
            return dcc.Graph(
                className='graph',
                id={'type': 'graph','index': self.index},
                style=graph_style,
                figure=figure
            )