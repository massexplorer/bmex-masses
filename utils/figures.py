import plotly.graph_objs as go
import numpy as np
import utils.bmex as bmex
from pickle import dump, load
import pandas as pd
from dash import html
import periodictable

series_colors = ["#e76f51", "#a5b1cd",  "#13c6e9", "#ffc300", "#1eae00", \
                 "#ff00ff", "#b6e880", "#b366ff", "#e33636", "#ba1160", "#327d80", "#ffffff",]
Wstring = {0: '', 1: '_W1', 2: '_W2'}
grid_color = "#a8a8a8"
minor_grid_color = "#646464"
units = {'BE': 'MeV', 'OneNSE': 'MeV', 'OnePSE': 'MeV', 'TwoNSE': 'MeV', 'TwoPSE': 'MeV', 'AlphaSE': 'MeV', 'TwoNSGap': 'MeV',\
         'TwoPSGap': 'MeV', 'DoubleMDiff': 'MeV', 'N3PointOED': 'MeV', 'P3PointOED': 'MeV', 'SNESplitting': 'MeV',\
         'SPESplitting': 'MeV', 'WignerEC': 'MeV', 'BEperA': 'MeV', 'AlphaDecayQValue': 'MeV', "BetaMinusDecay": "MeV", "BetaPlusDecay": "MeV", "MassExcess":"MeV","ElectronCaptureQValue": "MeV", "QDB2t": "", "QDB2n": "", "QDB2p": "", "QDB4t": "",\
        "QDB4n": "", "QDB4p": "", "FermiN": "MeV","FermiP": "MeV", "PEn": "MeV", "PEp": "MeV", "PGn": "MeV", "PGp": "MeV",\
        "CPn": "MeV", "CPp": "MeV", "RMSradT": "fm", "RMSradN": "fm", "RMSradP": "fm", "MRadN": "fm", "MRadP": "fm",\
        "ChRad": "fm", "NSkin": "fm", "QMQ2t": "fm\u00B2", "QMQ2n": "fm\u00B2", "QMQ2p": "fm\u00B2",}

def cb(colorbar, filtered=None, maxz=None):
    if(colorbar == 'linear'):
        return [
            [0, 'rgb(0, 0, 0)'],
            [.01, 'rgb(127, 0, 255)'],
            [.2, 'rgb(0, 0, 255)'],      
            [.39, 'rgb(0, 255, 127)'],
            [.58, 'rgb(127, 255, 0)'],
            [.76, 'rgb(255, 255, 0)'],
            [.95, 'rgb(255, 128, 0)'],
            [1, 'rgb(255, 0, 0)'],
        ]
    elif(colorbar == 'extended_linear'):
        return [
            [0, 'rgb(50, 0, 100)'],
            [.0005, 'rgb(127, 0, 255)'],
            [.1, 'rgb(0, 0, 255)'],      
            [.195, 'rgb(0, 255, 127)'],
            [.29, 'rgb(127, 255, 0)'],
            [.38, 'rgb(255, 255, 0)'],
            [.475, 'rgb(255, 128, 0)'],
            [.5, 'rgb(255, 0, 0)'],
            [.625, 'rgb(75, 0, 0)'], #dark red
            [.75, 'rgb(139, 69, 19)'], #brown
            [.875, 'rgb(100, 100, 100)'], #gray
            [1, 'rgb(200, 200, 200)'], #light gray
        ]
    elif(colorbar == 'equal'):
        equalized_color = filtered[filtered>=0]
        equalized_color = equalized_color[equalized_color<=maxz]
        range_z = max(equalized_color) - min(equalized_color)
        scale = (np.percentile(equalized_color, [19*x for x in range(1,6)]))/range_z
        return [
        [0, 'rgb(0, 0, 0)'],
        [.01, 'rgb(127, 0, 255)'],
        [scale[0], 'rgb(0, 0, 255)'],      
        [scale[1], 'rgb(0, 255, 127)'],
        [scale[2], 'rgb(127, 255, 0)'],
        [scale[3], 'rgb(255, 255, 0)'],
        [scale[4], 'rgb(255, 128, 0)'],
        [1, 'rgb(255, 0, 0)'],
        ]
    elif(colorbar == 'monochrome'):
        return  [[0, 'rgb(230, 120, 85)'], [1, 'rgb(255, 255, 255)']]
    elif(colorbar == 'diverging'):
        return  [[0, 'rgb(0, 0, 255)'], [.5, 'rgb(255, 255, 255)'], [1, 'rgb(255, 0, 0)']]

