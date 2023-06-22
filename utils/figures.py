
import plotly.graph_objs as go
import numpy as np
import utils.bmex as bmex
from pickle import dump, load
import pandas as pd
from dash import html

series_colors = ["#e76f51", "#a5b1cd", "#ffffff", "#13c6e9", "#ffc300", "#1eae00", "#ff6692", "#b6e880", "#b624ff"]

def single(quantity, model, Z, N, wigner=[0]):
    Z = Z[0]
    N = N[0]
    W = wigner[0]
    model = model[0]
    if Z==None and N==None:
        return html.P("Please enter a proton and neutron value")
    if quantity == 'All':
        output = []
        qinput = ['BE', 'OneNSE', 'OnePSE', 'TwoNSE', 'TwoPSE', 'AlphaSE', 'TwoNSGap', 'TwoPSGap', 'DoubleMDiff', 'N3PointOED', 'P3PointOED', 'SNESplitting', 'SPESplitting', 'WignerEC', 'BE/A']
        for qs in qinput:
            result, uncer, estimated = bmex.QuanValue(Z,N,model,qs,W,uncertainty=True)
            try:
                result+"a"
            except:
                out_str = bmex.OutputString(qs)+": "+str(result)
                if uncer != None:
                    out_str += " ± "+str(uncer)
                out_str += " MeV"
                if estimated == True:
                    out_str += " (Estimated Value)"
                output.append(html.P(out_str))
            else:
                output.append(html.P(result))
        return html.Div(id="nucleiAll", children=output, style={'font-size':'3rem'})
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
        return html.P(result)

def isotopic(quantity, model, colorbar, wigner, Z, N, A, view_range, uncertainties, even_even):
    layout = go.Layout(font={"color": "#a5b1cd", "size": 14}, title={"text": "Isotopic Chain", "font": {"size": 20}}, 
        plot_bgcolor="#282b38", paper_bgcolor="#282b38", 
        xaxis=dict(title="Neutrons", gridcolor="#646464",title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor="#3C3C3C",)),
        yaxis=dict(title=quantity+' (MeV)', gridcolor="#646464",title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor="#3C3C3C",)),
        )
    traces = []
    for i in range(len(Z)):
        df = bmex.IsotopicChain(Z[i],model[i],quantity,wigner[i]).sort_values(by=['N'])
        if even_even:
            df = df[df['N']%2==0]
        neutrons = df['N']
        # output = np.abs(df[quantity])
        output = df[quantity]
        error_dict = None
        est_str = np.full(len(neutrons), '')
        markers = 'circle'
        if model[i]=='EXP':
            markers = np.array(df['e'+quantity], dtype='U10')
            est_str = markers.copy()
            est_str[markers=='False'], est_str[markers=='True'] = '', 'Estimated'
            markers[markers=='False'], markers[markers=='True'] = 'circle', 'star'
            if uncertainties[i]:
                error_dict = dict(type='data',array=df['u'+quantity],visible=True)
        traces.append(go.Scatter(
            x=neutrons, y=output, mode="lines+markers", name='Z='+str(Z[i])+' | '+str(model[i]), 
            marker={"size": 7, "color": series_colors[i], "symbol": markers, "line": {"width": 0, "color": 'white'}}, 
            line={"width": 1}, error_y=error_dict, customdata=est_str,
            hovertemplate = '<b><i>N</i></b>: %{x}<br>'+'<b><i>'+quantity+'</i></b>: %{y} MeV<br>'+'<b>%{customdata}</b>',
        ))
    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])

