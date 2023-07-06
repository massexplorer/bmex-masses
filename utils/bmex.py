import numpy as np
import pandas as pd
import math

db = 'data/7-3-23.h5'
Wstring = {0: '', 1: '_W1', 2: '_W2'}

# Retrieves single value
def QuanValue(Z,N,model,quan,W=0,uncertainty=False):
    df = pd.read_hdf(db, model)
    try:
        if uncertainty and model=='AME2020':
            v = np.round(df[(df["N"]==N) & (df["Z"]==Z)][quan+Wstring[W]].values[0],6)
            e = df[(df["N"]==N) & (df["Z"]==Z)]['e'+quan].values[0]
            try:
                u = np.round(df[(df["N"]==N) & (df["Z"]==Z)]['u'+quan].values[0],6)
            except:
                u = None
            return v, u, e
        else:
            return np.round(df[(df["N"]==N) & (df["Z"]==Z)][quan].values[0],6), None, None
    except:
        return "Error: "+str(model)+" data does not have "+OutputString(quan)+" available for Nuclei with N="+str(N)+" and Z="+str(Z), None, None

def Landscape(model,quan,W=0,step=1):
    df = pd.read_hdf(db, model)
    df = df[df["N"]%step==0]
    df = df[df["Z"]%step==0]
    df = df.dropna(subset=[quan+Wstring[W]])
    arr2d = np.full((int(max(df['Z'])//step+1),int(max(df['N'])//step+1)), None)
    for rowi in df.index:
        try:
            arr2d[int(df.loc[rowi,'Z']//step), int(df.loc[rowi,'N']//step)] = np.round(df.loc[rowi,quan+Wstring[W]], 6)
        except:
            continue
    if model=='AME2020':
        uncertainties = np.full((max(df['Z'])//step+1,max(df['N'])//step+1), None)
        estimated = np.full((max(df['Z'])//step+1,max(df['N'])//step+1), 0)
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
    df = df[df["Z"]==Z]
    df = df.dropna(subset=[quan+Wstring[W]])
    if model=='AME2020':
        return df.loc[:, ["N", quan+Wstring[W], "u"+quan, 'e'+quan]]
    return df.loc[:, ["N", quan+Wstring[W]]]

def IsotonicChain(N,model,quan,W=0):
    df = pd.read_hdf(db, model)
    df = df[df["N"]==N]
    df = df.dropna(subset=[quan+Wstring[W]])
    if model=='AME2020':
        return df.loc[:, ["Z", quan+Wstring[W], "u"+quan, 'e'+quan]]
    return df.loc[:, ["Z", quan+Wstring[W]]]

def IsobaricChain(A,model,quan,W=0):
    df = pd.read_hdf(db, model)
    df = df[df["Z"]+df["N"]==A]
    df = df.dropna(subset=[quan+Wstring[W]])
    if model=='AME2020':
        return df.loc[:, ["Z", quan+Wstring[W], "u"+quan, 'e'+quan]]
    return df.loc[:, ["Z", quan+Wstring[W]]]

def OutputString(quantity):
    OutputStringDict = {
        "BE": "Binding Energy",
        "OneNSE": "One Neutron Separation Energy",
        "OnePSE": "One Proton Separation Energy",
        "TwoNSE": "Two Neutron Separation Energy",
        "TwoPSE": "Two Proton Separation Energy",
        "AlphaSE": "Alpha Separation Energy",
        "TwoPSGap": "Two Proton Shell Gap",
        "TwoNSGap": "Two Neutron Shell Gap",
        "DoubleMDiff": "Double Mass Difference",
        "N3PointOED": "Neutron 3-Point Odd-Even Binding Energy Difference",
        "P3PointOED": "Proton 3-Point Odd-Even Binding Energy Difference",
        "SNESplitting": "Single Neutron Energy Splitting",
        "SPESplitting": "Single Proton Energy Splitting",
        "WignerEC": "Wigner Energy Coefficient",
        "BEperA": "Binding Energy per Nucleon",
        "QDB2t": "Quadrupole Deformation Beta2",
        "QDB2n": "Quadrupole Deformation Beta2 N",
        "QDB2p": "Quadrupole Deformation Beta2 P",
        "QDB4t": "Quadrupole Deformation Beta4",
        "QDB4n": "Quadrupole Deformation Beta4 N",
        "QDB4p": "Quadrupole Deformation Beta4 P",
        "FermiN": "Fermi Energy N",
        "FermiP": "Fermi Energy P",
        "PEn": "Pairing Energy N",
        "PEp": "Pairing Energy P",
        "PGn": "Pairing Gap N",
        "PGp": "Pairing Gap P",
        "CPn": "Chemical Potential N",
        "CPp": "Chemical Potential P",
        "RMSradT": "RMS Radius Total",
        "RMSradN": "RMS Radius N",
        "RMSradP": "RMS Radius P",
        "MRadN": "Mass Radius N",
        "MRadP": "Mass Radius P",
        "ChRad": "Charge Radius",
        "NSkin": "Neutron Skin",
        "QMQ2t": "Quad Moment Q2 Total",
        "QMQ2n": "Quad Moment Q2 N",
        "QMQ2p": "Quad Moment Q2 P",
    }
    try:
        return OutputStringDict[quantity]
    except:
        return "Quantity not found!"


