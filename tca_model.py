"""
TCA Cycle (Citric Acid Cycle) ODE Model
=========================================

Based on:
- Korzeniewski & Zoladz (2003) - mitochondrial TCA cycle kinetics
- Includes pyruvate transport and pyruvate dehydrogenase

10 Reactions:
1. Pyruvate transport (cytosol → mitochondria)
2. Pyruvate dehydrogenase (Pyruvate → AcCoA)
3. Citrate synthase (AcCoA + OAA → Citrate)
4. Aconitase (Citrate ⇌ Isocitrate)
5. Isocitrate dehydrogenase (Isocitrate → α-KG)
6. α-Ketoglutarate dehydrogenase (α-KG → SucCoA)
7. Succinyl-CoA synthetase (SucCoA → Succinate)
8. Succinate dehydrogenase (Succinate → Fumarate)
9. Fumarase (Fumarate ⇌ Malate)
10. Malate dehydrogenase (Malate ⇌ OAA)

10 Dynamic metabolites:
PYR_mito, AcCoA, CIT, ISOCIT, aKG, SucCoA, SUC, FUM, MAL, OAA
"""

import numpy as np


class TCAModel:
    """TCA Cycle kinetic model"""
    
    def __init__(self, parameters):
        """
        Initialize TCA cycle model.
        
        Parameters:
        -----------
        parameters : dict
            Dictionary of kinetic parameters
        """
        self.params = parameters
        
        # State variable names
        self.state_names = [
            'PYR_mito',  # 0: Pyruvate (mitochondrial)
            'AcCoA',     # 1: Acetyl-CoA
            'CIT',       # 2: Citrate
            'ISOCIT',    # 3: Isocitrate
            'aKG',       # 4: α-Ketoglutarate
            'SucCoA',    # 5: Succinyl-CoA
            'SUC',       # 6: Succinate
            'FUM',       # 7: Fumarate
            'MAL',       # 8: Malate
            'OAA'        # 9: Oxaloacetate
        ]
        
        # Fixed cofactor concentrations (mM)
        self.CoA = 0.5
        self.NAD = 2.0
        self.NADH = 0.1
        self.FAD = 0.5
        self.FADH2 = 0.05
        self.GDP = 1.0
        self.GTP = 0.5
        self.Pi = 5.0
        self.Ca = 0.001  # Calcium for regulation
    
    def get_initial_state(self):
        """Get initial concentrations for all metabolites"""
        y0 = np.array([
            0.5,   # PYR_mito
            0.1,   # AcCoA
            0.5,   # CIT
            0.05,  # ISOCIT
            0.1,   # aKG
            0.05,  # SucCoA
            0.5,   # SUC
            0.2,   # FUM
            0.5,   # MAL
            0.01   # OAA (very low!)
        ])
        return y0
    
    def ode_system(self, t, y):
        """
        TCA cycle ODE system.
        
        Parameters:
        -----------
        t : float
            Time
        y : array
            Current state [PYR_mito, AcCoA, CIT, ISOCIT, aKG, SucCoA, SUC, FUM, MAL, OAA]
        
        Returns:
        --------
        dydt : array
            Rate of change for each metabolite
        """
        # Unpack state variables
        PYR_mito, AcCoA, CIT, ISOCIT, aKG, SucCoA, SUC, FUM, MAL, OAA = y
        
        # Ensure non-negative concentrations
        PYR_mito = max(PYR_mito, 1e-10)
        AcCoA = max(AcCoA, 1e-10)
        CIT = max(CIT, 1e-10)
        ISOCIT = max(ISOCIT, 1e-10)
        aKG = max(aKG, 1e-10)
        SucCoA = max(SucCoA, 1e-10)
        SUC = max(SUC, 1e-10)
        FUM = max(FUM, 1e-10)
        MAL = max(MAL, 1e-10)
        OAA = max(OAA, 1e-10)
        
        p = self.params
        
        # ============================================================
        # Reaction 1: Pyruvate Transport (cytosol → mitochondria)
        # ============================================================
        # Assume constant pyruvate supply from glycolysis
        PYR_supply = 0.5  # mM (from glycolysis endpoint)
        
        v_PYR_transport = (p['PYR_transport_Vmax'] * PYR_supply / 
                          (p['PYR_transport_Km'] + PYR_supply))
        
        # ============================================================
        # Reaction 2: Pyruvate Dehydrogenase (PDH)
        # Pyruvate + NAD + CoA → AcCoA + NADH + CO2
        # ============================================================
        v_PDH = (p['PDH_Vmax'] * PYR_mito * self.NAD * self.CoA /
                ((p['PDH_Km_pyruvate'] + PYR_mito) *
                 (p['PDH_Km_NAD'] + self.NAD) *
                 (p['PDH_Km_CoA'] + self.CoA)))
        
        # ============================================================
        # Reaction 3: Citrate Synthase (CS) - RATE LIMITING
        # AcCoA + OAA → Citrate + CoA
        # ============================================================
        # Inhibited by ATP and citrate
        v_CS = (p['CS_Vmax'] * AcCoA * OAA /
               ((p['CS_Km_AcCoA'] + AcCoA) * (p['CS_Km_OAA'] + OAA)) *
               (1 / (1 + CIT / p['CS_Ki_citrate'])))
        
        # ============================================================
        # Reaction 4: Aconitase (ACO)
        # Citrate ⇌ Isocitrate
        # ============================================================
        v_ACO_forward = (p['ACO_Vmax'] * CIT / 
                        (p['ACO_Km_citrate'] + CIT))
        
        v_ACO_reverse = (p['ACO_Vmax'] / p['ACO_Keq'] * ISOCIT /
                        (p['ACO_Km_isocitrate'] + ISOCIT))
        
        v_ACO = v_ACO_forward - v_ACO_reverse
        
        # ============================================================
        # Reaction 5: Isocitrate Dehydrogenase (ICDH) - KEY REGULATION
        # Isocitrate + NAD → α-KG + NADH + CO2
        # Activated by Ca2+ and ADP
        # ============================================================
        Ca_activation = 1 + self.Ca / p['ICDH_Ka_Ca']
        
        v_ICDH = (p['ICDH_Vmax'] * Ca_activation * ISOCIT * self.NAD /
                 ((p['ICDH_Km_isocitrate'] + ISOCIT) *
                  (p['ICDH_Km_NAD'] + self.NAD)))
        
        # ============================================================
        # Reaction 6: α-Ketoglutarate Dehydrogenase (KGDH) - RATE LIMITING
        # α-KG + NAD + CoA → SucCoA + NADH + CO2
        # Activated by Ca2+, inhibited by SucCoA and NADH
        # ============================================================
        Ca_activation = 1 + self.Ca / p['KGDH_Ka_Ca']
        SucCoA_inhibition = 1 / (1 + SucCoA / p['KGDH_Ki_SucCoA'])
        NADH_inhibition = 1 / (1 + self.NADH / p['KGDH_Ki_NADH'])
        
        v_KGDH = (p['KGDH_Vmax'] * Ca_activation * SucCoA_inhibition * NADH_inhibition *
                 aKG * self.NAD * self.CoA /
                 ((p['KGDH_Km_aKG'] + aKG) *
                  (p['KGDH_Km_NAD'] + self.NAD) *
                  (p['KGDH_Km_CoA'] + self.CoA)))
        
        # ============================================================
        # Reaction 7: Succinyl-CoA Synthetase (SCS)
        # SucCoA + GDP + Pi → Succinate + GTP + CoA
        # ============================================================
        v_SCS = (p['SCS_Vmax'] * SucCoA * self.GDP * self.Pi /
                ((p['SCS_Km_SucCoA'] + SucCoA) *
                 (p['SCS_Km_GDP'] + self.GDP) *
                 (p['SCS_Km_Pi'] + self.Pi)))
        
        # ============================================================
        # Reaction 8: Succinate Dehydrogenase (SDH) - Complex II
        # Succinate + FAD → Fumarate + FADH2
        # ============================================================
        v_SDH = (p['SDH_Vmax'] * SUC * self.FAD /
                ((p['SDH_Km_succinate'] + SUC) *
                 (p['SDH_Km_FAD'] + self.FAD)))
        
        # ============================================================
        # Reaction 9: Fumarase (FH)
        # Fumarate ⇌ Malate
        # ============================================================
        v_FH_forward = (p['FH_Vmax'] * FUM /
                       (p['FH_Km_fumarate'] + FUM))
        
        v_FH_reverse = (p['FH_Vmax'] / p['FH_Keq'] * MAL /
                       (p['FH_Km_malate'] + MAL))
        
        v_FH = v_FH_forward - v_FH_reverse
        
        # ============================================================
        # Reaction 10: Malate Dehydrogenase (MDH)
        # Malate + NAD ⇌ OAA + NADH
        # ============================================================
        v_MDH_forward = (p['MDH_Vmax'] * MAL * self.NAD /
                        ((p['MDH_Km_malate'] + MAL) *
                         (p['MDH_Km_NAD'] + self.NAD)))
        
        v_MDH_reverse = (p['MDH_Vmax'] / p['MDH_Keq'] * OAA * self.NADH /
                        ((p['MDH_Km_OAA'] + OAA) *
                         (p['MDH_Km_NADH'] + self.NADH)))
        
        v_MDH = v_MDH_forward - v_MDH_reverse
        
        # ============================================================
        # ODEs (mass balance for each metabolite)
        # ============================================================
        dydt = np.zeros(10)
        
        dydt[0] = v_PYR_transport - v_PDH                    # PYR_mito
        dydt[1] = v_PDH - v_CS                               # AcCoA
        dydt[2] = v_CS - v_ACO                               # CIT
        dydt[3] = v_ACO - v_ICDH                            # ISOCIT
        dydt[4] = v_ICDH - v_KGDH                           # aKG
        dydt[5] = v_KGDH - v_SCS                            # SucCoA
        dydt[6] = v_SCS - v_SDH                             # SUC
        dydt[7] = v_SDH - v_FH                              # FUM
        dydt[8] = v_FH - v_MDH                              # MAL
        dydt[9] = v_MDH - v_CS                              # OAA (completes cycle!)
        
        return dydt
    
    def get_fluxes(self, y):
        """
        Calculate reaction fluxes at given state.
        
        Returns dict of {reaction_name: flux}
        """
        PYR_mito, AcCoA, CIT, ISOCIT, aKG, SucCoA, SUC, FUM, MAL, OAA = y
        p = self.params
        
        PYR_supply = 0.5
        
        fluxes = {
            'v_PYR_transport': p['PYR_transport_Vmax'] * PYR_supply / (p['PYR_transport_Km'] + PYR_supply),
            'v_PDH': p['PDH_Vmax'] * PYR_mito * self.NAD * self.CoA / ((p['PDH_Km_pyruvate'] + PYR_mito) * (p['PDH_Km_NAD'] + self.NAD) * (p['PDH_Km_CoA'] + self.CoA)),
            'v_CS': p['CS_Vmax'] * AcCoA * OAA / ((p['CS_Km_AcCoA'] + AcCoA) * (p['CS_Km_OAA'] + OAA)),
            'v_ICDH': p['ICDH_Vmax'] * ISOCIT * self.NAD / ((p['ICDH_Km_isocitrate'] + ISOCIT) * (p['ICDH_Km_NAD'] + self.NAD)),
            'v_KGDH': p['KGDH_Vmax'] * aKG * self.NAD * self.CoA / ((p['KGDH_Km_aKG'] + aKG) * (p['KGDH_Km_NAD'] + self.NAD) * (p['KGDH_Km_CoA'] + self.CoA)),
            'v_SDH': p['SDH_Vmax'] * SUC * self.FAD / ((p['SDH_Km_succinate'] + SUC) * (p['SDH_Km_FAD'] + self.FAD))
        }
        
        return fluxes


if __name__ == "__main__":
    print("TCA Cycle Model Test")
    print("=" * 70)
    
    from kinetic_parameters import TCA_PARAMS
    
    model = TCAModel(TCA_PARAMS)
    y0 = model.get_initial_state()
    
    print(f"\nInitial state:")
    for i, name in enumerate(model.state_names):
        print(f"  {name:15s} = {y0[i]:.4f} mM")
    
    # Test ODE evaluation
    dydt = model.ode_system(0, y0)
    
    print(f"\nInitial rates:")
    for i, name in enumerate(model.state_names):
        print(f"  d{name}/dt = {dydt[i]:+.6f} mM/min")
    
    print("\n" + "=" * 70)