def single(quantity, model, Z, N, wigner=[0]):
    Z, N, W, model = Z[0], N[0], wigner[0], model[0]
    
        
    if Z==None or N==None:
        return html.P("Please enter a proton and neutron value")
    if quantity == 'All':
        qinput = ['BE', 'OneNSE', 'OnePSE', 'TwoNSE', 'TwoPSE', 'AlphaSE', 'TwoNSGap', 'TwoPSGap', \
                    'DoubleMDiff', 'N3PointOED', 'P3PointOED', 'SNESplitting', 'SPESplitting', 'WignerEC', 'BEperA', 'BetaQValue']
        output = []
        for qs in qinput:
            result, 2, estimated == bmex.QuanValue(Z,N,model,qs,W,uncertainty=True)
            if type(result) == str:
                output.append(html.P(result))
            else:
                if result == np.nan or result == None or str(result) == 'nan':
                    out_str = bmex.OutputString(qs)+": N/A"
                else:
                    out_str = bmex.OutputString(qs)+": "+str(result)
                    if uncer != None:
                        out_str += " ± "+str(uncer)
                    out_str += " "+units[qs]
                    if estimated == True:
                        out_str += " (Estimated Value)"
                output.append(html.P(out_str))
                
        return html.Div(id="nucleiAll", children=output, style={'font-size':'1vw'})
    else:
        result, uncer, estimated = bmex.QuanValue(Z,N,model,quantity,W,uncertainty=True)
        try:
            result+"a"
        except:
            out_str = bmex.OutputString(quantity)+": "+str(result)
            if uncer != None:
                out_str += " ± "+str(uncer)
            out_str += " MeV"
            if estimated == True:
                out_str += " (Estimated Value)"
            return html.P(out_str)
        return html.P(result, style={'font-size':'1vw'})

def isotopic(quantity, model, colorbar, wigner, Z, N, A, view_range, uncertainties, even_even):
    yaxis_unit = '' if units[quantity] == '' else '('+units[quantity]+')'
    layout = go.Layout(font={"color": "#a5b1cd", "size": 14}, title={"text": "Isotopic Chain", "font": {"size": 20}}, 
        plot_bgcolor="#282b38", paper_bgcolor="#282b38", 
        xaxis=dict(title="Neutrons", gridcolor=grid_color,title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor=minor_grid_color,)),
        yaxis=dict(title=quantity+' '+yaxis_unit, gridcolor=grid_color,title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor=minor_grid_color,)),
        )
    traces = []
    for i in range(len(Z)):
        df = bmex.IsotopicChain(Z[i],model[i],quantity,wigner[i]).sort_values(by=['N'])
        if even_even:
            df = df[df['N']%2==0]
        neutrons = df['N']
        output = df[quantity+Wstring[1 if wigner[i]==3 else wigner[i]]]
        error_dict = None
        est_str = np.full(len(neutrons), '')
        markers = 'circle'
        if model[i]=='AME2020':
            markers = np.array(df['e'+quantity], dtype=bool)
            est_str = markers.copy()
            est_str[markers==False], est_str[markers==True] = '', 'Estimated'
            markers[markers==False], markers[markers==True] = 'circle', 'star'
            if uncertainties[i]:
                error_dict = dict(type='data',array=df['u'+quantity],visible=True)
            # Create a hidden scatter trace with circles for the legend
            traces.append(go.Scatter(
                x=[None],y=[None],name='Z='+str(Z[i])+' | '+str(model[i]), mode='lines+markers',
                marker=dict(symbol='circle',size=7, color=series_colors[i])
            ))
        traces.append(go.Scatter(
            x=neutrons, y=output, mode="lines+markers", name='Z='+str(Z[i])+' | '+str(model[i]), 
            marker={"size": 7, "color": series_colors[i], "symbol": markers, "line": {"width": 0, "color": 'white'}}, 
            line={"width": 1}, error_y=error_dict, customdata=est_str,
            hovertemplate = '<b><i>N</i></b>: %{x}<br>'+'<b><i>'+quantity+'</i></b>: %{y} MeV<br>'+'<b>%{customdata}</b>',
            showlegend=False if model[i]=='AME2020' else True
        ))
    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])

