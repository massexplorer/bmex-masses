import numpy as np
import pandas as pd
import math

db = 'data/7-10-23.h5'
Wstring = {0: '', 1: '_W1', 2: '_W2'}

# Retrieves single value
def QuanValue(Z, N, model, quan, W=0, uncertainty=False, beta_type=None):
    df = pd.read_hdf(db, model)
    print(f"\n🔍 Debug - Available Nuclei in {model} Dataset:")
    print(df[["Z", "N", "BE"]])  # Only print Z, N, and BE for clarity
    m_e_c2 = 0.511  # MeV

    if quan == "BetaQValue":
        try:
            # Retrieve BE values for the selected nucleus
            current_be = df.loc[(df["N"] == N) & (df["Z"] == Z), "BE"].values[0]
            current_be_w1 = df.loc[(df["N"] == N) & (df["Z"] == Z), "BE_W1"].values[0]
            current_be_w2 = df.loc[(df["N"] == N) & (df["Z"] == Z), "BE_W2"].values[0]

            if beta_type == "minus":  # β⁻ decay
                descendant = df.loc[(df["N"] == N - 1) & (df["Z"] == Z + 1)]
                if descendant.empty:
                    descendant = df.loc[(df["N"] == N - 2) & (df["Z"] == Z + 2)]  # Fallback for even-even


            elif beta_type == "plus":  # β⁺ decay
                descendant = df.loc[(df["N"] == N + 1) & (df["Z"] == Z - 1)]
                if descendant.empty:
                    descendant = df.loc[(df["N"] == N + 2) & (df["Z"] == Z - 2)]  # Fallback for even-even

            if not descendant.empty:
                descendant_be = descendant["BE"].iloc[0]
                descendant_be_w1 = descendant["BE_W1"].iloc[0]
                descendant_be_w2 = descendant["BE_W2"].iloc[0]

                q_value = current_be - descendant_be - (m_e_c2 if beta_type == "minus" else 2 * m_e_c2)
                q_value_w1 = current_be_w1 - descendant_be_w1 - (m_e_c2 if beta_type == "minus" else 2 * m_e_c2)
                q_value_w2 = current_be_w2 - descendant_be_w2 - (m_e_c2 if beta_type == "minus" else 2 * m_e_c2)
                # print(f"\n✅ Single value - After Extracting BE:")
                # print(f"descendant_be = {descendant_be}")
                # print(f"\n🧮 Q-Value Calculation in single value for Z={Z}, N={N}:")
                # print(f"Q = {current_be} - {descendant_be} - {m_e_c2}")
            else:                        
                q_value = None
                q_value_w1 = None
                q_value_w2 = None


                # Apply Wigner based on W
                if W == 1:
                    return q_value_w1, None, None
                elif W == 2:
                    return q_value_w2, None, None
                elif W == 3:
                    return (q_value_w1 + q_value_w2) / 2, None, None
                else:
                    return q_value, None, None


        except (KeyError, IndexError):  
            return f"Beta Q-Value not computable for N={N} and Z={Z} in the selected model", None, None
        

        return q_value, None, None

    try:
        if uncertainty and model == 'AME2020':
            v = np.round(df[(df["N"] == N) & (df["Z"] == Z)][quan + Wstring[W]].values[0], 6)
            e = df[(df["N"] == N) & (df["Z"] == Z)]['e' + quan].values[0]
            try:
                u = np.round(df[(df["N"] == N) & (df["Z"] == Z)]['u' + quan].values[0], 6)
            except:
                u = None
            return v, u, e
        else:
            return np.round(df[(df["N"] == N) & (df["Z"] == Z)][quan].values[0], 6), None, None
    except:
        return f"{model} has no {OutputString(quan)} available for Nuclei with N={N} and Z={Z}", None, None


