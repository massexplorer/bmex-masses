import time
import numpy as np
import math
from datetime import date, datetime
import json
import plotly.express as px
import plotly.graph_objects as go
import base64, io
import zipfile
import plotly.io as pio
import sqlite3 as sl

import dash
from dash import dcc, ALL, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_breakpoints import WindowBreakpoints

from utils.bmex_views import *
from utils.views_class import View
from utils.sidebar_class import Sidebar


default = {"dimension": 'landscape', "chain": 'isotopic', "quantity": 'BE', "dataset": ['AME2020'], 
           "colorbar": 'linear', "wigner": [0], "proton": [None], "neutron": [None], "nucleon": [None], 
           "range": {"x": [None, None], "y": [None, None]}, "colorbar_range": [None, None],
           "uncertainty": [False], "estimated": [False]}

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

app.config.suppress_callback_exceptions=True

app.title = "Bayesian Mass Explorer"

server = app.server

app.layout = html.Div(
    children=[
        dcc.Location(id='url', refresh=False),
        WindowBreakpoints(
            id="breakpoints",
            widthBreakpointThresholdsPx=[800, 1700],
            widthBreakpointNames=["sm", "md", "lg"],
        ),
        html.Div(
            className="banner",
            children=[
                html.A(
                    id="logo",
                    children=[
                        html.Img(src=app.get_asset_url("BMEX-logo-beta.png"), id="logo-img")
                    ],
                    href="https://bmex.dev",
                ),
                html.A(
                    id="issues",
                    children=[
                        html.Img(src=app.get_asset_url("Submit-Issues.png"), id="issues-img")
                    ],
                    href="https://github.com/massexplorer/bmex-web/issues/new",             
                )   
            ]
        ),
        html.Div(id='page-content'),
        dcc.Store(id='intermediate-value'),
        dcc.Store(id='intermediate-colorbar-range'),
        html.P(id='placeholder', hidden=True),
        dcc.Store(id='url-store'),
        dcc.Store(id='viewsmemory', storage_type='session', data=json.dumps([default]),),
        dcc.Store(id='triggerGraph', data=json.dumps("update")),
        dcc.ConfirmDialog(id='confirm', message='Warning! Are you sure you want to delete this view?'),
        dcc.ConfirmDialog(id='confirm-reset', message='Warning! Are you sure you want to reset this page?'),
        dcc.Download(id="download-figs"),
    ]
)

@app.callback(
    Output('url-store','data'),
    Output('page-content','children'),
    [Input('url','pathname')]
    )
def display_page(pathname):
    if(pathname[:7] == "/masses"):
        out = masses_view()
    else:
        out = html.Div(
            id="body",
            className="container scalable",
            children=[html.P("How did you get here? Click the banner to make it back to safety!")])
    return pathname, out

@app.callback(
    Output("clipboard", "content"),
    Input("viewsmemory", "data")
)
def link_update(views):   
    # hash = ''.join(rand.choices(string.ascii_letters, k=6))
    # return "https://beta.bmex.dev/masses/"+hash
    cur_views = json.loads(views)
    return "https://beta.bmex.dev/masses/"+base64.urlsafe_b64encode( json.dumps( [list(cur_views[i].values()) for i in range(len(cur_views))] ).encode()).decode()
    # return "https://beta.bmex.dev/masses/"+base64.urlsafe_b64encode(views.encode()).decode()

# @app.callback(
#     Output("placeholder", "hidden"),
#     State("clipboard", "content"),
#     State("viewsmemory", "data"),
#     Input("clipboard", "n_clicks"),  
#     prevent_initial_call=True, 
# )
# def hash_store(link, views, clicks):
#     try:
#         hash = link.split("masses/")[1]
#     except:
#         raise PreventUpdate
#     con = sl.connect('view_hashes.db')
#     with con:
#         try:
#             con.execute("""INSERT INTO hashes (hash, info) VALUES (?,?);""", (hash, views))
#         except:
#             con.execute("""
#                 CREATE TABLE hashes (
#                     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#                     hash TEXT,
#                     info TEXT
#                 );
#             """)
#             con.execute("""INSERT INTO hashes (hash, info) VALUES (?,?);""", (hash, views))


@app.callback(
    Output('confirm', 'displayed'),
    Input({"type": 'delete-button', "index": ALL}, "n_clicks"),
    State("viewsmemory", "data")
)
def display_confirm(delete, json_cur_views):
    try:
        dash.callback_context.triggered_id['type']
    except:
        raise PreventUpdate
    if 'delete-button' == dash.callback_context.triggered_id['type']:
        try:
            if delete[0] > 0:
                l = len(json.loads(json_cur_views))
                if l < 2:
                    pass
                else:
                    return True
        except:
            pass