def isotonic(quantity, model, colorbar, wigner, Z, N, A, view_range, uncertainties, even_even):
    yaxis_unit = '' if units[quantity] == '' else '('+units[quantity]+')'
    layout = go.Layout(font={"color": "#a5b1cd", "size": 14}, title={"text": "Isotonic Chain", "font": {"size": 20}}, 
        plot_bgcolor="#282b38", paper_bgcolor="#282b38", 
        xaxis=dict(title="Protons", gridcolor=grid_color,title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor=minor_grid_color,)),
        yaxis=dict(title=quantity+' '+yaxis_unit, gridcolor=grid_color,title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor=minor_grid_color,)), 
        )
    traces = []
    for i in range(len(N)):
        df = bmex.IsotonicChain(N[i],model[i],quantity,wigner[i]).sort_values(by=['Z'])
        if even_even:
            df = df[df['Z']%2==0]
        protons = df['Z']
        output = df[quantity+Wstring[1 if wigner[i]==3 else wigner[i]]]
        error_dict = None
        est_str = np.full(len(protons), '')
        markers = 'circle'
        if model[i]=='AME2020':
            markers = np.array(df['e'+quantity], dtype=bool)
            est_str = markers.copy()
            est_str[markers==False], est_str[markers==True] = '', 'Estimated'
            markers[markers==False], markers[markers==True] = 'circle', 'star'
            if uncertainties[i]:
                error_dict = dict(type='data',array=df['u'+quantity],visible=True)
            # Create a hidden scatter trace with circles for the legend
            traces.append(go.Scatter(
                x=[None],y=[None],name='N='+str(N[i])+' | '+str(model[i]), mode='lines+markers',
                marker=dict(symbol='circle',size=7, color=series_colors[i])
            ))
        traces.append(go.Scatter(
            x=protons, y=output, mode="lines+markers", name='N='+str(N[i])+' | '+str(model[i]), 
            marker={"size": 7, "color": series_colors[i], "symbol": markers, "line": {"width": 0, "color": 'white'}}, 
            line={"width": 1}, error_y=error_dict, customdata=est_str,
            hovertemplate = '<b><i>Z</i></b>: %{x}<br>'+'<b><i>'+quantity+'</i></b>: %{y} MeV<br>'+'<b>%{customdata}</b>',
            showlegend=False if model[i]=='AME2020' else True
        ))
    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])


