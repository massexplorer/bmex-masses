# Dictionary: 
# Key: quantities ; Value: list of dictionaries with invalid datasets disabled.
def dataset_options(quan):
    # All Models
    if quan in ['BE', 'TwoNSE', 'TwoPSE', 'AlphaSE', 'TwoNSGap', 'TwoPSGap', 'DoubleMDiff', 'WignerEC', 'BEperA', 'All']:
        opts = \
        [
            {"label": "AME2020", "value": "AME2020"},
            {"label": "ME2", "value": "ME2"},
            {"label": "MEdelta", "value": "MEdelta"},
            {"label": "PC1", "value": "PC1"},
            {"label": "NL3S", "value": "NL3S"},
            {"label": "SkMs", "value": "SKMS"},
            {"label": "SKP", "value": "SKP"},
            {"label": "SLY4", "value": "SLY4"},
            {"label": "SV", "value": "SV"},
            {"label": "UNEDF0", "value": "UNEDF0"},
            {"label": "UNEDF1", "value": "UNEDF1"},
            {"label": "UNEDF2", "value": "UNEDF2"},
            {"label": "FRDM12", "value": "FRDM12"},
            {"label": "HFB24", "value": "HFB24"},
            {"label": "BCPM", "value": "BCPM"},
            {"label": "D1M", "value": "D1M"},
        ]
    # Single Particle (No Covar DFTs)
    elif quan in ['OneNSE', 'OnePSE', 'N3PointOED', 'N3PointOED', 'SNESplitting', 'SPESplitting']:
        opts = \
        [
            {"label": "AME2020", "value": "AME2020"},
            {"label": "ME2", "value": "ME2", "disabled": True},
            {"label": "MEdelta", "value": "MEdelta", "disabled": True},
            {"label": "PC1", "value": "PC1", "disabled": True},
            {"label": "NL3S", "value": "NL3S", "disabled": True},
            {"label": "SkMs", "value": "SKMS"},
            {"label": "SKP", "value": "SKP"},
            {"label": "SLY4", "value": "SLY4"},
            {"label": "SV", "value": "SV"},
            {"label": "UNEDF0", "value": "UNEDF0"},
            {"label": "UNEDF1", "value": "UNEDF1"},
            {"label": "UNEDF2", "value": "UNEDF2"},
            {"label": "FRDM12", "value": "FRDM12"},
            {"label": "HFB24", "value": "HFB24"},
            {"label": "BCPM", "value": "BCPM"},
            {"label": "D1M", "value": "D1M"},
        ]
    # Skyrme
    elif quan in ['FermiP', 'FermiN', 'QMQ2p', 'QMQ2n', 'QMQ2t', 'PGp', 'PGn', 'RMSradP', 'RMSradN', 'RMSradT', 'NSkin']:
        opts =  \
        [
            {"label": "AME2020", "value": "AME2020", "disabled": True},
            {"label": "ME2", "value": "ME2", "disabled": True},
            {"label": "MEdelta", "value": "MEdelta", "disabled": True},
            {"label": "PC1", "value": "PC1", "disabled": True},
            {"label": "NL3S", "value": "NL3S", "disabled": True},
            {"label": "SkMs", "value": "SKMS"},
            {"label": "SKP", "value": "SKP"},
            {"label": "SLY4", "value": "SLY4"},
            {"label": "SV", "value": "SV"},
            {"label": "UNEDF0", "value": "UNEDF0"},
            {"label": "UNEDF1", "value": "UNEDF1"},
            {"label": "UNEDF2", "value": "UNEDF2", "disabled": True},
            {"label": "FRDM12", "value": "FRDM12", "disabled": True},
            {"label": "HFB24", "value": "HFB24", "disabled": True},
            {"label": "BCPM", "value": "BCPM", "disabled": True},
            {"label": "D1M", "value": "D1M", "disabled": True},
        ]
    # Covar DFTs
    elif quan in ['CPn', 'CPp', 'PEn', 'PEp', 'QDB4n', 'QDB4p', 'MRadN', 'MRadP']:
        opts =  \
        [
            {"label": "AME2020", "value": "AME2020", "disabled": True},
            {"label": "ME2", "value": "ME2"},
            {"label": "MEdelta", "value": "MEdelta"},
            {"label": "PC1", "value": "PC1"},
            {"label": "NL3S", "value": "NL3S"},
            {"label": "SkMs", "value": "SKMS", "disabled": True},
            {"label": "SKP", "value": "SKP", "disabled": True},
            {"label": "SLY4", "value": "SLY4", "disabled": True},
            {"label": "SV", "value": "SV", "disabled": True},
            {"label": "UNEDF0", "value": "UNEDF0", "disabled": True},
            {"label": "UNEDF1", "value": "UNEDF1", "disabled": True},
            {"label": "UNEDF2", "value": "UNEDF2", "disabled": True},
            {"label": "FRDM12", "value": "FRDM12", "disabled": True},
            {"label": "HFB24", "value": "HFB24", "disabled": True},
            {"label": "BCPM", "value": "BCPM", "disabled": True},
            {"label": "D1M", "value": "D1M", "disabled": True},
        ]
    # Skyrme and Covar DFTs
    elif quan in ['QDB2p', 'QDB2n','ChRad']:
        opts = \
        [
            {"label": "AME2020", "value": "AME2020", "disabled": True},
            {"label": "ME2", "value": "ME2"},
            {"label": "MEdelta", "value": "MEdelta"},
            {"label": "PC1", "value": "PC1"},
            {"label": "NL3S", "value": "NL3S"},
            {"label": "SkMs", "value": "SKMS"},
            {"label": "SKP", "value": "SKP"},
            {"label": "SLY4", "value": "SLY4"},
            {"label": "SV", "value": "SV"},
            {"label": "UNEDF0", "value": "UNEDF0"},
            {"label": "UNEDF1", "value": "UNEDF1"},
            {"label": "UNEDF2", "value": "UNEDF2", "disabled": True},
            {"label": "FRDM12", "value": "FRDM12", "disabled": True},
            {"label": "HFB24", "value": "HFB24", "disabled": True},
            {"label": "BCPM", "value": "BCPM", "disabled": True},
            {"label": "D1M", "value": "D1M", "disabled": True},
        ]
    # Total Deformation 2 (includes FRDM)
    elif quan in ['QDB2t',]:
        opts = \
        [
            {"label": "AME2020", "value": "AME2020", "disabled": True},
            {"label": "ME2", "value": "ME2"},
            {"label": "MEdelta", "value": "MEdelta"},
            {"label": "PC1", "value": "PC1"},
            {"label": "NL3S", "value": "NL3S"},
            {"label": "SkMs", "value": "SKMS"},
            {"label": "SKP", "value": "SKP"},
            {"label": "SLY4", "value": "SLY4"},
            {"label": "SV", "value": "SV"},
            {"label": "UNEDF0", "value": "UNEDF0"},
            {"label": "UNEDF1", "value": "UNEDF1"},
            {"label": "UNEDF2", "value": "UNEDF2", "disabled": True},
            {"label": "FRDM12", "value": "FRDM12"},
            {"label": "HFB24", "value": "HFB24", "disabled": True},
            {"label": "BCPM", "value": "BCPM", "disabled": True},
            {"label": "D1M", "value": "D1M", "disabled": True},
        ]
    # Total Deformation 4 (only FRDM)
    elif quan in ['QDB4t']:
        return \
        [
            {"label": "AME2020", "value": "AME2020", "disabled": True},
            {"label": "ME2", "value": "ME2", "disabled": True},
            {"label": "MEdelta", "value": "MEdelta", "disabled": True},
            {"label": "PC1", "value": "PC1", "disabled": True},
            {"label": "NL3S", "value": "NL3S", "disabled": True},
            {"label": "SkMs", "value": "SKMS", "disabled": True},
            {"label": "SKP", "value": "SKP", "disabled": True},
            {"label": "SLY4", "value": "SLY4", "disabled": True},
            {"label": "SV", "value": "SV", "disabled": True},
            {"label": "UNEDF0", "value": "UNEDF0", "disabled": True},
            {"label": "UNEDF1", "value": "UNEDF1", "disabled": True},
            {"label": "UNEDF2", "value": "UNEDF2", "disabled": True},
            {"label": "FRDM12", "value": "FRDM12"},
            {"label": "HFB24", "value": "HFB24", "disabled": True},
            {"label": "BCPM", "value": "BCPM", "disabled": True},
            {"label": "D1M", "value": "D1M", "disabled": True},
        ]
    else:
        raise ValueError('Invalid quantity: {}'.format(quan))
    
    return opts
    