def isotonic(quantity, model, colorbar, wigner, Z, N, A, view_range, uncertainties, even_even):
    layout = go.Layout(font={"color": "#a5b1cd", "size": 14}, title={"text": "Isotonic Chain", "font": {"size": 20}}, 
        plot_bgcolor="#282b38", paper_bgcolor="#282b38", 
        xaxis=dict(title="Protons", gridcolor="#646464",title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor="#3C3C3C",)),
        yaxis=dict(title=quantity+' (MeV)', gridcolor="#646464",title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor="#3C3C3C",)), 
        )
    traces = []
    for i in range(len(N)):
        df = bmex.IsotonicChain(N[i],model[i],quantity,wigner[i]).sort_values(by=['Z'])
        if even_even:
            df = df[df['Z']%2==0]
        protons = df['Z']
        output = df[quantity]
        error_dict = None
        est_str = np.full(len(protons), '')
        markers = 'circle'
        if model[i]=='EXP':
            markers = np.array(df['e'+quantity], dtype='U10')
            est_str = markers.copy()
            est_str[markers=='False'], est_str[markers=='True'] = '', 'Estimated'
            markers[markers=='False'], markers[markers=='True'] = 'circle', 'star'
            if uncertainties[i]:
                error_dict = dict(type='data',array=df['u'+quantity],visible=True)
        traces.append(go.Scatter(
            x=protons, y=output, mode="lines+markers", name='N='+str(N[i])+' | '+str(model[i]), 
            marker={"size": 7, "color": series_colors[i], "symbol": markers, "line": {"width": 0, "color": 'white'}}, 
            line={"width": 1}, error_y=error_dict, customdata=est_str,
            hovertemplate = '<b><i>Z</i></b>: %{x}<br>'+'<b><i>'+quantity+'</i></b>: %{y} MeV<br>'+'<b>%{customdata}</b>',
        ))
    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])


def isobaric(quantity, model, colorbar, wigner, N, Z, A, view_range, uncertainties, even_even):
    layout = go.Layout(font={"color": "#a5b1cd", "size": 14}, title={"text": "Isotonic Chain", "font": {"size": 20}}, 
        plot_bgcolor="#282b38", paper_bgcolor="#282b38", 
        xaxis=dict(title="Protons", gridcolor="#646464",title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor="#3C3C3C",)),
        yaxis=dict(title=quantity+' (MeV)', gridcolor="#646464",title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor="#3C3C3C",)),
        )
    traces = []
    for i in range(len(A)):
        df = bmex.IsobaricChain(A[i],model[i],quantity,wigner[i]).sort_values(by=['Z'])
        if even_even:
            df = df[df['Z']%2==0]
        protons = df['Z']
        output = df[quantity]
        error_dict = None
        est_str = np.full(len(protons), '')
        markers = 'circle'
        if model[i]=='EXP':
            markers = np.array(df['e'+quantity], dtype='U10')
            est_str = markers.copy()
            est_str[markers=='False'], est_str[markers=='True'] = '', 'Estimated'
            markers[markers=='False'], markers[markers=='True'] = 'circle', 'star'
            if uncertainties[i]:
                error_dict = dict(type='data',array=df['u'+quantity],visible=True)
        traces.append(go.Scatter(
            x=protons, y=output, mode="lines+markers", name='A='+str(A[i])+' | '+str(model[i]), 
            marker={"size": 7, "color": series_colors[i], "symbol": markers, "line": {"width": 0, "color": 'white'}}, 
            line={"width": 1}, error_y=error_dict, customdata=est_str,
            hovertemplate = '<b><i>Z</i></b>: %{x}<br>'+'<b><i>'+quantity+'</i></b>: %{y} MeV<br>'+'<b>%{customdata}</b>',
        ))
    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])
    

def landscape(quantity, model, colorbar, wigner, Z=None, N=None, A=None, colorbar_range=[None, None], view_range=[None, None], even_even=False, uncertainties=False):
    W = wigner[0]
    model = model[0]
    layout = go.Layout(
            title=dict(text=bmex.OutputString(quantity)+"   |   "+str(model), font=dict(size=15)), font={"color": "#a5b1cd"},
            xaxis=dict(title=dict(text="Neutrons", font=dict(size=12)), gridcolor="#646464", showline=True,  #gridcolor="#2f3445",
            showgrid=True, gridwidth=1, minor=dict(showgrid=True, gridcolor="#3C3C3C",), mirror='ticks', zeroline=False, range=[0,156]),
            yaxis=dict(title=dict(text="Protons", font=dict(size=12)), gridcolor="#646464", showline=True, 
            showgrid=True, gridwidth=1, minor=dict(showgrid=True, gridcolor="#3C3C3C",), mirror='ticks', zeroline=False, range=[0,104]),
            plot_bgcolor="#282b38", paper_bgcolor="#282b38",
            #uirevision=model, width=600, height=440
    )
    step=1
    if even_even:
        step=2
    data, vals_arr2d, uncertainties, estimated = bmex.Landscape(model, quantity, W, step)
    combined_str = np.full_like(vals_arr2d, '')
    if model == 'EXP':
        estimated[estimated==True] = 'E'
        estimated[estimated==False] = ''
        estimated[estimated==None] = ''
        est_str = estimated.copy()
        est_str[est_str=='E'] = 'Estimated'
        combined_str = est_str.copy()
        if quantity == 'BE':
            uncertainties[uncertainties==None] = ''
            for ri in range(len(uncertainties)):
                for ci in range(len(uncertainties[0])):
                    if uncertainties[ri,ci] != '':
                        uncertainties[ri,ci] = "\u00B1"+str(uncertainties[ri,ci])
            
            combined_str = est_str.copy()
            for r in range(len(est_str)):
                for c in range(len(est_str[r])):
                    combined_str[r][c] = uncertainties[r][c] + '<br>' +est_str[r][c]

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

    def cb(colorbar):
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

    traces = [go.Heatmap(
        x=np.arange(0, vals_arr2d.shape[0]*step, step), y=np.arange(-step/2, vals_arr2d.shape[1]*step, step),
        z=vals_arr2d, zmin=minz, zmax=maxz, name = "", colorscale=cb(colorbar), colorbar=dict(title="MeV"), customdata=combined_str,
        hovertemplate = '<b><i>N</i></b>: %{x}<br>'+'<b><i>Z</i></b>: %{y}<br>'+'<b><i>Value</i></b>: %{z}<br>'+'<b>%{customdata}</b>', 
        text=estimated, texttemplate="%{text}",
    )]

    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])