def isobaric(quantity, model, colorbar, wigner, N, Z, A, view_range, uncertainties, even_even):
    yaxis_unit = '' if units[quantity] == '' else '('+units[quantity]+')'
    layout = go.Layout(font={"color": "#a5b1cd", "size": 14}, title={"text": "Isotonic Chain", "font": {"size": 20}}, 
        plot_bgcolor="#282b38", paper_bgcolor="#282b38", 
        xaxis=dict(title="Protons", gridcolor=grid_color,title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor=minor_grid_color,)),
        yaxis=dict(title=quantity+' '+yaxis_unit, gridcolor=grid_color,title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor=minor_grid_color,)),
        )
    traces = []
    for i in range(len(A)):
        df = bmex.IsobaricChain(A[i],model[i],quantity,wigner[i]).sort_values(by=['Z'])
        if even_even:
            df = df[df['Z']%2==0]
        protons = df['Z']
        output = df[quantity+Wstring[1 if wigner[i]==3 else wigner[i]]]
        error_dict = None
        est_str = np.full(len(protons), '')
        markers = 'circle'
        if model[i]=='AME2020':
            markers = np.array(df['e'+quantity], dtype=bool)
            est_str = markers.copy()
            est_str[markers==False], est_str[markers==True] = '', 'Estimated'
            markers[markers==False], markers[markers==True] = 'circle', 'star'
            if uncertainties[i]:
                error_dict = dict(type='data',array=df['u'+quantity],visible=True)
            # Create a hidden scatter trace with circles for the legend
            traces.append(go.Scatter(
                x=[None],y=[None],name='A='+str(A[i])+' | '+str(model[i]), mode='lines+markers',
                marker=dict(symbol='circle',size=7, color=series_colors[i])
            ))
        traces.append(go.Scatter(
            x=protons, y=output, mode="lines+markers", name='A='+str(A[i])+' | '+str(model[i]), 
            marker={"size": 7, "color": series_colors[i], "symbol": markers, "line": {"width": 0, "color": 'white'}}, 
            line={"width": 1}, error_y=error_dict, customdata=est_str,
            hovertemplate = '<b><i>Z</i></b>: %{x}<br>'+'<b><i>'+quantity+'</i></b>: %{y} MeV<br>'+'<b>%{customdata}</b>',
            showlegend=False if model[i]=='AME2020' else True
        ))
    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])
    

