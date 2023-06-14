import colorlover as cl
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import utils.bmex as bmex
from sklearn import metrics
from pickle import dump, load
import tensorflow as tf
from tensorflow.keras import backend as K
import pandas as pd
from dash import html

series_colors = ["#e76f51", "#a5b1cd", "#ffffff", "#13c6e9", "#ffc300", "#1eae00", "#ff6692", "#b6e880"]

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

def isotopic(quantity, model, colorbar, wigner, Z, N, A, view_range, uncertainties):
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
        neutrons = df['N']
        output = df[quantity]
        error_dict = None
        est_str = ''
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

def isotonic(quantity, model, colorbar, wigner, Z, N, A, view_range, uncertainties):
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
        protons = df['Z']
        output = df[quantity]
        error_dict = None
        est_str = ''
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


def isobaric(quantity, model, colorbar, wigner, N, Z, A, view_range, uncertainties):
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
        protons = df['Z']
        output = df[quantity]
        error_dict = None
        est_str = ''
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
    

def landscape(quantity, model, colorbar, wigner, Z=None, N=None, A=None, colorbar_range=[None, None], view_range=[None, None]):
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

    step = 2
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
        x=np.arange(0, vals_arr2d.shape[0]*step, step), y=np.arange(-1, vals_arr2d.shape[1]*step, step),
        z=vals_arr2d, zmin=minz, zmax=maxz, name = "", colorscale=cb(colorbar), colorbar=dict(title="MeV"), customdata=combined_str,
        hovertemplate = '<b><i>N</i></b>: %{x}<br>'+'<b><i>Z</i></b>: %{y}<br>'+'<b><i>Value</i></b>: %{z}<br>'+'<b>%{customdata}</b>', 
        text=estimated, texttemplate="%{text}",
    )]
    # if model == 'EXP':
    #     estimated[estimated=='E'] = 1
    #     estimated[estimated==''] = None
    #     traces.append(go.Heatmap(z=estimated,colorscale=['#000000', '#000000'],
    #                 x=np.arange(0, vals_arr2d.shape[0]*step, step), y=np.arange(-1, vals_arr2d.shape[1]*step, step),
    #                 showscale=False, hoverinfo='skip', xgap=5, ygap=5))

    return go.Figure(data=traces, layout=layout, layout_xaxis_range=view_range['x'], layout_yaxis_range=view_range['y'])




def serve_prediction_plot(
    model, X_train, X_test, y_train, y_test, Z, xx, yy, mesh_step, threshold
):
    # Get train and test score from model
    y_pred_train = (model.decision_function(X_train) > threshold).astype(int)
    y_pred_test = (model.decision_function(X_test) > threshold).astype(int)
    train_score = metrics.accuracy_score(y_true=y_train, y_pred=y_pred_train)
    test_score = metrics.accuracy_score(y_true=y_test, y_pred=y_pred_test)

    # Compute threshold
    scaled_threshold = threshold * (Z.max() - Z.min()) + Z.min()
    range = max(abs(scaled_threshold - Z.min()), abs(scaled_threshold - Z.max()))

    # Colorscale
    bright_cscale = [[0, "#ff3700"], [1, "#0b8bff"]]
    cscale = [
        [0.0000000, "#ff744c"],
        [0.1428571, "#ff916d"],
        [0.2857143, "#ffc0a8"],
        [0.4285714, "#ffe7dc"],
        [0.5714286, "#e5fcff"],
        [0.7142857, "#c8feff"],
        [0.8571429, "#9af8ff"],
        [1.0000000, "#20e6ff"],
    ]

    # Create the plot
    # Plot the prediction contour of the SVM
    trace0 = go.Contour(
        x=np.arange(xx.min(), xx.max(), mesh_step),
        y=np.arange(yy.min(), yy.max(), mesh_step),
        z=Z.reshape(xx.shape),
        zmin=scaled_threshold - range,
        zmax=scaled_threshold + range,
        hoverinfo="none",
        showscale=False,
        contours=dict(showlines=False),
        colorscale=cscale,
        opacity=0.9,
    )

    # Plot the threshold
    trace1 = go.Contour(
        x=np.arange(xx.min(), xx.max(), mesh_step),
        y=np.arange(yy.min(), yy.max(), mesh_step),
        z=Z.reshape(xx.shape),
        showscale=False,
        hoverinfo="none",
        contours=dict(
            showlines=False, type="constraint", operation="=", value=scaled_threshold
        ),
        name=f"Threshold ({scaled_threshold:.3f})",
        line=dict(color="#708090"),
    )

    # Plot Training Data
    trace2 = go.Scatter(
        x=X_train[:, 0],
        y=X_train[:, 1],
        mode="markers",
        name=f"Training Data (accuracy={train_score:.3f})",
        marker=dict(size=10, color=y_train, colorscale=bright_cscale),
    )

    # Plot Test Data
    trace3 = go.Scatter(
        x=X_test[:, 0],
        y=X_test[:, 1],
        mode="markers",
        name=f"Test Data (accuracy={test_score:.3f})",
        marker=dict(
            size=10, symbol="triangle-up", color=y_test, colorscale=bright_cscale
        ),
    )

    layout = go.Layout(
        xaxis=dict(ticks="", showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(ticks="", showticklabels=False, showgrid=False, zeroline=False),
        hovermode="closest",
        legend=dict(x=0, y=-0.01, orientation="h"),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"},
    )

    data = [trace0, trace1, trace2, trace3]
    figure = go.Figure(data=data, layout=layout)

    return figure

def isotope_chain_go(Z, NRange, model, axis_label, func):

    output = []

    for i in NRange:
        output.append(func(i, Z, model))

    trace0 = go.Scatter(
        x=NRange, y=output, mode="lines", name="Test Data", marker={"color": "#13c6e9"}
    )

    layout = go.Layout(
        #title=f"ROC Curve (AUC = {auc_score:.3f})",
        title=f"Isotopic Chain",
        xaxis=dict(title="Neutrons", gridcolor="#2f3445"),
        yaxis=dict(title=axis_label, gridcolor="#2f3445"),
        #legend=dict(x=0, y=1.05, orientation="h"),
        #margin=dict(l=100, r=10, t=25, b=40),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"},
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure

def R2(y_true, y_pred):
    SS_res =  K.sum(K.square( y_true-y_pred )) 
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) ) 
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