def Landscape(model,quan,W=0,step=1,SPSadj=False, beta_type=None):
    df = pd.read_hdf(db, model)
    m_e_c2 = 0.511  # MeV

    if quan == "BetaQValue":
        if beta_type is None:
            beta_type = "minus"
            
        beta_q_values = []
        uncertainties = [] 
        estimated = [] 
        beta_q_values_w1 = []
        beta_q_values_w2 = []
    

        for _, row in df.iterrows():
            Z, N = row["Z"], row["N"]
            try:
                current_be = row["BE"]
                current_be_w1 = row["BE_W1"]  # Use Wigner 1 BE
                current_be_w2 = row["BE_W2"]  # Use Wigner 2 BE

                if beta_type == "minus":
                    # Primary descendant (Z+1, N-1)
                    descendant = df.loc[(df["N"] == N - 1) & (df["Z"] == Z + 1)]
                    if descendant.empty:
                        # Fallback descendant (Z+2, N-2) for even-even datasets
                        descendant = df.loc[(df["N"] == N - 2) & (df["Z"] == Z + 2)]  
                        
                    if not descendant.empty:
                        descendant_be = descendant["BE"].iloc[0]
                        descendant_be_w1 = descendant["BE_W1"].iloc[0]
                        descendant_be_w2 = descendant["BE_W2"].iloc[0]

                        q_value = current_be - descendant_be - m_e_c2
                        q_value_w1 = current_be_w1 - descendant_be_w1 - m_e_c2
                        q_value_w2 = current_be_w2 - descendant_be_w2 - m_e_c2

                        # if Z == 4 and N == 4:
                        #     print(f"\n✅ Landscape - After Extracting BE:")
                        #     print(f"descendant_be = {descendant_be}")
                        #     print(f"\n🧮 Q-Value Calculation in landscape for Z={Z}, N={N}:")
                        #     print(f"Q = {current_be} - {descendant_be} - {m_e_c2}")
                    
                    else:
                        # If no valid descendant was found, set Q values to None
                        q_value = None
                        q_value_w1 = None
                        q_value_w2 = None

                elif beta_type == "plus":
                    # Primary descendant (Z-1, N+1)
                    descendant = df.loc[(df["N"] == N + 1) & (df["Z"] == Z - 1)]
                    if descendant.empty:
                        # Fallback descendant (Z-2, N+2) for even-even datasets
                        descendant = df.loc[(df["N"] == N + 2) & (df["Z"] == Z - 2)]

                    if not descendant.empty:
                        descendant_be = descendant["BE"].iloc[0]
                        descendant_be_w1 = descendant["BE_W1"].iloc[0]
                        descendant_be_w2 = descendant["BE_W2"].iloc[0]

                        q_value = current_be - descendant_be - 2 * m_e_c2
                        q_value_w1 = current_be_w1 - descendant_be_w1 - 2 * m_e_c2
                        q_value_w2 = current_be_w2 - descendant_be_w2 - 2 * m_e_c2

                    else:
                        # If no valid descendant was found, set Q values to None
                        q_value = None
                        q_value_w1 = None
                        q_value_w2 = None

            except (KeyError, IndexError):  
                q_value = None
                q_value_w1 = None
                q_value_w2 = None

            beta_q_values.append(q_value)
            beta_q_values_w1.append(q_value_w1)
            beta_q_values_w2.append(q_value_w2)
            
        # Add uncertainties and estimated flags for AME2020
            if model == 'AME2020':
                try:
                    u = np.round(row['uBE'], 6)  # Uncertainty for BE
                except KeyError:
                    u = None
                try:
                    e = row['eBE']  # Estimated value flag
                except KeyError:
                    e = None

                uncertainties.append(u)
                estimated.append(e)

        df["BetaQValue"] = beta_q_values
        df["BetaQValue_W1"] = beta_q_values_w1
        df["BetaQValue_W2"] = beta_q_values_w2

        if 4 in df["Z"].values and 4 in df["N"].values:
            debug_row = df[(df["Z"] == 4) & (df["N"] == 4)]
            print(f"\n✅ Debug - Final DF Entry for Z=4, N=4 Before Storing in vals_arr2d:\n{debug_row[['BetaQValue', 'BetaQValue_W1', 'BetaQValue_W2']]}")

        # Add uncertainty and estimated columns if AME2020
        if model == 'AME2020':
            df["uBetaQValue"] = uncertainties
            df["eBetaQValue"] = estimated
    df = df[df["N"] % 1 == 0]
    df = df[df["Z"] % 1 == 0]

    # Drop rows with missing values for the quantity
    df = df.dropna(subset=[quan])
    if df.empty:
        print('DF is empty here')
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