def quantity_options(dataset, single=False):

    if dataset in ['ME2', 'MEdelta', 'PC1', 'NL3S']:
        opts = \
        [
            {"label": "Binding Energy", "value": "BE", "title": "Energy required to completely seperate the nucleus: \n B(N,Z)"},
            {"label": "One Neutron Separation Energy", "value": "OneNSE", "title": "Energy required to remove a neutron: \n S\u2099(N,Z) = B(N,Z) - B(N-1,Z)", "disabled": True},
            {"label": "One Proton Separation Energy", "value": "OnePSE", "title": "Energy required to remove a proton: \n S\u209A(N,Z) = B(N,Z) - B(N,Z-1)", "disabled": True},
            {"label": "Two Neutron Separation Energy", "value": "TwoNSE", "title": "Energy required to remove two neutrons: \n S\u2082\u2099(N,Z) = B(N,Z) - B(N-2,Z)"},
            {"label": "Two Proton Separation Energy", "value": "TwoPSE", "title": "Energy required to remove two protons: \n S\u2082\u209A(N,Z) = B(N,Z) - B(N,Z-2)"},
            {"label": "Alpha Separation Energy", "value": "AlphaSE", "title": "Energy required to remove an alpha particle: \n S\u2090 = B(N,Z) - B(N-2,Z-2) - 28.3 MeV"},
            {"label": "Two Neutron Shell Gap", "value": "TwoNSGap", "title": "\u03B4\u2082\u2099(N,Z) = S\u2082\u2099(N,Z) - S\u2082\u2099(N+2,Z)"},
            {"label": "Two Proton Shell Gap", "value": "TwoPSGap", "title": "\u03B4\u2082\u209A(N,Z) = S\u2082\u209A(N,Z) - S\u2082\u209A(N,Z+2)"},
            {"label": "Double Mass Difference", "value": "DoubleMDiff", "title": "\u03B4V\u209A\u2099(N,Z) = 1/4 [S\u2082\u209A(N,Z) - S\u2082\u209A(N-2,Z)]"},
            {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED", "title": "\u0394\u2099(N,Z) = 1/2 [S\u2099(N,Z) -S\u2099(N+1,Z)]", "disabled": True},
            {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED", "title": "\u0394\u209A(N,Z) = 1/2 [S\u209A(N,Z) -S\u209A(N,Z+1)]", "disabled": True},
            {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting", "title": "\u0394e\u2099(N,Z) = S\u2099(N,Z) - S\u2099(N+2,Z)", "disabled": True},
            {"label": "Single-Proton Energy Splitting", "value": "SPESplitting", "title": " \u0394e\u209A(N,Z) = S\u209A(N,Z) - S\u209A(N,Z+2)", "disabled": True},
            {"label": "Wigner Energy Coefficient", "value": "WignerEC"},
            {"label": "Binding Energy per Nucleon", "value": "BEperA", "title": "B/A(N,Z) = B(N,Z)/(N+Z)"},
            {"label": "Quad Def Beta2", "value": "QDB2t"},
            {"label": "Quad Def Beta2 N", "value": "QDB2n"},
            {"label": "Quad Def Beta2 P", "value": "QDB2p"},
            {"label": "Quad Def Beta4", "value": "QDB4t", "disabled": True},
            {"label": "Quad Def Beta4 N", "value": "QDB4n"},
            {"label": "Quad Def Beta4 P", "value": "QDB4p"},
            {"label": "Fermi Energy N", "value": "FermiN", "disabled": True},
            {"label": "Fermi Energy P", "value": "FermiP", "disabled": True},
            {"label": "Pairing Energy N", "value": "PEn"},
            {"label": "Pairing Energy P", "value": "PEp"},
            {"label": "Pairing Gap N", "value": "PGn", "disabled": True},
            {"label": "Pairing Gap P", "value": "PGp", "disabled": True},
            {"label": "Chemical Potential N", "value": "CPn"},
            {"label": "Chemical Potential P", "value": "CPp"},
            {"label": "RMS Radius Total", "value": "RMSradT", "disabled": True},
            {"label": "RMS Radius N", "value": "RMSradN", "disabled": True},
            {"label": "RMS Radius P", "value": "RMSradP", "disabled": True},
            {"label": "Mass Radius N", "value": "MRadN"},
            {"label": "Mass Radius P", "value": "MRadP"},
            {"label": "Charge Radius", "value": "ChRad"},
            {"label": "Neutron Skin", "value": "NSkin", "disabled": True},
            {"label": "Quad Moment Q2 Total", "value": "QMQ2t", "disabled": True},
            {"label": "Quad Moment Q2 N", "value": "QMQ2n", "disabled": True},
            {"label": "Quad Moment Q2 P", "value": "QMQ2p", "disabled": True},
        ]
    elif dataset in ['AME2020', 'HFB24', 'UNEDF2', 'BCPM', 'D1M']:
        opts = \
        [
             {"label": "Binding Energy", "value": "BE", "title": "Energy required to completely seperate the nucleus: \n B(N,Z)"},
            {"label": "One Neutron Separation Energy", "value": "OneNSE", "title": "Energy required to remove a neutron: \n S\u2099(N,Z) = B(N,Z) - B(N-1,Z)"},
            {"label": "One Proton Separation Energy", "value": "OnePSE", "title": "Energy required to remove a proton: \n S\u209A(N,Z) = B(N,Z) - B(N,Z-1)"},
            {"label": "Two Neutron Separation Energy", "value": "TwoNSE", "title": "Energy required to remove two neutrons: \n S\u2082\u2099(N,Z) = B(N,Z) - B(N-2,Z)"},
            {"label": "Two Proton Separation Energy", "value": "TwoPSE", "title": "Energy required to remove two protons: \n S\u2082\u209A(N,Z) = B(N,Z) - B(N,Z-2)"},
            {"label": "Alpha Separation Energy", "value": "AlphaSE", "title": "Energy required to remove an alpha particle: \n S\u2090 = B(N,Z) - B(N-2,Z-2) - 28.3 MeV"},
            {"label": "Two Neutron Shell Gap", "value": "TwoNSGap", "title": "\u03B4\u2082\u2099(N,Z) = S\u2082\u2099(N,Z) - S\u2082\u2099(N+2,Z)"},
            {"label": "Two Proton Shell Gap", "value": "TwoPSGap", "title": "\u03B4\u2082\u209A(N,Z) = S\u2082\u209A(N,Z) - S\u2082\u209A(N,Z+2)"},
            {"label": "Double Mass Difference", "value": "DoubleMDiff", "title": "\u03B4V\u209A\u2099(N,Z) = 1/4 [S\u2082\u209A(N,Z) - S\u2082\u209A(N-2,Z)]"},
            {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED", "title": "\u0394\u2099(N,Z) = 1/2 [S\u2099(N,Z) -S\u2099(N+1,Z)]"},
            {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED", "title": "\u0394\u209A(N,Z) = 1/2 [S\u209A(N,Z) -S\u209A(N,Z+1)]"},
            {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting", "title": "\u0394e\u2099(N,Z) = S\u2099(N,Z) - S\u2099(N+2,Z)"},
            {"label": "Single-Proton Energy Splitting", "value": "SPESplitting", "title": " \u0394e\u209A(N,Z) = S\u209A(N,Z) - S\u209A(N,Z+2)"},
            {"label": "Wigner Energy Coefficient", "value": "WignerEC"},
            {"label": "Binding Energy per Nucleon", "value": "BEperA", "title": "B/A(N,Z) = B(N,Z)/(N+Z)"},
            {"label": "Quad Def Beta2", "value": "QDB2t", "disabled": True},
            {"label": "Quad Def Beta2 N", "value": "QDB2n", "disabled": True},
            {"label": "Quad Def Beta2 P", "value": "QDB2p", "disabled": True},
            {"label": "Quad Def Beta4", "value": "QDB4t", "disabled": True},
            {"label": "Quad Def Beta4 N", "value": "QDB4n", "disabled": True},
            {"label": "Quad Def Beta4 P", "value": "QDB4p", "disabled": True},
            {"label": "Fermi Energy N", "value": "FermiN", "disabled": True},
            {"label": "Fermi Energy P", "value": "FermiP", "disabled": True},
            {"label": "Pairing Energy N", "value": "PEn", "disabled": True},
            {"label": "Pairing Energy P", "value": "PEp", "disabled": True},
            {"label": "Pairing Gap N", "value": "PGn", "disabled": True},
            {"label": "Pairing Gap P", "value": "PGp", "disabled": True},
            {"label": "Chemical Potential N", "value": "CPn", "disabled": True},
            {"label": "Chemical Potential P", "value": "CPp", "disabled": True},
            {"label": "RMS Radius Total", "value": "RMSradT", "disabled": True},
            {"label": "RMS Radius N", "value": "RMSradN", "disabled": True},
            {"label": "RMS Radius P", "value": "RMSradP", "disabled": True},
            {"label": "Mass Radius N", "value": "MRadN", "disabled": True},
            {"label": "Mass Radius P", "value": "MRadP", "disabled": True},
            {"label": "Charge Radius", "value": "ChRad", "disabled": True},
            {"label": "Neutron Skin", "value": "NSkin", "disabled": True},
            {"label": "Quad Moment Q2 Total", "value": "QMQ2t", "disabled": True},
            {"label": "Quad Moment Q2 N", "value": "QMQ2n", "disabled": True},
            {"label": "Quad Moment Q2 P", "value": "QMQ2p", "disabled": True},
        ]
    elif dataset in ['SKMS', 'SKP', 'SLY4', 'SV', 'UNEDF0', 'UNEDF1']:
        opts = \
        [
            {"label": "Binding Energy", "value": "BE", "title": "Energy required to completely seperate the nucleus: \n B(N,Z)"},
            {"label": "One Neutron Separation Energy", "value": "OneNSE", "title": "Energy required to remove a neutron: \n S\u2099(N,Z) = B(N,Z) - B(N-1,Z)"},
            {"label": "One Proton Separation Energy", "value": "OnePSE", "title": "Energy required to remove a proton: \n S\u209A(N,Z) = B(N,Z) - B(N,Z-1)"},
            {"label": "Two Neutron Separation Energy", "value": "TwoNSE", "title": "Energy required to remove two neutrons: \n S\u2082\u2099(N,Z) = B(N,Z) - B(N-2,Z)"},
            {"label": "Two Proton Separation Energy", "value": "TwoPSE", "title": "Energy required to remove two protons: \n S\u2082\u209A(N,Z) = B(N,Z) - B(N,Z-2)"},
            {"label": "Alpha Separation Energy", "value": "AlphaSE", "title": "Energy required to remove an alpha particle: \n S\u2090 = B(N,Z) - B(N-2,Z-2) - 28.3 MeV"},
            {"label": "Two Neutron Shell Gap", "value": "TwoNSGap", "title": "\u03B4\u2082\u2099(N,Z) = S\u2082\u2099(N,Z) - S\u2082\u2099(N+2,Z)"},
            {"label": "Two Proton Shell Gap", "value": "TwoPSGap", "title": "\u03B4\u2082\u209A(N,Z) = S\u2082\u209A(N,Z) - S\u2082\u209A(N,Z+2)"},
            {"label": "Double Mass Difference", "value": "DoubleMDiff", "title": "\u03B4V\u209A\u2099(N,Z) = 1/4 [S\u2082\u209A(N,Z) - S\u2082\u209A(N-2,Z)]"},
            {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED", "title": "\u0394\u2099(N,Z) = 1/2 [S\u2099(N,Z) -S\u2099(N+1,Z)]"},
            {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED", "title": "\u0394\u209A(N,Z) = 1/2 [S\u209A(N,Z) -S\u209A(N,Z+1)]"},
            {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting", "title": "\u0394e\u2099(N,Z) = S\u2099(N,Z) - S\u2099(N+2,Z)"},
            {"label": "Single-Proton Energy Splitting", "value": "SPESplitting", "title": " \u0394e\u209A(N,Z) = S\u209A(N,Z) - S\u209A(N,Z+2)"},
            {"label": "Wigner Energy Coefficient", "value": "WignerEC"},
            {"label": "Binding Energy per Nucleon", "value": "BEperA", "title": "B/A(N,Z) = B(N,Z)/(N+Z)"},
            {"label": "Quad Def Beta2", "value": "QDB2t"},
            {"label": "Quad Def Beta2 N", "value": "QDB2n"},
            {"label": "Quad Def Beta2 P", "value": "QDB2p"},
            {"label": "Quad Def Beta4", "value": "QDB4t", "disabled": True},
            {"label": "Quad Def Beta4 N", "value": "QDB4n", "disabled": True},
            {"label": "Quad Def Beta4 P", "value": "QDB4p", "disabled": True},
            {"label": "Fermi Energy N", "value": "FermiN"},
            {"label": "Fermi Energy P", "value": "FermiP"},
            {"label": "Pairing Energy N", "value": "PEn", "disabled": True},
            {"label": "Pairing Energy P", "value": "PEp", "disabled": True},
            {"label": "Pairing Gap N", "value": "PGn"},
            {"label": "Pairing Gap P", "value": "PGp"},
            {"label": "Chemical Potential N", "value": "CPn", "disabled": True},
            {"label": "Chemical Potential P", "value": "CPp", "disabled": True},
            {"label": "RMS Radius Total", "value": "RMSradT", "disabled": True},
            {"label": "RMS Radius Total", "value": "RMSradT"},
            {"label": "RMS Radius N", "value": "RMSradN"},
            {"label": "RMS Radius P", "value": "RMSradP"},
            {"label": "Mass Radius N", "value": "MRadN", "disabled": True},
            {"label": "Mass Radius P", "value": "MRadP", "disabled": True},
            {"label": "Charge Radius", "value": "ChRad"},
            {"label": "Neutron Skin", "value": "NSkin"},
            {"label": "Quad Moment Q2 Total", "value": "QMQ2t"},
            {"label": "Quad Moment Q2 N", "value": "QMQ2n"},
            {"label": "Quad Moment Q2 P", "value": "QMQ2p"},
        ]
    elif dataset in ['FRDM12']:
        opts = \
        [
             {"label": "Binding Energy", "value": "BE", "title": "Energy required to completely seperate the nucleus: \n B(N,Z)"},
            {"label": "One Neutron Separation Energy", "value": "OneNSE", "title": "Energy required to remove a neutron: \n S\u2099(N,Z) = B(N,Z) - B(N-1,Z)"},
            {"label": "One Proton Separation Energy", "value": "OnePSE", "title": "Energy required to remove a proton: \n S\u209A(N,Z) = B(N,Z) - B(N,Z-1)"},
            {"label": "Two Neutron Separation Energy", "value": "TwoNSE", "title": "Energy required to remove two neutrons: \n S\u2082\u2099(N,Z) = B(N,Z) - B(N-2,Z)"},
            {"label": "Two Proton Separation Energy", "value": "TwoPSE", "title": "Energy required to remove two protons: \n S\u2082\u209A(N,Z) = B(N,Z) - B(N,Z-2)"},
            {"label": "Alpha Separation Energy", "value": "AlphaSE", "title": "Energy required to remove an alpha particle: \n S\u2090 = B(N,Z) - B(N-2,Z-2) - 28.3 MeV"},
            {"label": "Two Neutron Shell Gap", "value": "TwoNSGap", "title": "\u03B4\u2082\u2099(N,Z) = S\u2082\u2099(N,Z) - S\u2082\u2099(N+2,Z)"},
            {"label": "Two Proton Shell Gap", "value": "TwoPSGap", "title": "\u03B4\u2082\u209A(N,Z) = S\u2082\u209A(N,Z) - S\u2082\u209A(N,Z+2)"},
            {"label": "Double Mass Difference", "value": "DoubleMDiff", "title": "\u03B4V\u209A\u2099(N,Z) = 1/4 [S\u2082\u209A(N,Z) - S\u2082\u209A(N-2,Z)]"},
            {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED", "title": "\u0394\u2099(N,Z) = 1/2 [S\u2099(N,Z) -S\u2099(N+1,Z)]"},
            {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED", "title": "\u0394\u209A(N,Z) = 1/2 [S\u209A(N,Z) -S\u209A(N,Z+1)]"},
            {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting", "title": "\u0394e\u2099(N,Z) = S\u2099(N,Z) - S\u2099(N+2,Z)"},
            {"label": "Single-Proton Energy Splitting", "value": "SPESplitting", "title": " \u0394e\u209A(N,Z) = S\u209A(N,Z) - S\u209A(N,Z+2)"},
            {"label": "Wigner Energy Coefficient", "value": "WignerEC"},
            {"label": "Binding Energy per Nucleon", "value": "BEperA", "title": "B/A(N,Z) = B(N,Z)/(N+Z)"},
            {"label": "Quad Def Beta2", "value": "QDB2t"},
            {"label": "Quad Def Beta2 N", "value": "QDB2n", "disabled": True},
            {"label": "Quad Def Beta2 P", "value": "QDB2p", "disabled": True},
            {"label": "Quad Def Beta4", "value": "QDB4t"},
            {"label": "Quad Def Beta4 N", "value": "QDB4n", "disabled": True},
            {"label": "Quad Def Beta4 P", "value": "QDB4p", "disabled": True},
            {"label": "Fermi Energy N", "value": "FermiN", "disabled": True},
            {"label": "Fermi Energy P", "value": "FermiP", "disabled": True},
            {"label": "Pairing Energy N", "value": "PEn", "disabled": True},
            {"label": "Pairing Energy P", "value": "PEp", "disabled": True},
            {"label": "Pairing Gap N", "value": "PGn", "disabled": True},
            {"label": "Pairing Gap P", "value": "PGp", "disabled": True},
            {"label": "Chemical Potential N", "value": "CPn", "disabled": True},
            {"label": "Chemical Potential P", "value": "CPp", "disabled": True},
            {"label": "RMS Radius Total", "value": "RMSradT", "disabled": True},
            {"label": "RMS Radius N", "value": "RMSradN", "disabled": True},
            {"label": "RMS Radius P", "value": "RMSradP", "disabled": True},
            {"label": "Mass Radius N", "value": "MRadN", "disabled": True},
            {"label": "Mass Radius P", "value": "MRadP", "disabled": True},
            {"label": "Charge Radius", "value": "ChRad", "disabled": True},
            {"label": "Neutron Skin", "value": "NSkin", "disabled": True},
            {"label": "Quad Moment Q2 Total", "value": "QMQ2t", "disabled": True},
            {"label": "Quad Moment Q2 N", "value": "QMQ2n", "disabled": True},
            {"label": "Quad Moment Q2 P", "value": "QMQ2p", "disabled": True},
        ]
    else:
        raise ValueError('Invalid dataset: {}'.format(dataset))
    
    if single:
        opts.append({"label": "All", "value": "All"})
    return opts
    