def PESpredict_single(A, Z, Q20, Q30, model, scaler):

    X = np.zeros(4)
    X[0] = A
    X[1] = Z
    X[2] = Q20
    X[3] = Q30
    xx = scaler.transform(X.reshape(1,-1))
    pes=model.predict(xx)
    
    return pes.T.squeeze()

def PESpredict(X, model, scaler):

    xx = scaler.transform(X)
    pes=model.predict(xx)
    
    return pes.T.squeeze()

def pesnet_surface(N, Z):

    model = tf.keras.models.load_model('utils/PESNet.model',custom_objects={'R2':R2})
    xscaler = load( open( 'utils/xscaler.pkl', "rb" ) )

    An = N+Z
    q20num = 121
    q30num = 21
    Q20 = np.linspace(0,250,q20num)
    Q30 = np.linspace(0,60,q30num)
    Q20v, Q30v = np.meshgrid(Q20,Q30, indexing='ij')
    Q20v = Q20v.flatten()
    Q30v = Q30v.flatten()
    Av = np.zeros(Q20v.shape)
    Zv = np.zeros(Q20v.shape)
    Av[:] = An
    Zv[:] = Z
    #xx = (Q20,Q30)
    #PESv = np.vectorize(PESpredict)
    #pes = PESv(A, Z, Q20v, Q30v, model, xscaler)
    X=(Av,Zv,Q20v,Q30v)
    X = np.asarray(X)
    X = X.T

    pes = np.reshape(PESpredict(X,model,xscaler),(q20num,q30num)).T

    layout = go.Layout(
        #title=f"ROC Curve (AUC = {auc_score:.3f})",
        title=f"PESnet Prediction",
        xaxis=dict(title="Q20", gridcolor="#2f3445",title_font_size=14),
        yaxis=dict(title="Q30", gridcolor="#2f3445",title_font_size=14),
        #legend=dict(x=0, y=1.05, orientation="h"),
        #margin=dict(l=100, r=10, t=25, b=40),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd", "size": 28},
    )

    fig = go.Figure(data =
    go.Contour(
        z=pes,
        x=Q20, # horizontal axis
        y=Q30, # vertical axis
        colorscale="Spectral_r",
    ),layout=layout)
    return fig

def true_surface(df, N, Z):

    An = N+Z
    q20num = 126
    q30num = 21
    Q20 = np.linspace(0,250,q20num)
    Q30 = np.linspace(0,60,q30num)
    Q20v, Q30v = np.meshgrid(Q20,Q30, indexing='ij')
    Q20v = Q20v.flatten()
    Q30v = Q30v.flatten()
    Av = np.zeros(Q20v.shape)
    Zv = np.zeros(Q20v.shape)
    Av[:] = An
    Zv[:] = Z
    #xx = (Q20,Q30)
    #PESv = np.vectorize(PESpredict)
    #pes = PESv(A, Z, Q20v, Q30v, model, xscaler)
    PES_sub = df[(df['A'] == An) & (df['Z'] == Z)]

    A = PES_sub['A']
    Z = PES_sub['Z']
    #Q20 = PES_sub['Q20']
    #Q30 = PES_sub['Q30']
    E = PES_sub['HFB_cubic']



    layout = go.Layout(
        #title=f"ROC Curve (AUC = {auc_score:.3f})",
        title=f"True PES",
        xaxis=dict(title="Q20", gridcolor="#2f3445",title_font_size=14),
        yaxis=dict(title="Q30", gridcolor="#2f3445",title_font_size=14),
        #legend=dict(x=0, y=1.05, orientation="h"),
        #margin=dict(l=100, r=10, t=25, b=40),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd", "size": 28},
    )

    fig = go.Figure(data =
    go.Contour(
        z=np.reshape(E.to_numpy(),(q20num,q30num)).T,
        x=Q20, # horizontal axis
        y=Q30, # vertical axis
        colorscale="Spectral_r",
    ),layout=layout)
    return fig

