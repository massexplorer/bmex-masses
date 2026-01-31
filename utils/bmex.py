import numpy as np
import pandas as pd
import math

db = 'data/2-27-25.h5'
Wstring = {0: '', 1: '_W1', 2: '_W2'}

def ame_with_bmc_fallback_and_mask(df_ame, df_bmc, cols):
    bmc_cols = [c for c in cols if c in df_bmc.columns]
    if len(bmc_cols) == 0:
        empty = df_ame[['N', 'Z']].copy()
        for c in cols:
            empty['bmc_' + c] = False
        return df_ame, empty

    merged = pd.merge(
        df_ame,
        df_bmc[['N', 'Z'] + bmc_cols],
        on=['N', 'Z'],
        how='outer',
        suffixes=('', '_bmc')
    )

    for c in bmc_cols:
        cb = c + '_bmc'
        merged['bmc_' + c] = merged[c].isna() & merged[cb].notna()

        merged[c] = merged[c].combine_first(merged[cb])
        merged = merged.drop(columns=[cb])

    merged = merged.dropna(subset=['N', 'Z'])

    mask_df = merged[['N', 'Z'] + ['bmc_' + c for c in bmc_cols]].copy()
    return merged, mask_df



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
        return str(model)+" has no "+OutputString(quan)+" available for Nuclei with N="+str(N)+" and Z="+str(Z), None, None

