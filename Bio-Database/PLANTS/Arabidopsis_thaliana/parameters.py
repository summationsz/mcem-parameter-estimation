"""
KINETIC PARAMETERS: Arabidopsis thaliana
==================================================
Source: Yeast template (scaled 110%)
Note: Plant - scaled 110%
This is a standard approach in comparative
metabolic modeling when organism-specific
parameters are not available.
"""

# Parameters (from Yeast template)
PARAMS = {
    'HXK_Vmax': 249.15000000000003,
    'HXK_Km_glucose': 0.11000000000000001,
    'HXK_Ki_G6P': 0.044000000000000004,
    'HXK_Ki_T6P': 0.044000000000000004,
    'PGI_Vmax': 373.67,
    'PGI_Km_G6P': 1.54,
    'PGI_Km_F6P': 0.33,
    'PGI_Keq': 0.319,
    'PFK_Vmax': 201.19000000000003,
    'PFK_Km_F6P': 0.11000000000000001,
    'PFK_Km_ATP': 0.781,
    'PFK_Ki_ATP': 0.7150000000000001,
    'PFK_Ka_AMP': 0.10945000000000002,
    'ALD_Vmax': 354.53000000000003,
    'ALD_Km_F16BP': 0.33,
    'ALD_Km_DHAP': 2.64,
    'ALD_Km_GAP': 2.2,
    'ALD_Keq': 0.07590000000000001,
    'TPI_Vmax': 1099.23,
    'TPI_Km_DHAP': 1.32,
    'TPI_Km_GAP': 1.32,
    'TPI_Keq': 0.0495,
    'GAPDH_Vmax': 1302.95,
    'GAPDH_Km_GAP': 0.42900000000000005,
    'GAPDH_Km_NAD': 3.124,
    'GAPDH_Km_Pi': 4.29,
    'GAPDH_Ka_NAD': 0.05500000000000001,
    'PGK_Vmax': 1437.0400000000002,
    'PGK_Km_13BPG': 0.0033000000000000004,
    'PGK_Km_ADP': 0.22000000000000003,
    'PGK_Keq': 3520.0000000000005,
    'GPM_Vmax': 2778.3800000000006,
    'GPM_Km_3PG': 1.32,
    'GPM_Km_2PG': 0.08800000000000001,
    'GPM_Keq': 0.20900000000000002,
    'ENO_Vmax': 402.38000000000005,
    'ENO_Km_2PG': 0.044000000000000004,
    'ENO_Km_PEP': 0.55,
    'ENO_Keq': 7.370000000000001,
    'PYK_Vmax': 1196.8000000000002,
    'PYK_Km_PEP': 0.15400000000000003,
    'PYK_Km_ADP': 0.5830000000000001,
    'PYK_Ka_F16BP': 0.20900000000000002,
    'PYK_n': 4.4,
    'PFK_n': 2.75,
    'PDC_Vmax': 191.84000000000003,
    'PDC_Km_pyruvate': 6.996000000000001,
    'PDC_n': 2.09,
}