def landscape_diff(quantity, model, colorbar, wigner, Z=None, N=None, A=None, colorbar_range=[None, None], view_range=[None, None], even_even=False):
    W = wigner[0]
    model = model[0]
    layout = go.Layout(
            title=dict(text=bmex.OutputString(quantity)+"   |   "+str(model), font=dict(size=15)), font={"color": "#a5b1cd"},
            xaxis=dict(title=dict(text="Neutrons", font=dict(size=12)), gridcolor="#646464", showline=True,  #gridcolor="#2f3445",
            showgrid=True, gridwidth=1, minor=dict(showgrid=True, gridcolor="#3C3C3C",), mirror='ticks', zeroline=False, range=[0,156]),
            yaxis=dict(title=dict(text="Protons", font=dict(size=12)), gridcolor="#646464", showline=True, 
            showgrid=True, gridwidth=1, minor=dict(showgrid=True, gridcolor="#3C3C3C",), mirror='ticks', zeroline=False, range=[0,104]),
            plot_bgcolor="#282b38", paper_bgcolor="#282b38",
            #uirevision=model, width=600, height=440
    )
    step=1
    if even_even:
        step=2
    data, vals_arr2d, uncertainties, estimated = bmex.Landscape(model, quantity, 0, step)
    data, vals_arr2d_exp, uncertainties, estimated = bmex.Landscape('EXP', quantity, W, step)
    vals_arr2d = vals_arr2d[ : min(len(vals_arr2d_exp),len(vals_arr2d)) , : min(len(vals_arr2d_exp[0]),len(vals_arr2d[0])) ]
    vals_arr2d_exp = vals_arr2d_exp[:len(vals_arr2d),:len(vals_arr2d[0])]
    for r in range(len(vals_arr2d)):
        for c in range(len(vals_arr2d[r])):
            if vals_arr2d_exp[r][c] == None or vals_arr2d[r][c] == None :
                vals_arr2d_exp[r][c] = 0
                vals_arr2d[r][c] = 9999
                estimated[r][c] = None

    vals_arr2d = vals_arr2d - vals_arr2d_exp
    for r in range(len(vals_arr2d)):
        for c in range(len(vals_arr2d[r])):
            if vals_arr2d[r][c] == 9999:
                vals_arr2d[r][c] = None

    estimated[estimated==True] = 'E'
    estimated[estimated==False] = ''
    estimated[estimated==None] = ''
    est_str = estimated.copy()
    est_str[est_str=='E'] = 'Estimated'
    combined_str = est_str.copy()
    if quantity == 'BE':
        uncertainties[uncertainties==None] = ''
        for ri in range(len(uncertainties)):
            for ci in range(len(uncertainties[0])):
                if uncertainties[ri,ci] != '':
                    uncertainties[ri,ci] = "\u00B1"+str(uncertainties[ri,ci])
        
        combined_str = est_str.copy()
        for r in range(len(est_str)):
            for c in range(len(est_str[r])):
                combined_str[r][c] = uncertainties[r][c] + '<br>' +est_str[r][c]

    

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

    def cb(colorbar):
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

    traces = [go.Heatmap(
        x=np.arange(0, vals_arr2d.shape[0]*step, step), y=np.arange(-step/2, vals_arr2d.shape[1]*step, step),
        z=vals_arr2d, zmin=minz, zmax=maxz, name = "", colorscale=cb(colorbar), colorbar=dict(title="MeV"), customdata=combined_str,
        hovertemplate = '<b><i>N</i></b>: %{x}<br>'+'<b><i>Z</i></b>: %{y}<br>'+'<b><i>Value</i></b>: %{z}<br>'+'<b>%{customdata}</b>', 
        text=estimated, texttemplate="%{text}",
    )]

    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])


