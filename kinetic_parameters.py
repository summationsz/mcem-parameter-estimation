"""
Kinetic Parameters for Glycolysis and TCA Cycle
================================================

Ground truth parameters from literature for MCEM validation.

Primary source: van Eunen et al. (2012) PLOS Comput Biol
DOI: 10.1371/journal.pcbi.1002483
"""

import numpy as np

# ==============================================================================
# GLYCOLYSIS PARAMETERS (Saccharomyces cerevisiae)
# From: van Eunen et al. (2012) - In vivo-like conditions
# ==============================================================================

GLYCOLYSIS_PARAMS = {
    # Hexokinase (HXK)
    'HXK_Vmax': 226.5,        # mM/min (D=0.1 h⁻¹, in vivo-like)
    'HXK_Km_glucose': 0.1,    # mM
    'HXK_Ki_G6P': 0.04,       # mM (product inhibition)
    'HXK_Ki_T6P': 0.04,       # mM (trehalose-6-phosphate, isoform 2)
    
    # Phosphoglucose Isomerase (PGI)
    'PGI_Vmax': 339.7,        # mM/min
    'PGI_Km_G6P': 1.4,        # mM
    'PGI_Km_F6P': 0.3,        # mM (reverse)
    'PGI_Keq': 0.29,          # Equilibrium constant
    
    # Phosphofructokinase (PFK)
    'PFK_Vmax': 182.9,        # mM/min
    'PFK_Km_F6P': 0.1,        # mM
    'PFK_Km_ATP': 0.71,       # mM
    'PFK_Ki_ATP': 0.65,       # mM (substrate inhibition)
    'PFK_Ka_AMP': 0.0995,     # mM (activation)
    
    # Aldolase (ALD)
    'ALD_Vmax': 322.3,        # mM/min
    'ALD_Km_F16BP': 0.3,      # mM
    'ALD_Km_DHAP': 2.4,       # mM (reverse)
    'ALD_Km_GAP': 2.0,        # mM (reverse)
    'ALD_Keq': 0.069,         # Equilibrium constant
    
    # Triose Phosphate Isomerase (TPI)
    'TPI_Vmax': 999.3,        # mM/min (very fast)
    'TPI_Km_DHAP': 1.2,       # mM
    'TPI_Km_GAP': 1.2,        # mM (reverse)
    'TPI_Keq': 0.045,         # Equilibrium constant (favors DHAP)
    
    # Glyceraldehyde-3-Phosphate Dehydrogenase (GAPDH)
    'GAPDH_Vmax': 1184.5,     # mM/min
    'GAPDH_Km_GAP': 0.39,     # mM (CRITICAL: in vivo-like vs 1.68 traditional)
    'GAPDH_Km_NAD': 2.84,     # mM (CRITICAL: in vivo-like vs 0.09 traditional)
    'GAPDH_Km_Pi': 3.9,       # mM (inorganic phosphate)
    'GAPDH_Ka_NAD': 0.05,     # mM (NAD+ activation constant - EXTENDED)
    
    # Phosphoglycerate Kinase (PGK)
    'PGK_Vmax': 1306.4,       # mM/min
    'PGK_Km_13BPG': 0.003,    # mM
    'PGK_Km_ADP': 0.2,        # mM
    'PGK_Keq': 3200,          # Equilibrium constant
    
    # Phosphoglycerate Mutase (GPM)
    'GPM_Vmax': 2525.8,       # mM/min
    'GPM_Km_3PG': 1.2,        # mM
    'GPM_Km_2PG': 0.08,       # mM (reverse)
    'GPM_Keq': 0.19,          # Equilibrium constant
    
    # Enolase (ENO)
    'ENO_Vmax': 365.8,        # mM/min
    'ENO_Km_2PG': 0.04,       # mM
    'ENO_Km_PEP': 0.5,        # mM (reverse)
    'ENO_Keq': 6.7,           # Equilibrium constant
    
    # Pyruvate Kinase (PYK)
    'PYK_Vmax': 1088.0,       # mM/min
    'PYK_Km_PEP': 0.14,       # mM
    'PYK_Km_ADP': 0.53,       # mM
    'PYK_Ka_F16BP': 0.19,     # mM (feedforward activation - EXTENDED)
    'PYK_n': 4.0,             # Hill coefficient for F16BP - EXTENDED
    
    # Phosphofructokinase (PFK) - Extended parameters
    'PFK_n': 2.5,             # Hill coefficient for cooperativity - EXTENDED
    
    # Pyruvate Decarboxylase (PDC)
    'PDC_Vmax': 174.4,        # mM/min
    'PDC_Km_pyruvate': 6.36,  # mM (at 50 mM phosphate)
    'PDC_n': 1.9,             # Hill coefficient
}