def IsotopicChain(Z,model,quan,W=0, beta_type="minus"):
    df = pd.read_hdf(db, model)
    m_e_c2 = 0.511  # MeV
    # if quan == "BetaQValue":
    #     if beta_type is None:
    #         beta_type = "minus"

    #     beta_q_values = []
    #     for _, row in df.iterrows():
    #         Z, current_N = row["Z"], row["N"]
    #         try:
    #             current_be = row["BE"]
    #             if beta_type == "minus":  # β⁻ decay
    #                 descendant_be = df.loc[(df["N"] == current_N - 1) & (df["Z"] == Z + 1), "BE"].values[0]
    #                 q_value = current_be - descendant_be - m_e_c2
    #             elif beta_type == "plus":  # β⁺ decay
    #                 descendant_be = df.loc[(df["N"] == current_N + 1) & (df["Z"] == Z - 1), "BE"].values[0]
    #                 q_value = current_be - descendant_be - 2 * m_e_c2
    #             else:
    #                 raise ValueError(f"Invalid beta_type: {beta_type}. Must be 'minus' or 'plus'.")
    #         except (KeyError, IndexError):  
    #             q_value = None

    #         beta_q_values.append(q_value)

    #     # Add BetaQValue column to the dataframe
    #     df["BetaQValue"] = beta_q_values
    
    df = df[df["Z"] == Z]
    if df.empty:
            print('df is empty')
    # # Ensure the Quantity Exists
    # if quan not in df.columns:
    #     raise ValueError(f"Quantity '{quan}' is not found in the dataset.")

    # # Drop Missing Data
    # df = df.dropna(subset=[quan])
    # if df.empty:
    #     raise ValueError("Filtered DataFrame is empty after dropping missing values.")
    
    if model=='AME2020':
        if W == 3:
            newdf = df.loc[:, ["N", quan+Wstring[1], "u"+quan, 'e'+quan]]
            newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
            return df
        return df.loc[:, ["N", quan+Wstring[W], "u"+quan, 'e'+quan]]
    if W == 3:
        newdf = df.loc[:, ["N", quan+Wstring[W]]]
        newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
        return df
    return df.loc[:, ["N", quan+Wstring[W]]]