@app.callback(
    Output('confirm-reset', 'displayed'),
    Input('reset-button', "n_clicks"),
)
def display_reset_confirm(reset):
    try:
        if reset > 0:
            return True
    except:
        pass


@app.callback(
    Output("download-figs", "data"),
    Input("download-button", "n_clicks"),
    State({'type': 'graph','index': ALL}, "figure"),
    State("viewsmemory", "data"),
    prevent_initial_call=True,
)
def download(n_clicks, figures, json_cur_views):
    try:
        n_clicks>0
    except:
        raise PreventUpdate
    cur_views = json.loads(json_cur_views)
    zip_file_name = "BMEX-"+str(date.today().strftime("%b-%d-%Y"))+"_"+str(datetime.now().strftime("%H-%M-%S"))+".zip"
    def write_zip(bytes_io):
        with zipfile.ZipFile(bytes_io, mode="w") as zf:
            # garbage graph to prevent print out
            fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
            fig.write_image("trash_graph.pdf", format="pdf")
            time.sleep(.5)
            for i in range(len(figures)):
                filename = "Fig_"+str(i+1)+".pdf"
                buf = io.BytesIO()
                fig = go.Figure(figures[i])
                pio.full_figure_for_development(fig, warn=False)
                if cur_views[i]['colorbar'] == 'monochrome':
                    fig.update_traces(colorscale=[[0, 'rgb(163, 77, 57)'], [1, 'rgb(255, 200, 170)']])
                if cur_views[i]['colorbar'] == 'diverging':
                    fig.update_traces(colorscale=[[0, 'rgb(0, 0, 255)'], [.5, 'rgb(0, 0, 0)'], [1, 'rgb(255, 0, 0)']])
                    
                fig.update_layout(
                    font={"color": "#000000"}, title=None,
                    xaxis=dict(linecolor='black', showgrid=True,  minor=dict(showgrid=True, gridcolor="#cccccc"),),
                    yaxis=dict(linecolor='black', showgrid=True, minor=dict(showgrid=True, gridcolor="#cccccc"),),
                    plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", 
                    width=46*15, height=35.75*15),

                for trace in fig.data:
                    try:
                        if trace.marker.color == '#ffffff':
                            trace.marker.color = '#000000'
                    except:
                        pass

                fig.write_image(buf, format='pdf', engine="kaleido")
                zf.writestr(filename, buf.getvalue())
    return dcc.send_bytes(write_zip, zip_file_name)