def isotope_chain_gp(Z, NRange, model, axis_label, func):

    output = []

    layout = go.Layout(
        #title=f"ROC Curve (AUC = {auc_score:.3f})",
        title=f"Isotopic Chain",
        xaxis=dict(title="Neutrons", gridcolor="#2f3445",title_font_size=14),
        yaxis=dict(title=axis_label, gridcolor="#2f3445",title_font_size=14),
        #legend=dict(x=0, y=1.05, orientation="h"),
        #margin=dict(l=100, r=10, t=25, b=40),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd", "size": 14},
    )

    N = bmex.df[(bmex.df["Z"]==Z) & (bmex.df["Model"]=="Exp") & (bmex.df["N"] >= NRange[0]) & (bmex.df["N"] <= NRange[1])]["N"]
    plotFRDMGP,plotFRDMGPBandplus,plotFRDMGPBandminus = func(model[0],model[1],model[2],Z)

    trace0 = go.Scatter(
        x=N, y=plotFRDMGP, mode="lines+markers", name="Test Data", marker=\
            {
                "color": "#13c6e9",
                #"size": 20,
            }
    )

    #figure = px.line(x=Z, y=output, markers=True)
    data = [trace0]
    figure = go.Figure([
        go.Scatter(
            x=plotFRDMGP.T[0],
            y=plotFRDMGP.T[1],
            line=dict(color='rgb(100,100,80)'),
            mode='lines'
        ),
        go.Scatter(
            x=plotFRDMGP.T[0]+plotFRDMGP.T[0][::-1], # x, then x reversed
            y=plotFRDMGPBandplus.T[0]+plotFRDMGPBandminus.T[1][::-1], # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(255,0,0)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            #showlegend=False
        )
    ], layout=layout)
    figure.update_xaxes(title_font_size=20)
    figure.update_yaxes(title_font_size=20)
    figure.update_layout(title_font_size=24)
    return figure

def isotone_chain_go(N, ZRange, model, axis_label, func):

    output = []

    for i in ZRange:
        output.append(func(N, i, model))

    trace0 = go.Scatter(
        x=ZRange, y=output, mode="lines", name="Test Data", marker={"color": "#13c6e9"}
    )

    layout = go.Layout(
        #title=f"ROC Curve (AUC = {auc_score:.3f})",
        title=f"Isotonic Chain",
        xaxis=dict(title="Protons", gridcolor="#2f3445"),
        yaxis=dict(title=axis_label, gridcolor="#2f3445"),
        #legend=dict(x=0, y=1.05, orientation="h"),
        #margin=dict(l=100, r=10, t=25, b=40),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"},
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure
    
def serve_pie_confusion_matrix(model, X_test, y_test, Z, threshold):
    # Compute threshold
    scaled_threshold = threshold * (Z.max() - Z.min()) + Z.min()
    y_pred_test = (model.decision_function(X_test) > scaled_threshold).astype(int)

    matrix = metrics.confusion_matrix(y_true=y_test, y_pred=y_pred_test)
    tn, fp, fn, tp = matrix.ravel()

    values = [tp, fn, fp, tn]
    label_text = ["True Positive", "False Negative", "False Positive", "True Negative"]
    labels = ["TP", "FN", "FP", "TN"]
    blue = cl.flipper()["seq"]["9"]["Blues"]
    red = cl.flipper()["seq"]["9"]["Reds"]
    colors = ["#13c6e9", blue[1], "#ff916d", "#ff744c"]

    trace0 = go.Pie(
        labels=label_text,
        values=values,
        hoverinfo="label+value+percent",
        textinfo="text+value",
        text=labels,
        sort=False,
        marker=dict(colors=colors),
        insidetextfont={"color": "white"},
        rotation=90,
    )

    layout = go.Layout(
        title="Confusion Matrix",
        margin=dict(l=50, r=50, t=100, b=10),
        legend=dict(bgcolor="#282b38", font={"color": "#a5b1cd"}, orientation="h"),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"},
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure
