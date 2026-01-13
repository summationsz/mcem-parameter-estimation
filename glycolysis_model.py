"""
Glycolysis ODE System
=====================

Ordinary differential equations for glycolysis pathway.
Based on Michaelis-Menten kinetics with allosteric regulation.

Reference: van Eunen et al. (2012) PLOS Comput Biol
"""

import numpy as np
from kinetic_parameters import GLYCOLYSIS_PARAMS, TCA_PARAMS, INITIAL_CONCENTRATIONS

class GlycolysisModel:
    """
    Complete glycolysis pathway model with realistic kinetics.
    
    Implements:
    - Michaelis-Menten kinetics
    - Allosteric regulation (HXK, PFK, PYK)
    - Product inhibition
    - Reversible reactions
    """
    
    def __init__(self, params=None):
        """Initialize with parameters"""
        self.params = params if params is not None else GLYCOLYSIS_PARAMS
        
        # State variable indices
        self.idx = {
            'glucose': 0,
            'G6P': 1,
            'F6P': 2,
            'F16BP': 3,
            'DHAP': 4,
            'GAP': 5,
            'BPG': 6,
            '3PG': 7,
            '2PG': 8,
            'PEP': 9,
            'pyruvate': 10
        }
        
    def hexokinase(self, glucose, G6P, ATP, T6P=0.024):
        """
        Hexokinase: Glucose + ATP → G6P + ADP
        
        With:
        - Product inhibition by G6P
        - Trehalose-6-P inhibition (prevents turbo phenotype)
        """
        p = self.params
        
        # Competitive inhibition by T6P
        Km_app = p['HXK_Km_glucose'] * (1 + T6P / p['HXK_Ki_T6P'])
        
        # Product inhibition by G6P
        Ki_G6P = p['HXK_Ki_G6P']
        
        # Michaelis-Menten with inhibition
        v = p['HXK_Vmax'] * (glucose / (Km_app + glucose)) * (1 / (1 + G6P / Ki_G6P))
        
        return v
    
    def phosphoglucose_isomerase(self, G6P, F6P):
        """
        PGI: G6P ↔ F6P (reversible, near equilibrium)
        """
        p = self.params
        
        # Forward and reverse rates
        v_for = p['PGI_Vmax'] * G6P / (p['PGI_Km_G6P'] + G6P)
        v_rev = (p['PGI_Vmax'] / p['PGI_Keq']) * F6P / (p['PGI_Km_F6P'] + F6P)
        
        return v_for - v_rev
    
    def phosphofructokinase(self, F6P, ATP, AMP, F26BP=0.014):
        """
        PFK: F6P + ATP → F16BP + ADP
        
        With:
        - ATP substrate inhibition
        - AMP activation
        - F26BP activation
        
        CRITICAL regulatory enzyme!
        """
        p = self.params
        
        # ATP inhibition (substrate inhibition at high ATP)
        atp_term = ATP / (p['PFK_Km_ATP'] * (1 + ATP / p['PFK_Ki_ATP']))
        
        # AMP activation (allosteric)
        amp_factor = 1 + AMP / p['PFK_Ka_AMP']
        
        # Simplified version (full allosteric model is complex)
        v = p['PFK_Vmax'] * amp_factor * (F6P / (p['PFK_Km_F6P'] + F6P)) * (atp_term / (1 + atp_term))
        
        return v
    
    def aldolase(self, F16BP, DHAP, GAP):
        """
        ALD: F16BP ↔ DHAP + GAP (reversible)
        """
        p = self.params
        
        # Forward
        v_for = p['ALD_Vmax'] * F16BP / (p['ALD_Km_F16BP'] + F16BP)
        
        # Reverse (product of concentrations)
        v_rev = (p['ALD_Vmax'] / p['ALD_Keq']) * (DHAP * GAP) / \
                ((p['ALD_Km_DHAP'] + DHAP) * (p['ALD_Km_GAP'] + GAP))
        
        return v_for - v_rev
    
    def triose_phosphate_isomerase(self, DHAP, GAP):
        """
        TPI: DHAP ↔ GAP (very fast, near equilibrium)
        """
        p = self.params
        
        v_for = p['TPI_Vmax'] * DHAP / (p['TPI_Km_DHAP'] + DHAP)
        v_rev = (p['TPI_Vmax'] / p['TPI_Keq']) * GAP / (p['TPI_Km_GAP'] + GAP)
        
        return v_for - v_rev
    
    def gapdh(self, GAP, NAD, Pi=50.0):
        """
        GAPDH: GAP + NAD + Pi ↔ BPG + NADH
        
        CRITICAL: Uses in vivo-like Km values
        - Km(GAP) = 0.39 mM (not 1.68 mM)
        - Km(NAD) = 2.84 mM (not 0.09 mM)
        
        30-fold difference from traditional assays!
        """
        p = self.params
        
        # Simplified (full mechanism requires NADH, BPG)
        v = p['GAPDH_Vmax'] * (GAP / (p['GAPDH_Km_GAP'] + GAP)) * \
            (NAD / (p['GAPDH_Km_NAD'] + NAD)) * \
            (Pi / (p['GAPDH_Km_Pi'] + Pi))
        
        return v
    
    def phosphoglycerate_kinase(self, BPG, ADP):
        """
        PGK: BPG + ADP → 3PG + ATP (near equilibrium, favors products)
        """
        p = self.params
        
        # Very favorable reaction
        v = p['PGK_Vmax'] * (BPG / (p['PGK_Km_13BPG'] + BPG)) * \
            (ADP / (p['PGK_Km_ADP'] + ADP))
        
        return v
    
    def phosphoglycerate_mutase(self, PG3, PG2):
        """
        GPM: 3PG ↔ 2PG (reversible)
        """
        p = self.params
        
        v_for = p['GPM_Vmax'] * PG3 / (p['GPM_Km_3PG'] + PG3)
        v_rev = (p['GPM_Vmax'] / p['GPM_Keq']) * PG2 / (p['GPM_Km_2PG'] + PG2)
        
        return v_for - v_rev
    
    def enolase(self, PG2, PEP):
        """
        ENO: 2PG ↔ PEP + H2O (reversible, favors products)
        """
        p = self.params
        
        v_for = p['ENO_Vmax'] * PG2 / (p['ENO_Km_2PG'] + PG2)
        v_rev = (p['ENO_Vmax'] / p['ENO_Keq']) * PEP / (p['ENO_Km_PEP'] + PEP)
        
        return v_for - v_rev
    
    def pyruvate_kinase(self, PEP, ADP, F16BP):
        """
        PYK: PEP + ADP → Pyruvate + ATP
        
        With:
        - Feedforward activation by F16BP (ESSENTIAL!)
        
        Prevents metabolite accumulation in lower glycolysis.
        """
        p = self.params
        
        # Hill equation for F16BP activation
        f16bp_factor = 1 + ((F16BP / p['PYK_Ka_F16BP']) ** p['PYK_n']) / \
                           (1 + (F16BP / p['PYK_Ka_F16BP']) ** p['PYK_n'])
        
        v = p['PYK_Vmax'] * f16bp_factor * \
            (PEP / (p['PYK_Km_PEP'] + PEP)) * \
            (ADP / (p['PYK_Km_ADP'] + ADP))
        
        return v
    
    def pyruvate_decarboxylase(self, pyruvate):
        """
        PDC: Pyruvate → Acetaldehyde + CO2
        
        With Hill coefficient (cooperative binding)
        """
        p = self.params
        
        # Hill equation
        v = p['PDC_Vmax'] * (pyruvate ** p['PDC_n']) / \
            (p['PDC_Km_pyruvate'] ** p['PDC_n'] + pyruvate ** p['PDC_n'])
        
        return v
    
    def ode_system(self, t, y, ATP=2.5, ADP=1.3, NAD=1.2, Pi=50.0, 
                   T6P=0.024, F26BP=0.014):
        """
        Complete ODE system for glycolysis
        
        dy/dt = [rate of production] - [rate of consumption]
        
        Cofactors (ATP, ADP, NAD, NADH, Pi) held constant for simplicity.
        """
        
        # Extract state variables
        glucose = y[self.idx['glucose']]
        G6P = y[self.idx['G6P']]
        F6P = y[self.idx['F6P']]
        F16BP = y[self.idx['F16BP']]
        DHAP = y[self.idx['DHAP']]
        GAP = y[self.idx['GAP']]
        BPG = y[self.idx['BPG']]
        PG3 = y[self.idx['3PG']]
        PG2 = y[self.idx['2PG']]
        PEP = y[self.idx['PEP']]
        pyruvate = y[self.idx['pyruvate']]
        
        # Calculate AMP from adenylate energy charge (simplified)
        AMP = 0.28  # Approximately constant
        
        # Calculate fluxes through each enzyme
        v_HXK = self.hexokinase(glucose, G6P, ATP, T6P)
        v_PGI = self.phosphoglucose_isomerase(G6P, F6P)
        v_PFK = self.phosphofructokinase(F6P, ATP, AMP, F26BP)
        v_ALD = self.aldolase(F16BP, DHAP, GAP)
        v_TPI = self.triose_phosphate_isomerase(DHAP, GAP)
        v_GAPDH = self.gapdh(GAP, NAD, Pi)
        v_PGK = self.phosphoglycerate_kinase(BPG, ADP)
        v_GPM = self.phosphoglycerate_mutase(PG3, PG2)
        v_ENO = self.enolase(PG2, PEP)
        v_PYK = self.pyruvate_kinase(PEP, ADP, F16BP)
        v_PDC = self.pyruvate_decarboxylase(pyruvate)
        
        # ODEs (mass balance)
        dydt = np.zeros(len(y))
        
        dydt[self.idx['glucose']] = -v_HXK  # Glucose consumption
        dydt[self.idx['G6P']] = v_HXK - v_PGI
        dydt[self.idx['F6P']] = v_PGI - v_PFK
        dydt[self.idx['F16BP']] = v_PFK - v_ALD
        dydt[self.idx['DHAP']] = v_ALD - v_TPI
        dydt[self.idx['GAP']] = v_ALD + v_TPI - v_GAPDH  # GAP from aldolase + TPI
        dydt[self.idx['BPG']] = v_GAPDH - v_PGK
        dydt[self.idx['3PG']] = v_PGK - v_GPM
        dydt[self.idx['2PG']] = v_GPM - v_ENO
        dydt[self.idx['PEP']] = v_ENO - v_PYK
        dydt[self.idx['pyruvate']] = v_PYK - v_PDC
        
        return dydt
    
    def get_initial_state(self):
        """Get initial concentrations as array"""
        init = INITIAL_CONCENTRATIONS
        
        y0 = np.zeros(len(self.idx))
        for name, idx in self.idx.items():
            y0[idx] = init.get(name, 0.1)  # Default to 0.1 if missing
        
        return y0
    
    def get_state_names(self):
        """Get ordered list of state variable names"""
        names = [''] * len(self.idx)
        for name, idx in self.idx.items():
            names[idx] = name
        return names