def landscape(quantity, model, colorbar, wigner, Z=None, N=None, A=None, colorbar_range=[None, None], view_range={"x": [None, None], "y": [None, None]}, even_even=False, uncertainties=False, SPSadj=False, show_text=False):
    W = wigner[0]
    model = model[0]
    step=1
    if even_even:
        step=2
    data, vals_arr2d, uncertainties, estimated = bmex.Landscape(model, quantity, W, step, SPSadj)
    def get_symbol(z):
        try:
            return periodictable.elements[z].symbol
        except:
            return ""

    combined_str = np.full_like(vals_arr2d, '')
    for z in range(vals_arr2d.shape[0]):
        for n in range(vals_arr2d.shape[1]):
            if vals_arr2d[z, n] is not None:
                symbol = get_symbol(z)

    if model == 'AME2020':
        estimated = np.where(estimated==1, 'E', '')
        est_str = estimated.copy()
        est_str = np.where(estimated=='E', 'Estimated', '')
        combined_str = est_str.copy()

        if quantity == 'BE':
                uncertainties[uncertainties==np.nan] = ''
                for ri in range(len(uncertainties)):
                    for ci in range(len(uncertainties[0])):
                        if uncertainties[ri,ci] != '':
                            uncertainties[ri,ci] = "\u00B1"+str(uncertainties[ri,ci])
                combined_str = [x + '<br>' + y for x, y in zip(uncertainties, est_str)]


    filtered = []
    for e in vals_arr2d.flatten():
        try:
            e + 0.0
        except:
            pass
        else:
            filtered.append(e)
    filtered = np.array(filtered)
    if len(filtered)<5:
        raise Exception
    minz, maxz = colorbar_range[0], colorbar_range[1]
    if minz == None:
        minz = float(min(filtered))
    if maxz == None:
        maxz=float(max(filtered))
        # maxz=float(np.percentile(filtered, [97]))

    if quantity in ['BetaMinusDecay', 'BetaPlusDecay', 'AlphaDecayQValue', 'ElectronCaptureQValue']:
        max_abs_value = max(abs(minz), abs(maxz))
        minz, maxz = -max_abs_value, max_abs_value
        colorscale = [[0, 'rgb(0, 0, 255)'], [0.5, 'rgb(255, 255, 255)'], [1, 'rgb(255, 0, 0)']]
     
    result = []
    for row in vals_arr2d:
        new_row = []
        for value in row:
            if value is None or value >= 0:
                new_row.append(None)
            else:
                new_row.append(-1)
        result.append(new_row)
    negatives = np.array(result)
    estimated = np.where(
    (negatives == -1) & (~np.isin(quantity, ['BetaPlusDecay', 'BetaMinusDecay', 'AlphaDecayQValue', 'ElectronCaptureQValue'])),
    '★',
    estimated if model == 'AME2020' else ''

)
    text_array = np.full_like(vals_arr2d, '', dtype=object)

    for z in range(vals_arr2d.shape[0]):
        for n in range(vals_arr2d.shape[1]):
            if vals_arr2d[z, n] is not None:
                if model == 'AME2020' and estimated[z, n] != '':
                    text_array[z, n] = estimated[z, n]  # E or ★
                else:
                    text_array[z, n] = get_symbol(z)
    texttemplate_val = "%{text}" if show_text else None

    traces = [
        go.Heatmap(
                x=np.arange(0, vals_arr2d.shape[0]*step, step),
                y=np.arange(-step/2, vals_arr2d.shape[1]*step, step),
                z=vals_arr2d,
                zmin=minz,
                zmax=maxz,
                name="",
                colorscale=cb(colorbar, filtered, maxz),
                colorbar=dict(title=units[quantity]),
                customdata=combined_str,
                text=text_array,
                hovertemplate='<b>%{text}</b><br>' +
                            '<b><i>N</i></b>: %{x}<br>' +
                            '<b><i>Z</i></b>: %{y}<br>' +
                            '<b><i>Value</i></b>: %{z}<br>' +
                            '<b>%{customdata}</b>',
                texttemplate=texttemplate_val,
                textfont=dict(color='black'),
            ),

    ]
    layout = go.Layout(
            title=dict(text=bmex.OutputString(quantity)+"   |   "+str(model), font=dict(size=15)), 
            font={"color": "#a5b1cd"},
            xaxis=dict(title=dict(text="Neutrons", font=dict(size=12)), gridcolor=grid_color, showline=True,  
            showgrid=True, gridwidth=1, minor=dict(showgrid=True, gridcolor=minor_grid_color,), mirror='ticks', zeroline=False,
            range=[0,156]),
            yaxis=dict(title=dict(text="Protons", font=dict(size=12)), gridcolor=grid_color, showline=True,   
            showgrid=True, gridwidth=1, minor=dict(showgrid=True, gridcolor=minor_grid_color,), mirror='ticks', zeroline=False, 
            range=[0,104]), #uirevision=model, width=600, height=440
            plot_bgcolor="#282b38", paper_bgcolor="#282b38", yaxis_scaleanchor="x",
    )
    fig = go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])
    xran, yran = fig.layout.xaxis.range, fig.layout.yaxis.range
    for t in [2, 5, 10, 20, 50, 100]:
        try:
            if (xran[1]-xran[0])/9 < t:
                fig.update_layout(xaxis=dict(dtick=t), yaxis=dict(dtick=t))
                break
        except:
            fig.update_layout(xaxis=dict(dtick=20), yaxis=dict(dtick=20))
            break
    return fig