def IsotonicChain(N,model,quan,W=0, beta_type="minus"):


    if N is None:
        raise ValueError("N cannot be None. Please provide a valid neutron number.")

    df = pd.read_hdf(db, model)
    m_e_c2 = 0.511  # MeV
    print(f"Unique N values: {df['N'].unique()}")
    print(f"Unique Z values: {df['Z'].unique()}")
    print(f"N dtype: {df['N'].dtype}, Z dtype: {df['Z'].dtype}")

    if quan == "BetaQValue":
        if beta_type is None:
            beta_type = "minus"

        beta_q_values = []
        for _, row in df.iterrows():
            Z, current_N = row["Z"], row["N"]
            try:
                current_be = row["BE"]
                if beta_type == "minus":  # β⁻ decay
                    #print(f"Looking for descendant: N={current_N - 1}, Z={Z + 1}")
                    descendant = df.loc[(df["N"] == current_N - 1) & (df["Z"] == Z + 1)]
                    if descendant.empty:
                        #print("Descendant not found.")
                        descendant_be = None
                    else:
                        descendant_be = descendant["BE"].values[0]
                    q_value = current_be - descendant_be - m_e_c2 if descendant_be is not None else None
                elif beta_type == "plus":  # β⁺ decay
                    print(f"Looking for descendant: N={current_N + 1}, Z={Z - 1}")
                    descendant = df.loc[(df["N"] == current_N + 1) & (df["Z"] == Z - 1)]
                    if descendant.empty:
                        print("Descendant not found.")
                        descendant_be = None
                    else:
                        descendant_be = descendant["BE"].values[0]
                    q_value = current_be - descendant_be - 2 * m_e_c2 if descendant_be is not None else None
                else:
                    raise ValueError(f"Invalid beta_type: {beta_type}. Must be 'minus' or 'plus'.")
            except KeyError as e:
                print(f"KeyError during descendant lookup: {e}")
                q_value = None
            except IndexError as e:
                print(f"IndexError during descendant lookup: {e}")
                q_value = None

            beta_q_values.append(q_value)

        # Add BetaQValue column to the DataFrame
        df["BetaQValue"] = beta_q_values
        print(f"BetaQValue added. First 10 values: {df['BetaQValue'].head(10)}")

    df = df[df["N"] == N]
    print(f"Filtered DataFrame for N={N}. Rows remaining: {len(df)}")

    if df.empty:
        print("Filtered DataFrame is empty for N after BetaQValue calculation.")
        return df

    df = df.dropna(subset=[quan])
    print(f"Filtered DataFrame for {quan}. Rows remaining: {len(df)}")

    if model=='AME2020':
        if W == 3:
            newdf = df.loc[:, ["Z", quan+Wstring[1], "u"+quan, 'e'+quan]]
            newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
            return df
        return df.loc[:, ["Z", quan+Wstring[W], "u"+quan, 'e'+quan]]
    if W == 3:
        newdf = df.loc[:, ["Z", quan+Wstring[W]]]
        newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
        return df
    return df.loc[:, ["Z", quan+Wstring[W]]]

def IsobaricChain(A,model,quan,W=0, beta_type=None, terms=None):
    df = pd.read_hdf(db, model)
    df = df[df["Z"]+df["N"]==A]
    df = df.dropna(subset=[quan])

    # Handle β Q-values
    if quan == "BetaQValue":
        m_e_c2 = 0.511  # MeV
        df["BetaQValue"] = df["BE"] - df["BE"].shift(-1) - m_e_c2  # β⁻ decay
        return df.loc[:, ["Z", "BetaQValue"]]

    # Handle arbitrary Q-values
    elif quan == "ArbitraryQValue" and terms:
        df["ArbitraryQValue"] = 0
        for term in terms:
            coef = term.get("coef", 1)
            Z_term = term["Z"]
            try:
                be = df[df["Z"] == Z_term]["BE"].values[0]  # Fetch binding energy for the term
                df["ArbitraryQValue"] += coef * be
            except:
                pass  # Handle missing data gracefully
        return df.loc[:, ["Z", "ArbitraryQValue"]]
    
    if model=='AME2020':
        if W == 3:
            newdf = df.loc[:, ["Z", quan+Wstring[1], "u"+quan, 'e'+quan]]
            newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
            return df
        return df.loc[:, ["Z", quan+Wstring[W], "u"+quan, 'e'+quan]]
    if W == 3:
        newdf = df.loc[:, ["Z", quan+Wstring[W]]]
        newdf[quan+Wstring[1]] = (df[quan+Wstring[1]]  + df[quan+Wstring[2]])/2
        return df
    return df.loc[:, ["Z", quan+Wstring[W]]]

def OutputString(quantity):
    OutputStringDict = {
        "BE": "Binding Energy",
        "OneNSE": "One Neutron Separation Energy",
        "OnePSE": "One Proton Separation Energy",
        "TwoNSE": "Two Neutron Separation Energy",
        "TwoPSE": "Two Proton Separation Energy",
        "BetaQValue": "Beta Q-Value",
        "AlphaSE": "Alpha Separation Energy",
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
    



