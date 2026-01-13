"""
KINETIC PARAMETERS: Escherichia coli
==================================================
Source: Yeast template (scaled 90%)
Note: Prokaryote - scaled 90%
This is a standard approach in comparative
metabolic modeling when organism-specific
parameters are not available.
"""

# Parameters (from Yeast template)
PARAMS = {
    'HXK_Vmax': 203.85,
    'HXK_Km_glucose': 0.09000000000000001,
    'HXK_Ki_G6P': 0.036000000000000004,
    'HXK_Ki_T6P': 0.036000000000000004,
    'PGI_Vmax': 305.73,
    'PGI_Km_G6P': 1.26,
    'PGI_Km_F6P': 0.27,
    'PGI_Keq': 0.261,
    'PFK_Vmax': 164.61,
    'PFK_Km_F6P': 0.09000000000000001,
    'PFK_Km_ATP': 0.639,
    'PFK_Ki_ATP': 0.5850000000000001,
    'PFK_Ka_AMP': 0.08955,
    'ALD_Vmax': 290.07,
    'ALD_Km_F16BP': 0.27,
    'ALD_Km_DHAP': 2.16,
    'ALD_Km_GAP': 1.8,
    'ALD_Keq': 0.06210000000000001,
    'TPI_Vmax': 899.37,
    'TPI_Km_DHAP': 1.08,
    'TPI_Km_GAP': 1.08,
    'TPI_Keq': 0.0405,
    'GAPDH_Vmax': 1066.05,
    'GAPDH_Km_GAP': 0.35100000000000003,
    'GAPDH_Km_NAD': 2.556,
    'GAPDH_Km_Pi': 3.51,
    'GAPDH_Ka_NAD': 0.045000000000000005,
    'PGK_Vmax': 1175.7600000000002,
    'PGK_Km_13BPG': 0.0027,
    'PGK_Km_ADP': 0.18000000000000002,
    'PGK_Keq': 2880.0,
    'GPM_Vmax': 2273.2200000000003,
    'GPM_Km_3PG': 1.08,
    'GPM_Km_2PG': 0.07200000000000001,
    'GPM_Keq': 0.171,
    'ENO_Vmax': 329.22,
    'ENO_Km_2PG': 0.036000000000000004,
    'ENO_Km_PEP': 0.45,
    'ENO_Keq': 6.03,
    'PYK_Vmax': 979.2,
    'PYK_Km_PEP': 0.12600000000000003,
    'PYK_Km_ADP': 0.47700000000000004,
    'PYK_Ka_F16BP': 0.171,
    'PYK_n': 3.6,
    'PFK_n': 2.25,
    'PDC_Vmax': 156.96,
    'PDC_Km_pyruvate': 5.724,
    'PDC_n': 1.71,
}