def landscape_diff(quantity, model, colorbar, wigner, Z=None, N=None, A=None, colorbar_range=[None, None], view_range={"x": [None, None], "y": [None, None]}, even_even=False):
    W = wigner[0]
    model = model[0]
    layout = go.Layout(
            title=dict(text=bmex.OutputString(quantity)+"   |   "+str(model)+" - AME2020", font=dict(size=15)), font={"color": "#a5b1cd"},
            xaxis=dict(title=dict(text="Neutrons", font=dict(size=12)), gridcolor=grid_color, showline=True,  #gridcolor="#2f3445",
            showgrid=True, gridwidth=1, minor=dict(showgrid=True, gridcolor=minor_grid_color,), mirror='ticks', zeroline=False, range=[0,156]),
            yaxis=dict(title=dict(text="Protons", font=dict(size=12)), gridcolor=grid_color, showline=True, 
            showgrid=True, gridwidth=1, minor=dict(showgrid=True, gridcolor=minor_grid_color,), mirror='ticks', zeroline=False, range=[0,104]),
            plot_bgcolor="#282b38", paper_bgcolor="#282b38",
            #uirevision=model, width=600, height=440
    )
    step=1
    if even_even:
        step=2
    data, vals_arr2d, uncertainties, estimated = bmex.Landscape(model, quantity, 0, step)
    data, vals_arr2d_exp, uncertainties, estimated = bmex.Landscape('AME2020', quantity, W, step)
    vals_arr2d = vals_arr2d[ : min(len(vals_arr2d_exp),len(vals_arr2d)) , : min(len(vals_arr2d_exp[0]),len(vals_arr2d[0])) ]
    vals_arr2d_exp = vals_arr2d_exp[:len(vals_arr2d),:len(vals_arr2d[0])]
    for r in range(len(vals_arr2d)):
        for c in range(len(vals_arr2d[r])):
            if vals_arr2d_exp[r][c] == None or vals_arr2d[r][c] == None :
                vals_arr2d_exp[r][c] = 0
                vals_arr2d[r][c] = 9999
                estimated[r][c] = 0

    vals_arr2d = vals_arr2d - vals_arr2d_exp
    for r in range(len(vals_arr2d)):
        for c in range(len(vals_arr2d[r])):
            if vals_arr2d[r][c] == 9999:
                vals_arr2d[r][c] = None

    combined_str = np.full_like(vals_arr2d, '')

    estimated = np.where(estimated==1, 'E', '') if model=='AME2020' else ''
    est_str = estimated.copy()
    est_str = np.where(estimated=='E', 'Estimated', '')
    combined_str = est_str.copy()
    if quantity == 'BE':
        uncertainties[uncertainties==np.nan] = ''
        for ri in range(len(uncertainties)):
            for ci in range(len(uncertainties[0])):
                if uncertainties[ri,ci] != '':
                    uncertainties[ri,ci] = "\u00B1"+str(uncertainties[ri,ci])
        combined_str = [x + '<br>' + y for x, y in zip(uncertainties, est_str)]

    filtered = []
    for e in vals_arr2d.flatten():
        try:
            e + 0.0
        except:
            pass
        else:
            filtered.append(e)
    filtered = np.array(filtered)
    if len(filtered)<5:
        raise Exception
    minz, maxz = colorbar_range[0], colorbar_range[1]
    if minz == None:
        minz = 0
    if maxz == None:
        maxz=float(max(filtered))
        # maxz=float(np.percentile(filtered, [97]))

    traces = [go.Heatmap(
        x=np.arange(0, vals_arr2d.shape[0]*step, step), y=np.arange(-step/2, vals_arr2d.shape[1]*step, step),
        z=vals_arr2d, zmin=minz, zmax=maxz, name = "", colorscale=cb(colorbar, filtered, maxz), colorbar=dict(title=units[quantity]), \
        customdata=combined_str, text=estimated, texttemplate="%{text}", textfont=dict(color='black'),
        hovertemplate = '<b><i>N</i></b>: %{x}<br>'+'<b><i>Z</i></b>: %{y}<br>'+'<b><i>Value</i></b>: %{z}<br>'+'<b>%{customdata}</b>', 
    )]

    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])