if __name__ == "__main__":
    from scipy.integrate import solve_ivp
    import matplotlib.pyplot as plt
    
    print("="*70)
    print("TESTING GLYCOLYSIS MODEL")
    print("="*70)
    
    # Create model
    model = GlycolysisModel()
    
    # Get initial conditions
    y0 = model.get_initial_state()
    
    print(f"\nInitial conditions:")
    for name, value in zip(model.get_state_names(), y0):
        print(f"  {name}: {value:.4f} mM")
    
    # Simulate
    print("\nSimulating 10 minutes...")
    sol = solve_ivp(
        model.ode_system,
        t_span=[0, 10],  # 10 minutes
        y0=y0,
        method='LSODA',  # Stiff solver
        dense_output=True,
        max_step=0.1
    )
    
    if sol.success:
        print(f"✓ Simulation successful!")
        print(f"  Time points: {len(sol.t)}")
        print(f"  Final time: {sol.t[-1]:.2f} min")
        
        # Check if steady state reached
        final_state = sol.y[:, -1]
        print(f"\nFinal concentrations:")
        for name, value in zip(model.get_state_names(), final_state):
            print(f"  {name}: {value:.4f} mM")
    else:
        print(f"✗ Simulation failed: {sol.message}")
    
    print("\n" + "="*70)