def Landscape(model, quan, W=0, step=1, SPSadj=False, include_bmc=False):
    df = pd.read_hdf(db, model)
    bmc_mask_df = None

    if include_bmc and model == 'AME2020':
        df_bmc = pd.read_hdf(db, 'BMC')
        if W == 3:
            cols = [quan + Wstring[1], quan + Wstring[2]]
        else:
            cols = [quan + Wstring[W]]
        df, bmc_mask_df = ame_with_bmc_fallback_and_mask(df, df_bmc, cols)

    df = df[df["N"]%step==0]
    df = df[df["Z"]%step==0]
    if W == 3:
        df = df.dropna(subset=[quan + Wstring[1], quan + Wstring[2]])
    else:
        df = df.dropna(subset=[quan + Wstring[W]])
    if SPSadj=='N':
        df[quan+Wstring[0]] = df[quan+Wstring[0]]/(41*(df['N']+df['Z'])**(-1/3)*( 1 + (df['N']-df['Z'])/(3*(df['N']+df['Z']))))
        df[quan+Wstring[1]] = df[quan+Wstring[1]]/(41*(df['N']+df['Z'])**(-1/3)*( 1 + (df['N']-df['Z'])/(3*(df['N']+df['Z']))))
        df[quan+Wstring[2]] = df[quan+Wstring[2]]/(41*(df['N']+df['Z'])**(-1/3)*( 1 + (df['N']-df['Z'])/(3*(df['N']+df['Z']))))
    elif SPSadj=='P':
        df[quan+Wstring[0]] = df[quan+Wstring[0]]/(41*(df['N']+df['Z'])**(-1/3)*( 1 - (df['N']-df['Z'])/(3*(df['N']+df['Z']))))
        df[quan+Wstring[1]] = df[quan+Wstring[1]]/(41*(df['N']+df['Z'])**(-1/3)*( 1 - (df['N']-df['Z'])/(3*(df['N']+df['Z']))))
        df[quan+Wstring[2]] = df[quan+Wstring[2]]/(41*(df['N']+df['Z'])**(-1/3)*( 1 - (df['N']-df['Z'])/(3*(df['N']+df['Z']))))
    arr2d = np.full((int(max(df['Z'])//step+1),int(max(df['N'])//step+1)), None)
    for rowi in df.index:
        try:
            if W==3:
                arr2d[int(df.loc[rowi,'Z']//step), int(df.loc[rowi,'N']//step)] = np.round((df.loc[rowi,quan+Wstring[1]]+df.loc[rowi,quan+Wstring[2]])/2, 6)
            else:
                arr2d[int(df.loc[rowi,'Z']//step), int(df.loc[rowi,'N']//step)] = np.round(df.loc[rowi,quan+Wstring[W]], 6)
        except:
            continue
    bmc_used = None
    ### HEREEEEE
    if (include_bmc and model == 'AME2020') and (bmc_mask_df is not None):
        bmc_mask_df = bmc_mask_df.dropna(subset=["N", "Z"])
        bmc_mask_df = bmc_mask_df[(bmc_mask_df["N"] % step == 0) & (bmc_mask_df["Z"] % step == 0)].copy()

        max_z_idx = int(max(df["Z"]) // step)
        max_n_idx = int(max(df["N"]) // step)
        bmc_used = np.full((max_z_idx + 1, max_n_idx + 1), False)

        if W == 3:
            c1 = "bmc_" + (quan + Wstring[1])
            c2 = "bmc_" + (quan + Wstring[2])
            has_c1 = c1 in bmc_mask_df.columns
            has_c2 = c2 in bmc_mask_df.columns

            if has_c1 or has_c2:
                for rowi in bmc_mask_df.index:
                    z = int(bmc_mask_df.loc[rowi, "Z"] // step)
                    n = int(bmc_mask_df.loc[rowi, "N"] // step)

                    if (z < 0) or (n < 0) or (z > max_z_idx) or (n > max_n_idx):
                        continue

                    v = False
                    if has_c1:
                        v = v or bool(bmc_mask_df.loc[rowi, c1])
                    if has_c2:
                        v = v or bool(bmc_mask_df.loc[rowi, c2])
                    bmc_used[z, n] = v
        else:
            c = "bmc_" + (quan + Wstring[W])
            if c in bmc_mask_df.columns:
                for rowi in bmc_mask_df.index:
                    z = int(bmc_mask_df.loc[rowi, "Z"] // step)
                    n = int(bmc_mask_df.loc[rowi, "N"] // step)

                    if (z < 0) or (n < 0) or (z > max_z_idx) or (n > max_n_idx):
                        continue

                    bmc_used[z, n] = bool(bmc_mask_df.loc[rowi, c])


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
        if include_bmc and (bmc_used is not None):
            df_bmc = pd.read_hdf(db, "BMC")
            ucol = "u" + quan

            if ucol in df_bmc.columns:
                df_bmc = df_bmc[(df_bmc["N"] % step == 0) & (df_bmc["Z"] % step == 0)]
                df_bmc = df_bmc.dropna(subset=[ucol])

                max_z = uncertainties.shape[0] - 1
                max_n = uncertainties.shape[1] - 1

                for rowi in df_bmc.index:
                    z = int(df_bmc.loc[rowi, "Z"] // step)
                    n = int(df_bmc.loc[rowi, "N"] // step)

                    if z < 0 or n < 0 or z > max_z or n > max_n:
                        continue

                    if bmc_used[z, n]:
                        uncertainties[z, n] = np.round(df_bmc.loc[rowi, ucol], 6)

        return df, arr2d, uncertainties, estimated, bmc_used
    if model == 'BMC':
        ucol = 'u' + quan
        if ucol in df.columns:
            unc2d = np.full((int(max(df['Z'])//step+1), int(max(df['N'])//step+1)), None)
            for rowi in df.index:
                try:
                    unc2d[int(df.loc[rowi,'Z']//step), int(df.loc[rowi,'N']//step)] = np.round(df.loc[rowi, ucol], 6)
                except:
                    pass
            return df, arr2d, unc2d, None, bmc_used

    return df, arr2d, None, None, bmc_used



def IsotopicChain(Z,model,quan,W=0, include_bmc=False):
    df = pd.read_hdf(db, model)
    ucol = "u" + quan
    if include_bmc and model == 'AME2020':
        df_bmc = pd.read_hdf(db, 'BMC')
        if W == 3:
            cols = [quan + Wstring[1], quan + Wstring[2], ucol]
        else:
            cols = [quan + Wstring[W], ucol]
        df, bmc_mask_df = ame_with_bmc_fallback_and_mask(df, df_bmc, cols)

    # Now filter to the chain
    df = df[df["Z"] == Z].copy()
    if model=='AME2020':
        if W == 3:
            newdf = df.loc[:, ["N", quan+Wstring[1], "u"+quan, 'e'+quan]]
            newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
            return newdf
        return df.loc[:, ["N", quan+Wstring[W], "u"+quan, 'e'+quan]]
    if model=='BMC':
        ucol = "u" + quan
        if W == 3:
            cols = ["N", quan+Wstring[1]]
            if ucol in df.columns:
                cols.append(ucol)
            newdf = df.loc[:, cols]
            newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
            return newdf
        cols = ["N", quan+Wstring[W]]
        if ucol in df.columns:
            cols.append(ucol)
        return df.loc[:, cols]

    if W == 3:
        newdf = df.loc[:, ["N", quan+Wstring[W]]]
        newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
        return df
    return df.loc[:, ["N", quan+Wstring[W]]]

def IsotonicChain(N,model,quan,W=0, include_bmc=False):
    df = pd.read_hdf(db, model)
    ucol = "u" + quan
    if include_bmc and model == 'AME2020':
        df_bmc = pd.read_hdf(db, 'BMC')
        if W == 3:
            cols = [quan + Wstring[1], quan + Wstring[2], ucol]
        else:
            cols = [quan + Wstring[W], ucol]
        df, bmc_mask_df = ame_with_bmc_fallback_and_mask(df, df_bmc, cols)

    df = df[df["N"] == N].copy()
    if model=='AME2020':
        if W == 3:
            newdf = df.loc[:, ["Z", quan+Wstring[1], "u"+quan, 'e'+quan]]
            newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
            return df
        return df.loc[:, ["Z", quan+Wstring[W], "u"+quan, 'e'+quan]]
    if model=='BMC':
        ucol = "u" + quan
        if W == 3:
            cols = ["N", quan+Wstring[1]]
            if ucol in df.columns:
                cols.append(ucol)
            newdf = df.loc[:, cols]
            newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
            return df
        cols = ["Z", quan+Wstring[W]]
        if ucol in df.columns:
            cols.append(ucol)
        return df.loc[:, cols]
    if W == 3:
        newdf = df.loc[:, ["Z", quan+Wstring[W]]]
        newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
        return df
    return df.loc[:, ["Z", quan+Wstring[W]]]

def IsobaricChain(A,model,quan,W=0, include_bmc=False):
    df = pd.read_hdf(db, model)
    ucol = "u" + quan
    if include_bmc and model == 'AME2020':
        df_bmc = pd.read_hdf(db, 'BMC')
        if W == 3:
            cols = [quan + Wstring[1], quan + Wstring[2], ucol]
        else:
            cols = [quan + Wstring[W], ucol]
        df, bmc_mask_df = ame_with_bmc_fallback_and_mask(df, df_bmc, cols)

    df = df[(df["Z"] + df["N"]) == A].copy()
    if model=='AME2020':
        if W == 3:
            newdf = df.loc[:, ["Z", quan+Wstring[1], "u"+quan, 'e'+quan]]
            newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
            return df
        return df.loc[:, ["Z", quan+Wstring[W], "u"+quan, 'e'+quan]]
    if model=='BMC':
        ucol = "u" + quan
        if W == 3:
            cols = ["Z", quan+Wstring[1]]
            if ucol in df.columns:
                cols.append(ucol)
            newdf = df.loc[:, cols]
            newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
            return df
        cols = ["Z", quan+Wstring[W]]
        if ucol in df.columns:
            cols.append(ucol)
        return df.loc[:, cols]
    if W == 3:
        newdf = df.loc[:, ["Z", quan+Wstring[W]]]
        newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
        return df
    return df.loc[:, ["Z", quan+Wstring[W]]]

def OutputString(quantity):
    OutputStringDict = {
        "BE": "Binding Energy",
        "MassExcess": "Mass Excess",
        "OneNSE": "One Neutron Separation Energy",
        "OnePSE": "One Proton Separation Energy",
        "TwoNSE": "Two Neutron Separation Energy",
        "TwoPSE": "Two Proton Separation Energy",
        "AlphaSE": "Alpha Separation Energy",
        "BetaMinusDecay": "Beta Minus Decay Q-Value",
        "BetaPlusDecay": "Beta Plus Decay Q-Value",
        "ElectronCaptureQValue": "Electron Capture Q-Value",
        "AlphaDecayQValue": "Alpha Decay Q-Value",
        "TwoPSGap": "Two Proton Shell Gap",
        "TwoNSGap": "Two Neutron Shell Gap",
        "DoubleMDiff": "Double Mass Difference",
        "N3PointOED": "Neutron 3-Point Odd-Even Binding Energy Difference",
        "P3PointOED": "Proton 3-Point Odd-Even Binding Energy Difference",
        "SNESplitting": "Single-Neutron Shell Gap",
        "SPESplitting": "Single-Proton Shell Gap",
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