def isotopic_diff(quantity, model, colorbar, wigner, Z, N, A, view_range, uncertainties, even_even):
    yaxis_unit = '' if units[quantity] == '' else '('+units[quantity]+')'
    layout = go.Layout(font={"color": "#a5b1cd", "size": 14}, title={"text": "Model/EXP Diff Isotopic Chain", "font": {"size": 20}}, 
        plot_bgcolor="#282b38", paper_bgcolor="#282b38", 
        xaxis=dict(title="Neutrons", gridcolor=grid_color,title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor=minor_grid_color,)),
        yaxis=dict(title='\u0394'+quantity+' '+yaxis_unit, gridcolor=grid_color,title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor=minor_grid_color,)),
        )
    traces = []
   
    for i in range(len(Z)):
        exp = bmex.IsotopicChain(Z[i],'AME2020',quantity,wigner[i]).sort_values(by=['N'])
        exp.columns=['N', quantity+'_exp', 'u'+quantity, 'e'+quantity]
        df = bmex.IsotopicChain(Z[i],model[i],quantity,wigner[i]).sort_values(by=['N'])
        master = pd.merge(exp, df, how='inner', on=['N'])
        if even_even:
            master = master[master['N']%2==0]
        neutrons = master['N']
        output = np.array(master[quantity]) - np.array(master[quantity+'_exp'])
        error_dict = None
        est_str = np.full(len(neutrons), '')
        markers = 'circle'
        traces.append(go.Scatter(
            x=neutrons, y=output, mode="lines+markers", name='Z='+str(Z[i])+' | '+str(model[i]),
            marker={"size": 7, "color": series_colors[i], "symbol": markers, "line": {"width": 0, "color": 'white'}}, 
            line={"width": 1}, error_y=error_dict, customdata=est_str,
            hovertemplate = '<b><i>N</i></b>: %{x}<br>'+'<b><i>'+quantity+'</i></b>: %{y} MeV<br>'+'<b>%{customdata}</b>',
            showlegend=False if model[i]=='AME2020' else True
        ))
    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])

def isotonic_diff(quantity, model, colorbar, wigner, Z, N, A, view_range, uncertainties, even_even):
    yaxis_unit = '' if units[quantity] == '' else '('+units[quantity]+')'
    layout = go.Layout(font={"color": "#a5b1cd", "size": 14}, title={"text": "Model/EXP Diff Isotonic Chain", "font": {"size": 20}}, 
        plot_bgcolor="#282b38", paper_bgcolor="#282b38", 
        xaxis=dict(title="Protons", gridcolor=grid_color,title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor=minor_grid_color,)),
        yaxis=dict(title='\u0394'+quantity+' '+yaxis_unit, gridcolor=grid_color,title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor=minor_grid_color,)), 
        )
    traces = []
    for i in range(len(N)):
        exp = bmex.IsotonicChain(N[i],'AME2020',quantity,wigner[i]).sort_values(by=['Z'])
        exp.columns=['Z', quantity+'_exp', 'u'+quantity, 'e'+quantity]
        df = bmex.IsotonicChain(N[i],model[i],quantity,wigner[i]).sort_values(by=['Z'])
        master = pd.merge(exp, df, how='inner', on=['Z'])
        if even_even:
            master = master[master['Z']%2==0]
        protons = master['Z']
        output = np.array(master[quantity]) - np.array(master[quantity+'_exp'])
        error_dict = None
        est_str = np.full(len(protons), '')
        markers = 'circle'
        traces.append(go.Scatter(
            x=protons, y=output, mode="lines+markers", name='N='+str(N[i])+' | '+str(model[i]), 
            marker={"size": 7, "color": series_colors[i], "symbol": markers, "line": {"width": 0, "color": 'white'}}, 
            line={"width": 1}, error_y=error_dict, customdata=est_str,
            hovertemplate = '<b><i>Z</i></b>: %{x}<br>'+'<b><i>'+quantity+'</i></b>: %{y} MeV<br>'+'<b>%{customdata}</b>',
            showlegend=False if model[i]=='AME2020' else True
        ))
    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])