def isotopic_diff(quantity, model, colorbar, wigner, Z, N, A, view_range, uncertainties, even_even):
    layout = go.Layout(font={"color": "#a5b1cd", "size": 14}, title={"text": "Model/EXP Diff Isotopic Chain", "font": {"size": 20}}, 
        plot_bgcolor="#282b38", paper_bgcolor="#282b38", 
        xaxis=dict(title="Neutrons", gridcolor="#646464",title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor="#3C3C3C",)),
        yaxis=dict(title='\u0394'+quantity+' (MeV)', gridcolor="#646464",title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor="#3C3C3C",)),
        )
    traces = []
   
    for i in range(len(Z)):
        exp = bmex.IsotopicChain(Z[i],'EXP',quantity,wigner[i]).sort_values(by=['N'])
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
        if model[i]=='EXP':
            markers = np.array(df['e'+quantity], dtype='U10')
            est_str = markers.copy()
            est_str[markers=='False'], est_str[markers=='True'] = '', 'Estimated'
            markers[markers=='False'], markers[markers=='True'] = 'circle', 'star'
            if uncertainties[i]:
                error_dict = dict(type='data',array=df['u'+quantity],visible=True)
        traces.append(go.Scatter(
            x=neutrons, y=output, mode="lines+markers", name='Z='+str(Z[i])+' | '+str(model[i])+'<br>avg: '+str(round(np.mean(abs(output)), 2)),
            marker={"size": 7, "color": series_colors[i], "symbol": markers, "line": {"width": 0, "color": 'white'}}, 
            line={"width": 1}, error_y=error_dict, customdata=est_str,
            hovertemplate = '<b><i>N</i></b>: %{x}<br>'+'<b><i>'+quantity+'</i></b>: %{y} MeV<br>'+'<b>%{customdata}</b>',
        ))
    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])

def isotonic_diff(quantity, model, colorbar, wigner, Z, N, A, view_range, uncertainties, even_even):
    layout = go.Layout(font={"color": "#a5b1cd", "size": 14}, title={"text": "Model/EXP Diff Isotonic Chain", "font": {"size": 20}}, 
        plot_bgcolor="#282b38", paper_bgcolor="#282b38", 
        xaxis=dict(title="Protons", gridcolor="#646464",title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor="#3C3C3C",)),
        yaxis=dict(title='\u0394'+quantity+' (MeV)', gridcolor="#646464",title_font_size=16, showline=True,mirror='ticks',
                   minor=dict(showgrid=True, gridcolor="#3C3C3C",)), 
        )
    traces = []
    for i in range(len(N)):
        exp = bmex.IsotonicChain(N[i],'EXP',quantity,wigner[i]).sort_values(by=['Z'])
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
        if model[i]=='EXP':
            markers = np.array(df['e'+quantity], dtype='U10')
            est_str = markers.copy()
            est_str[markers=='False'], est_str[markers=='True'] = '', 'Estimated'
            markers[markers=='False'], markers[markers=='True'] = 'circle', 'star'
            if uncertainties[i]:
                error_dict = dict(type='data',array=df['u'+quantity],visible=True)
        traces.append(go.Scatter(
            x=protons, y=output, mode="lines+markers", name='N='+str(N[i])+' | '+str(model[i])+'<br>avg: '+str(round(np.mean(abs(output)), 2)), 
            marker={"size": 7, "color": series_colors[i], "symbol": markers, "line": {"width": 0, "color": 'white'}}, 
            line={"width": 1}, error_y=error_dict, customdata=est_str,
            hovertemplate = '<b><i>Z</i></b>: %{x}<br>'+'<b><i>'+quantity+'</i></b>: %{y} MeV<br>'+'<b>%{customdata}</b>',
        ))
    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])