# ==============================================================================
# TCA CYCLE PARAMETERS
# From: Korzeniewski & Zoladz (2003), Martinez-Reyes & Chandel (2020)
# ==============================================================================

TCA_PARAMS = {
    # Pyruvate Transport & Entry
    'PYR_transport_Vmax': 50.0,    # mM/min (added for pyruvate import)
    'PYR_transport_Km': 0.019,     # mM (12-26 μM range, using midpoint)
    
    # Pyruvate Dehydrogenase (PDH) - converts pyruvate to AcCoA
    'PDH_Vmax': 100.0,             # mM/min (added)
    'PDH_Km_pyruvate': 0.025,      # mM (added)
    'PDH_Km_NAD': 0.05,            # mM (added)
    'PDH_Km_CoA': 0.013,           # mM (added)
    
    # Citrate Synthase (CS)
    'CS_Vmax': 100.0,              # Arbitrary units (scale to match flux)
    'CS_Km_AcCoA': 0.013,          # mM
    'CS_Km_OAA': 0.002,            # mM (very low - rate limiting)
    'CS_Ki_ATP': 0.9,              # mM (allosteric inhibition)
    'CS_Ki_citrate': 1.5,          # mM (product inhibition)
    
    # Aconitase (ACO)
    'ACO_Vmax': 150.0,             # Fast enzyme
    'ACO_Km_citrate': 0.48,        # mM
    'ACO_Km_isocitrate': 0.12,     # mM (reverse)
    'ACO_Keq': 0.067,              # Equilibrium constant
    
    # Isocitrate Dehydrogenase (ICDH)
    'ICDH_Vmax': 85.0,             # Regulatory enzyme
    'ICDH_Km_isocitrate': 0.11,    # mM
    'ICDH_Km_NAD': 0.09,           # mM
    'ICDH_Ka_ADP': 0.1,            # mM (activation)
    'ICDH_Ka_Ca': 0.001,           # mM (calcium activation)
    
    # α-Ketoglutarate Dehydrogenase (KGDH)
    'KGDH_Vmax': 75.0,             # Regulatory enzyme
    'KGDH_Km_aKG': 0.4,            # mM (α-ketoglutarate)
    'KGDH_Km_NAD': 0.038,          # mM
    'KGDH_Km_CoA': 0.013,          # mM
    'KGDH_Ki_SucCoA': 0.05,        # mM (product inhibition) - fixed name
    'KGDH_Ki_NADH': 0.05,          # mM (product inhibition)
    'KGDH_Ka_Ca': 0.001,           # mM (calcium activation)
    
    # Succinyl-CoA Synthetase (SCS) - added entirely
    'SCS_Vmax': 75.0,              # mM/min
    'SCS_Km_SucCoA': 0.056,        # mM
    'SCS_Km_GDP': 0.01,            # mM
    'SCS_Km_Pi': 0.56,             # mM
    
    # Succinate Dehydrogenase (SDH) - Complex II
    'SDH_Vmax': 60.0,
    'SDH_Km_succinate': 0.45,      # mM
    'SDH_Km_FAD': 0.002,           # mM (tightly bound)
    
    # Fumarase (FH)
    'FH_Vmax': 200.0,              # Fast enzyme
    'FH_Km_fumarate': 0.044,       # mM
    'FH_Km_malate': 0.25,          # mM (reverse)
    'FH_Keq': 4.4,                 # Equilibrium constant
    
    # Malate Dehydrogenase (MDH)
    'MDH_Vmax': 180.0,
    'MDH_Km_malate': 0.025,        # mM (21-32 μM range)
    'MDH_Km_NAD': 0.22,            # mM
    'MDH_Km_OAA': 0.003,           # mM (reverse)
    'MDH_Km_NADH': 0.025,          # mM (reverse)
    'MDH_Keq': 6.9e-5,             # Equilibrium constant (favors malate)
}