@app.callback(
    [
        Output("viewsmemory", "data"),
        Output("main-tabs", "children"),
        Output("triggerGraph", "data"),
        Output("main-tabs", "value"),
        Output("tabs_output", "children"),
        Output("link-view-checklist", "options"),
        Output("link-view-checklist", "value"),
    ],
    [
        State("viewsmemory", "data"),
        State("main-tabs", "children"),
        State("tabs_output", "children"),
        State({'type': 'graph','index': ALL}, "figure"),
        State('link-view-checklist', 'value'),
        #link
        # Input("link-colorbar-button", "n_clicks"),
        #rescale
        Input({'type': 'rescale-colorbar-button', 'index': ALL}, 'n_clicks'),
        #url
        Input("url-store", "data"),
        #tabs_output
        Input("main-tabs", "value"),
        #relayout_data
        Input({'type': 'graph','index': ALL}, "relayoutData"),
        #new_series
        Input({"type": 'series-button', "index": ALL}, "n_clicks"),
        #series_tabs
        Input({'type': 'series_tabs','index': ALL}, "value"),
        #delete_series
        Input({'type': 'delete-series-button','index': ALL}, "n_clicks"),
        #delete_plot
        Input('confirm', 'submit_n_clicks'),
        #reset_page
        Input('confirm-reset', "submit_n_clicks"),
        #uncertainty-checklist
        Input({'type': 'uncertainty-checklist', 'index': ALL}, 'value'),
        #colorbar-input
        Input({'type': 'cb-input-min', 'index': ALL}, 'value'),
        Input({'type': 'cb-input-max', 'index': ALL}, 'value'),
        #dropdowns
        Input({'type': 'dropdown-dimension', 'index': ALL}, 'value'),
        Input({'type': 'dropdown-1D', 'index': ALL}, 'value'),
        Input({'type': 'dropdown-quantity', 'index': ALL}, 'value'),
        Input({'type': 'dropdown-dataset', 'index': ALL}, 'value'),
        Input({'type': 'input-protons', 'index': ALL}, 'value'),
        Input({'type': 'input-neutrons', 'index': ALL}, 'value'),
        Input({'type': 'input-nucleons', 'index': ALL}, 'value'),
        Input({'type': 'dropdown-colorbar', 'index': ALL}, 'value'),
        Input({'type': 'radio-wigner', 'index': ALL}, 'value'),
    ],
)
def main_update(
    json_cur_views, cur_tabs, cur_sidebar, figures, links, 
    # link_colorbar, 
    rescale_colorbar, url, tab_n, relayout_data, series_button, series_tab, delete_series, delete_button, 
    reset_button, uncer, cb_min, cb_max, dimension, oneD, quantity, dataset, protons, neutrons, nucleons, colorbar, wigner):

    cur_views = json.loads(json_cur_views)
    new_views = cur_views.copy()

    n = int(tab_n[3])
    if len(series_tab) == 0:
        series_n = 1
    else:
        series_n = int(series_tab[0][3])

    #url
    if "url-store" == dash.callback_context.triggered_id:
        if(len(url)>10):
            loaded_list = json.loads(base64.urlsafe_b64decode(url[8:].encode()).decode())
            loaded_views = [{} for i in range(len(loaded_list))]
            for j in range(len(loaded_list)):
                for key, k in zip(default, range(len(default))):
                    loaded_views[j][key] = loaded_list[j][k]
            new_tabs = [dcc.Tab(label=str(i+1),value='tab'+str(i+1),className='custom-tab', selected_className='custom-tab--selected') for i in range(len(loaded_views))]
            if len(new_tabs)<4:
                new_tabs.append(dcc.Tab(label='+', value='tab0', className='custom-tab', selected_className='custom-tab--selected'))
            return  [
                json.dumps(loaded_views), 
                new_tabs,
                json.dumps('update'),
                tab_n,
                Sidebar(loaded_views[n-1], 1, len(new_tabs)).show(),
                ['1'],
                []
            ]
        # if(len(url)>10):
        #     con = sl.connect('view_hashes.db')
        #     hash = url[8:]
        #     with con:
        #         loaded_views = json.loads(list(con.execute("SELECT info FROM hashes WHERE hash == (?)", (hash,)))[0][0])
        #     new_tabs = [dcc.Tab(label=str(i+1),value='tab'+str(i+1),className='custom-tab', selected_className='custom-tab--selected') for i in range(len(loaded_views))]
        #     return  [
        #         json.dumps(loaded_views), 
        #         new_tabs,
        #         json.dumps('update'),
        #         tab_n,
        #         Sidebar(loaded_views[n-1]).show(), 
        #     ]
        else:
            new_tabs = [dcc.Tab(label=str(i+1),value='tab'+str(i+1),className='custom-tab', selected_className='custom-tab--selected') for i in range(len(cur_views))]
            if len(new_tabs)<4:
                new_tabs.append(dcc.Tab(label='+', value='tab0', className='custom-tab', selected_className='custom-tab--selected'))
            checklist = [str(i+1) for i in range(len(cur_views))]
            return  [
                json_cur_views, 
                new_tabs,
                json.dumps("update"),
                tab_n,
                Sidebar(cur_views[n-1], 1, len(new_tabs)).show(),
                checklist,
                []
            ]

    #main-tabs_change
    if "main-tabs" == dash.callback_context.triggered_id:
        new_tabs = cur_tabs.copy()
        update = "dontupdate"
        # add plot
        if n == 0:
            tab_n = "tab"+str(len(cur_tabs))
            update = "update"
            new_views.append(default)
            new_tabs.insert(len(cur_tabs)-1, dcc.Tab(label=str(len(cur_tabs)), value='tab'+str(len(cur_tabs)), className='custom-tab', selected_className='custom-tab--selected'))
            if len(new_tabs)>4:
                new_tabs.pop()
            checklist = [str(i+1) for i in range(len(cur_views)+1)]
        else:
            checklist = [str(i+1) for i in range(len(cur_views))]
            
        return [
            json.dumps(new_views),
            new_tabs,
            json.dumps(update), #graph
            tab_n,
            Sidebar(new_views[n-1], 1, len(new_tabs)).show(),
            checklist,
            links
        ]

    #delete_plot
    if 'confirm' == dash.callback_context.triggered_id:
        n_views = len(cur_views)
        if  n_views > 1:
            new_views.pop(n-1)
            new_tabs = cur_tabs
            if n_views == 4:
                new_tabs.pop(-1)
                new_tabs.append(dcc.Tab(label='+', value='tab0', className='custom-tab', selected_className='custom-tab--selected'))
            else:
                new_tabs.pop(-2)
            checklist = [str(i+1) for i in range(len(cur_views)-1)]
            return [
                json.dumps(new_views), 
                new_tabs,
                json.dumps("update"), #graph
                "tab"+str(len(new_views)),
                Sidebar(new_views[-1], 1, len(new_tabs)).show(),
                checklist,
                links
            ]
        else:
            raise PreventUpdate

    #reset_page
    if "confirm-reset" == dash.callback_context.triggered_id:
        return [
            json.dumps([default]), 
            [dcc.Tab(label="1", value='tab1', className='custom-tab', selected_className='custom-tab--selected'), 
            dcc.Tab(label='+', value='tab0', className='custom-tab', selected_className='custom-tab--selected')],
            json.dumps("update"),
            'tab1',
            Sidebar().show(),
            ['1'],
            []
        ]

    # A function that inputs an array of different data types and only keeps the floats
    def float_array(array):
        return np.array( [array[i] for i in range(len(array)) if type(array[i])==type(1.0)] )
    
    # Match Colorbars
    if "link-colorbar-button" == dash.callback_context.triggered_id:
        mins = np.array( [figures[i]['data'][0]['zmin'] for i in range(len(figures)) if cur_views[i]['dimension']=='landscape'] )
        maxes = np.array( [figures[i]['data'][0]['zmax'] for i in range(len(figures)) if cur_views[i]['dimension']=='landscape'] )
        try:
            minz, maxz = float(min(mins)), float(max(maxes))
        except:
            raise PreventUpdate
        for i in range(len(new_views)):
            new_views[i]['colorbar_range'] = [minz, maxz]
        checklist = [str(i+1) for i in range(len(cur_views))]
        return [
            json.dumps(new_views),
            cur_tabs,
            json.dumps("update"), #graph
            tab_n,
            Sidebar(new_views[n-1], series_n, len(cur_tabs)).show(),
            checklist,
            links
        ]

    try:
        dash.callback_context.triggered_id['type']
    except:
        raise PreventUpdate
    

    # Rescale Individual Plot Colorbar
    if "rescale-colorbar-button" == dash.callback_context.triggered_id['type']:
        if type(rescale_colorbar[0])==type(1):
            x_range, y_range = cur_views[n-1]['range']['x'].copy(), cur_views[n-1]['range']['y'].copy()
            if x_range[0] == None:
                x_range[0] = -999
            if x_range[1] == None:
                x_range[1] = 999
            if y_range[0] == None:
                y_range[0] = -999
            if y_range[1] == None:
                y_range[1] = 999
            xmin, xmax = math.floor(x_range[0])+math.floor(x_range[0])%2, math.ceil(x_range[1])-math.ceil(x_range[1])%2
            ymin, ymax = math.floor(y_range[0])+math.floor(y_range[0])%2, math.ceil(y_range[1])-math.ceil(y_range[1])%2
            x, y = np.array(figures[n-1]['data'][0]['x']), np.array(figures[n-1]['data'][0]['y'])
            xmin_i, xmax_i = int(np.where(x>=xmin)[0][0]), int(np.where(x<=xmax)[0][-1])+1
            ymin_i, ymax_i = int(np.where(y>=ymin)[0][0]), int(np.where(y<=ymax)[0][-1])+1
            values = float_array(np.array(figures[n-1]['data'][0]['z'])[ymin_i:ymax_i, xmin_i:xmax_i].flatten())
            val_min, val_max = np.round(np.min(values),3), np.round(np.max(values),3)
            new_views[n-1]['colorbar_range'] = [val_min, val_max]
            checklist = [str(i+1) for i in range(len(cur_views))]
            return [
                json.dumps(new_views),
                cur_tabs,
                json.dumps("update"), #graph
                tab_n,
                Sidebar(new_views[n-1], series_n, len(cur_tabs)).show(),
                checklist,
                links
            ]
        raise PreventUpdate
    
    # Relayout Data Change
    if "graph" == dash.callback_context.triggered_id['type']:
        for k, view in enumerate(cur_views):
            if view['dimension'] == 'single':
                relayout_data.insert(k, None)
        # Store Relayout Change
        trigger_index = dash.callback_context.triggered_id['index']
        new_data = relayout_data[trigger_index-1]
        if new_data == None:
            raise PreventUpdate
        auto = False
        if new_data == {'dragmode': 'pan'} or new_data == {'dragmode': 'zoom'} or 'autosize' in new_data:
            raise PreventUpdate
        if 'xaxis.autorange' in new_data:
            auto = True
            new_views[trigger_index-1]['range']['x'] = [None, None]
            new_views[trigger_index-1]['range']['y'] = [None, None]
        else:
            try:
                new_xrange = [float(np.round(new_data['xaxis.range[0]'],3)), float(np.round(new_data['xaxis.range[1]'],3))]
                new_views[trigger_index-1]['range']['x'] = new_xrange
            except:
                new_xrange = cur_views[trigger_index-1]['range']['x']
            try:
                new_yrange = [float(np.round(new_data['yaxis.range[0]'],3)), float(np.round(new_data['yaxis.range[1]'],3))]
                new_views[trigger_index-1]['range']['y'] = new_yrange
            except:
                new_yrange = cur_views[trigger_index-1]['range']['y']
            
        #Link Views
        if links != None and str(trigger_index) in links:
            trig_dim = cur_views[trigger_index-1]['dimension']
            if trig_dim == '1D':
                trig_dim = cur_views[trigger_index-1]['chain']
            for link in links:
                if int(link) != trigger_index:
                    if auto:
                        new_views[int(link)-1]['range']['x'] = [None, None]
                        new_views[int(link)-1]['range']['y'] = [None, None]
                    else:
                        link_dim = cur_views[int(link)-1]['dimension']
                        if link_dim == '1D':
                            link_dim = cur_views[int(link)-1]['chain']
                        if (trig_dim[:3]=='iso' and link_dim=='landscape') or (trig_dim=='landscape' and link_dim[:3]=='iso'): # One of each type
                            chain = trig_dim
                            if chain=='landscape':
                                chain = link_dim
                            if chain == 'isotopic':
                                new_views[int(link)-1]['range']['x'] = new_xrange
                            else:
                                if trig_dim[:3]=='iso':
                                    new_views[int(link)-1]['range']['y'] = new_xrange
                                else:
                                    new_views[int(link)-1]['range']['x'] = new_yrange
                        elif (trig_dim!='isotopic' or link_dim!='isotopic') and ((trig_dim=='isotopic' and link_dim[:3]=='iso') or (trig_dim[:3]=='iso' and link_dim=='isotopic')): # 1Ds w/ only one isotopic
                            pass
                        elif trig_dim[:3]=='iso' and link_dim[:3]=='iso': # Both isotopic or both isotonic/baric
                            new_views[int(link)-1]['range']['x'] = new_xrange
                        else:
                            new_views[int(link)-1]['range']['x'] = new_xrange
                            new_views[int(link)-1]['range']['y'] = new_yrange

        checklist = [str(i+1) for i in range(len(cur_views))]
        return [
            json.dumps(new_views),
            cur_tabs,
            json.dumps("update"), #graph
            tab_n,
            Sidebar(new_views[n-1], series_n, len(cur_tabs)).show(),
            checklist,
            links
        ]

    #delete_series
    if 'delete-series-button' == dash.callback_context.triggered_id['type']:
        l = len(cur_views[n-1]['proton'])
        if  l>1:
            new_views = cur_views
            new_views[n-1]['proton'].pop(series_n-1)
            new_views[n-1]['neutron'].pop(series_n-1)
            new_views[n-1]['nucleon'].pop(series_n-1)
            new_views[n-1]['dataset'].pop(series_n-1)
            new_views[n-1]['wigner'].pop(series_n-1)
            new_views[n-1]['uncertainty'].pop(series_n-1)
            checklist = [str(i+1) for i in range(len(cur_views))]
            return [
                json.dumps(new_views), 
                cur_tabs,
                json.dumps("update"), #graph
                tab_n,
                Sidebar(new_views[n-1], series_n-1+math.ceil(abs(series_n-l)/10), len(cur_tabs)).show(),
                checklist,
                links
            ]
        else:
            raise PreventUpdate
    
    #series_tabs
    if "series_tabs" == dash.callback_context.triggered_id['type']:
        checklist = [str(i+1) for i in range(len(cur_views))]
        if series_n==0:
            new_views = cur_views
            new_views[n-1]['proton'].append(default['proton'][0])
            new_views[n-1]['neutron'].append(default['neutron'][0])
            new_views[n-1]['nucleon'].append(default['nucleon'][0])
            new_views[n-1]['dataset'].append(default['dataset'][0])
            new_views[n-1]['wigner'].append(default['wigner'][0])
            new_views[n-1]['uncertainty'].append(default['uncertainty'][0])
            return [
                json.dumps(new_views), 
                cur_tabs,
                json.dumps("update"),
                tab_n,
                Sidebar(new_views[n-1], "new", len(cur_tabs)).show(),
                checklist,
                links
            ]
        return [
            json.dumps(cur_views), 
            cur_tabs,
            json.dumps("noupdate"),
            tab_n,
            Sidebar(cur_views[n-1], series_n, len(cur_tabs)).show(),
            checklist,
            links
        ]
    
    # Colorbar Input
    if "cb-input-min" == dash.callback_context.triggered_id['type']:
        if len(cb_min) > 0:
            new_views[n-1]['colorbar_range'][0] = cb_min[0]
    elif "cb-input-max" == dash.callback_context.triggered_id['type']:
        if len(cb_max) > 0:
            new_views[n-1]['colorbar_range'][1] = cb_max[0]
    # Dropdown Input
    elif "dropdown-dimension" == dash.callback_context.triggered_id['type']:
        new_views[n-1]['dimension'] = dimension[0]
    elif "dropdown-1D" == dash.callback_context.triggered_id['type']:   
        new_views[n-1]['chain'] = oneD[0]
    elif "dropdown-colorbar" == dash.callback_context.triggered_id['type']:
        new_views[n-1]['colorbar'] = colorbar[0]
    elif "radio-wigner" == dash.callback_context.triggered_id['type']:
        new_views[n-1]['wigner'][series_n-1] = wigner[0]
    elif "input-protons" == dash.callback_context.triggered_id['type']:
        new_views[n-1]['proton'][series_n-1] = protons[0]
    elif "input-neutrons" == dash.callback_context.triggered_id['type']:
        new_views[n-1]['neutron'][series_n-1] = neutrons[0]
    elif "input-nucleons" == dash.callback_context.triggered_id['type']:
        new_views[n-1]['nucleon'][series_n-1] = nucleons[0]
    elif "dropdown-quantity" == dash.callback_context.triggered_id['type']:
        new_views[n-1]['quantity'] = quantity[0]
        new_views[n-1]['colorbar_range'] = [None, None]
    elif "dropdown-dataset" == dash.callback_context.triggered_id['type']:
        new_views[n-1]['dataset'][series_n-1] = dataset[0]
    elif "uncertainty-checklist" == dash.callback_context.triggered_id['type']:
        u = bool(len(uncer[0]))
        new_views[n-1]['uncertainty'][series_n-1] = u
    checklist = [str(i+1) for i in range(len(cur_views))]
    return [
        json.dumps(new_views),
        cur_tabs,
        json.dumps("update"),
        tab_n,
        Sidebar(new_views[n-1], series_n, len(cur_tabs)).show(),
        checklist,
        links
    ]



