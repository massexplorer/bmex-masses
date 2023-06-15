import numpy as np
import pandas as pd
import math

db = 'data/6-14-23.h5'

# Retrieves single value
def QuanValue(Z,N,model,quan,W=0,uncertainty=False):
    df = pd.read_hdf(db, model)
    try:
        if uncertainty and model=='EXP':
            v = np.round(float(df[(df["N"]==N) & (df["Z"]==Z) & (df["Wigner"]==W)][quan]),6)
            e = df[(df["N"]==N) & (df["Z"]==Z) & (df["Wigner"]==W)]['e'+quan].values[0]
            try:
                u = np.round(float(df[(df["N"]==N) & (df["Z"]==Z) & (df["Wigner"]==W)]['u'+quan]),6)
            except:
                u = None
            return v, u, e
        else:
            return np.round(float(df[(df["N"]==N) & (df["Z"]==Z) & (df["Wigner"]==W)][quan]),6), None, None
    except:
        return "Error: "+str(model)+" data does not have "+OutputString(quan)+" available for Nuclei with N="+str(N)+" and Z="+str(Z), None, None

def Landscape(model,quan,W=0,step=2):
    df = pd.read_hdf(db, model)
    df = df[df["Wigner"]==W]
    df = df[df["N"]%step==0]
    df = df[df["Z"]%step==0]
    arr2d = np.full((int(max(df['Z'])//step+1),int(max(df['N'])//step+1)), None)
    for rowi in df.index:
        try:
            arr2d[int(df.loc[rowi,'Z']//step), int(df.loc[rowi,'N']//step)] = np.round(df.loc[rowi,quan], 6)
        except:
            continue
    if model=='EXP':
        uncertainties = np.full((max(df['Z'])//step+1,max(df['N'])//step+1), None)
        estimated = np.full((max(df['Z'])//step+1,max(df['N'])//step+1), None)
        for rowi in df.index:
            try:
                uncertainties[df.loc[rowi,'Z']//step, df.loc[rowi,'N']//step] = np.round(df.loc[rowi,'u'+quan], 6)
            except:
                pass
            try:
                estimated[df.loc[rowi,'Z']//step, df.loc[rowi,'N']//step] = df.loc[rowi,'e'+quan]
            except:
                    pass
        return df, arr2d, uncertainties, estimated
    return df, arr2d, None, None

def IsotopicChain(Z,model,quan,W=0):
    df = pd.read_hdf(db, model)
    df = df[df["Wigner"]==W]
    df = df[df["Z"]==Z]
    df = df.dropna(subset=[quan])
    if model=='EXP':
        return df.loc[:, ["N", quan, "u"+quan, 'e'+quan]]
    return df.loc[:, ["N", quan]]

def IsotonicChain(N,model,quan,W=0):
    df = pd.read_hdf(db, model)
    df = df[df["Wigner"]==W]
    df = df[df["N"]==N]
    if model=='EXP':
        return df.loc[:, ["Z", quan, "u"+quan, 'e'+quan]]
    return df.loc[:, ["Z", quan]]

def IsobaricChain(A,model,quan,W=0):
    df = pd.read_hdf(db, model)
    df = df[df["Wigner"]==W]
    df = df[df["Z"]+df["N"]==A]
    if model=='EXP':
        return df.loc[:, ["Z", quan, "u"+quan, 'e'+quan]]
    return df.loc[:, ["Z", quan]]

def OutputString(quantity):
    out_str = "Quantity not found!"
    if (quantity == "BE"):
        out_str = "Binding Energy"
    elif (quantity == "OneNSE"):
        out_str = "One Neutron Separation Energy"
    elif (quantity == "OnePSE"):
        out_str = "One Proton Separation Energy"
    elif (quantity == "TwoNSE"):
        out_str = "Two Neutron Separation Energy"
    elif (quantity == "TwoPSE"):
        out_str = "Two Proton Separation Energy"
    elif (quantity == "AlphaSE"):
        out_str = "Alpha Separation Energy"
    elif (quantity == "TwoPSGap"):
        out_str = "Two Proton Shell Gap"
    elif (quantity == "TwoNSGap"):
        out_str = "Two Neutron Shell Gap"
    elif (quantity == "DoubleMDiff"):
        out_str = "Double Mass Difference"
    elif (quantity == "N3PointOED"):
        out_str = "Neutron 3-Point Odd-Even Binding Energy Difference"
    elif (quantity == "P3PointOED"):
        out_str = "Proton 3-Point Odd-Even Binding Energy Difference"
    elif (quantity == "SNESplitting"):
        out_str = "Single-Neutron Energy Splitting"
    elif (quantity == "SPESplitting"):
        out_str = "Single-Proton Energy Splitting"
    elif (quantity == "WignerEC"):
        out_str = "Wigner Energy Coefficient"
    elif (quantity == "QDB2t"):
        out_str = "Quad Def Beta2"
    elif (quantity == "BE/A"):
        out_str = "Binding Energy per Nucleon"
    return out_str

