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
        self.line_color = my_dict.get('line_color', "#e76f51")
        self.line_width = my_dict.get('line_width', 2)
        self.line_style = my_dict.get('line_style', "solid")


    def plot(self, graph_style={}):
        if self.dimension == 'single':
            return figs.single(self.quantity, self.dataset, self.proton, self.neutron, self.wigner)
        elif self.dimension == 'landscape':
            # try:
            return dcc.Graph(className='graph', id={'type': 'graph','index': self.index}, style=graph_style,
                                figure=figs.landscape(self.quantity, self.dataset, self.colorbar, self.wigner, self.proton, \
                                                    self.neutron, self.nucleon, self.colorbar_range, self.range, self.even_even, show_text=getattr(self, "show_text", True)),\
                                relayoutData={'dragmode': 'pan'})
            # except:
            #     return html.P('This particular plot is not available', style={'font-size': 20,'padding-left': '180px', 'padding-right': '180px'})
        elif self.dimension == 'landscape_diff':
             return dcc.Graph(className='graph', id={'type': 'graph','index': self.index}, style=graph_style, \
                              figure=figs.landscape_diff(self.quantity, self.dataset, self.colorbar, self.wigner, self.proton, \
                                                    self.neutron, self.nucleon, self.colorbar_range, self.range, self.even_even))
        elif self.dimension == '1D':
            if {'isotopic':self.proton,'isotonic':self.neutron,'isobaric':self.nucleon,'isotopic_diff':self.proton,'isotonic_diff':self.neutron}[self.chain] == None:
                return html.P('Please Enter a Valid Chain', style={'padding-left': '180px', 'padding-right': '180px'})
            figure = getattr(figs, self.chain)(
            self.quantity, self.dataset, self.colorbar, self.wigner, 
            self.proton, self.neutron, self.nucleon, self.range, 
            self.uncertainty, self.even_even
        )
            # Update all traces
        for i, trace in enumerate(figure['data']):
            # First trace (legend/marker only)
            if i % 2 == 0: 
                if "marker" in trace:
                    trace["marker"]["color"] = self.line_color  # Match the line color
                    trace["marker"]["size"] = 7

            # Second trace (actual data)
            if i % 2 == 1:  
                if "line" not in trace:
                    trace["line"] = {}
                trace["line"]["color"] = self.line_color
                trace["line"]["width"] = self.line_width
                trace["line"]["dash"] = self.line_style
                if "marker" in trace:
                    trace["marker"]["color"] = self.line_color

        # Ensure the graph fully redraws
        figure["layout"]["uirevision"] = None

        return dcc.Graph(className='graph', id={'type': 'graph','index': self.index}, style=graph_style, 
                             figure=getattr(figs, self.chain)(self.quantity, self.dataset, self.colorbar, self.wigner, self.proton, self.neutron, \
                                                              self.nucleon, self.range, self.uncertainty, self.even_even))