@app.callback(
    Output("div-graphs", "children"),
    Output("div-graphs", "style"),
    [
        Input("triggerGraph", "data"),
        Input("breakpoints", "widthBreakpoint"),
        Input('even-even-checklist', 'value'),
        State("viewsmemory", "data"),  
    ],
)
def graph_output(trigger: str, breakpoint_name: str, even_even: list, json_views: list):  
    if(dash.callback_context.triggered_id != 'triggerGraph' or json.loads(trigger)=="update"):
        views_list = json.loads(json_views)
        graph_styles = []
        if breakpoint_name == "lg" and len(views_list) > 1:
            style = {"display": 'grid', "grid-template-columns": '[c1] 50% [c2] 50% [c3]',
            "grid-template-rows": '[r1] 50% [r2] 50% [r3]', "width": '100%', "height": '39.6vw'}
            for i in range(len(views_list)):
                graph_styles.append({"grid-area": f"r{math.ceil((i+1)/2)} / c{1+i%2} / r{math.ceil((i+1)/2)+1} / c{2+i%2}", \
                                     "width": '27vw', "height": '19.8vw'})
        else:
            style = {"display": 'flex', "width": '100%'}
            graph_styles = [{"width": '48vw', "height": '35.75vw'} for i in range(len(views_list))]
        output = []
        for i in range(len(views_list)): # iterate through dicts in list
            view = View(views_list[i], i+1)
            output.append(view.plot(graph_style=graph_styles[i], even_even=bool(len(even_even))))
        return output, style
    raise PreventUpdate

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)