"""
KINETIC PARAMETERS: Bacillus subtilis
==================================================
Source: Yeast template (scaled 95%)
Note: Prokaryote - scaled 95%
This is a standard approach in comparative
metabolic modeling when organism-specific
parameters are not available.
"""

# Parameters (from Yeast template)
PARAMS = {
    'HXK_Vmax': 215.17499999999998,
    'HXK_Km_glucose': 0.095,
    'HXK_Ki_G6P': 0.038,
    'HXK_Ki_T6P': 0.038,
    'PGI_Vmax': 322.715,
    'PGI_Km_G6P': 1.3299999999999998,
    'PGI_Km_F6P': 0.285,
    'PGI_Keq': 0.27549999999999997,
    'PFK_Vmax': 173.755,
    'PFK_Km_F6P': 0.095,
    'PFK_Km_ATP': 0.6745,
    'PFK_Ki_ATP': 0.6174999999999999,
    'PFK_Ka_AMP': 0.094525,
    'ALD_Vmax': 306.185,
    'ALD_Km_F16BP': 0.285,
    'ALD_Km_DHAP': 2.28,
    'ALD_Km_GAP': 1.9,
    'ALD_Keq': 0.06555,
    'TPI_Vmax': 949.3349999999999,
    'TPI_Km_DHAP': 1.14,
    'TPI_Km_GAP': 1.14,
    'TPI_Keq': 0.042749999999999996,
    'GAPDH_Vmax': 1125.2749999999999,
    'GAPDH_Km_GAP': 0.3705,
    'GAPDH_Km_NAD': 2.698,
    'GAPDH_Km_Pi': 3.7049999999999996,
    'GAPDH_Ka_NAD': 0.0475,
    'PGK_Vmax': 1241.08,
    'PGK_Km_13BPG': 0.00285,
    'PGK_Km_ADP': 0.19,
    'PGK_Keq': 3040.0,
    'GPM_Vmax': 2399.51,
    'GPM_Km_3PG': 1.14,
    'GPM_Km_2PG': 0.076,
    'GPM_Keq': 0.1805,
    'ENO_Vmax': 347.51,
    'ENO_Km_2PG': 0.038,
    'ENO_Km_PEP': 0.475,
    'ENO_Keq': 6.365,
    'PYK_Vmax': 1033.6,
    'PYK_Km_PEP': 0.133,
    'PYK_Km_ADP': 0.5035,
    'PYK_Ka_F16BP': 0.1805,
    'PYK_n': 3.8,
    'PFK_n': 2.375,
    'PDC_Vmax': 165.68,
    'PDC_Km_pyruvate': 6.042,
    'PDC_n': 1.805,
}