# ==============================================================================
# METABOLITE CONCENTRATIONS (Initial/Steady-State)
# From: van Eunen et al. (2012) - Experimental measurements
# ==============================================================================

INITIAL_CONCENTRATIONS = {
    # Glycolysis intermediates (mM)
    'glucose_ext': 5.0,        # External glucose
    'glucose': 0.087,          # Intracellular glucose
    'G6P': 2.45,               # Glucose-6-phosphate
    'F6P': 0.62,               # Fructose-6-phosphate
    'F16BP': 5.51,             # Fructose-1,6-bisphosphate
    'DHAP': 2.67,              # Dihydroxyacetone phosphate
    'GAP': 0.68,               # Glyceraldehyde-3-phosphate
    'BPG': 0.0,                # 1,3-bisphosphoglycerate (very low)
    '3PG': 0.9,                # 3-phosphoglycerate
    '2PG': 0.12,               # 2-phosphoglycerate
    'PEP': 0.07,               # Phosphoenolpyruvate
    'pyruvate': 1.85,          # Pyruvate
    
    # TCA cycle intermediates (mM)
    'AcCoA': 0.1,              # Acetyl-CoA
    'citrate': 0.5,            # Citrate
    'isocitrate': 0.05,        # Isocitrate
    'aKG': 0.15,               # α-ketoglutarate
    'sucCoA': 0.05,            # Succinyl-CoA
    'succinate': 0.4,          # Succinate
    'fumarate': 0.1,           # Fumarate
    'malate': 0.3,             # Malate
    'OAA': 0.004,              # Oxaloacetate (very low)
    
    # Cofactors (mM)
    'ATP': 2.52,               # Measured in yeast
    'ADP': 1.32,               # Measured
    'AMP': 0.28,               # Measured
    'NAD': 1.2,                # NAD+ pool
    'NADH': 0.39,              # NADH pool
    'Pi': 50.0,                # Inorganic phosphate
    'CoA': 0.5,                # Coenzyme A
    'FAD': 0.1,                # FAD pool
    'FADH2': 0.05,             # FADH2 pool
    
    # Regulatory molecules (mM)
    'T6P': 0.024,              # Trehalose-6-phosphate
    'F26BP': 0.014,            # Fructose-2,6-bisphosphate
    'Ca': 0.0001,              # Calcium (100 nM)
}

# ==============================================================================
# COMPLETE PARAMETER SET (for easy access)
# ==============================================================================

ALL_PARAMETERS = {**GLYCOLYSIS_PARAMS, **TCA_PARAMS}

# Print summary
if __name__ == "__main__":
    print("="*70)
    print("KINETIC PARAMETERS LOADED")
    print("="*70)
    print(f"\nGlycolysis parameters: {len(GLYCOLYSIS_PARAMS)}")
    print(f"TCA cycle parameters: {len(TCA_PARAMS)}")
    print(f"Total parameters: {len(ALL_PARAMETERS)}")
    print(f"Initial concentrations: {len(INITIAL_CONCENTRATIONS)}")
    
    print("\n" + "="*70)
    print("SAMPLE PARAMETERS (CRITICAL VALUES)")
    print("="*70)
    print(f"\nGAPDH Km(GAP): {GLYCOLYSIS_PARAMS['GAPDH_Km_GAP']} mM (in vivo)")
    print(f"GAPDH Km(NAD): {GLYCOLYSIS_PARAMS['GAPDH_Km_NAD']} mM (in vivo)")
    print(f"  Note: Traditional assay gives 0.09 mM (30x difference!)")
    
    print(f"\nHXK Km(glucose): {GLYCOLYSIS_PARAMS['HXK_Km_glucose']} mM")
    print(f"HXK Ki(T6P): {GLYCOLYSIS_PARAMS['HXK_Ki_T6P']} mM")
    print(f"  Note: Trehalose-6-P inhibition prevents 'turbo' phenotype")
    
    print(f"\nPYK Ka(F16BP): {GLYCOLYSIS_PARAMS['PYK_Ka_F16BP']} mM")
    print(f"  Note: Feedforward activation essential for homeostasis")
    
    print("\n" + "="*70)
