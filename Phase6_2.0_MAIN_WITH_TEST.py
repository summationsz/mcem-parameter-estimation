"""
PHASE 6 2.0: COMPLETE MULTI-ORGANISM VALIDATION SUITE (ENHANCED)
========================================================================
Full validation framework with:
- Descriptive session names
- Auto-visualization
- Auto-data export
- TEST mode for quick verification
"""
import numpy as np
from pathlib import Path
import time
import sys

from glycolysis_model import GlycolysisModel
from my_mcem_fixed import run_mcem
from scipy.integrate import solve_ivp

# Import analysis modules
try:
    from phase6_parameter_estimation import run_parameter_estimation
    from phase6_robustness import run_robustness_testing
    from phase6_bayesian_fispo import run_bayesian_fispo
    from phase6_complete_analysis import run_complete_analysis
    from phase6_generate_report import generate_comparative_report
except ImportError:
    print("Warning: Some analysis modules not found. Basic functionality available.")

# ============================================================================
# MENU FUNCTIONS
# ============================================================================

def print_header():
    """Print main header"""
    print("\n" + "="*80)
    print("PHASE 6 2.0: COMPLETE MULTI-ORGANISM VALIDATION SUITE")
    print("="*80)
    print("Cross-kingdom MCEM validation:")
    print("  > E. coli (Bacteria - Gram negative)")
    print("  > B. subtilis (Bacteria - Gram positive)")
    print("  > Arabidopsis (Plant)")
    print("  > S. cerevisiae (Yeast - Fungi)")
    print("="*80)

def print_main_menu():
    """Print main menu"""
    print("\n" + "="*80)
    print("MAIN MENU")
    print("-"*80)
    print("1) Parameter Estimation")
    print("2) Robustness Testing")
    print("3) Bayesian + FISPO Analysis")
    print("4) Complete Analysis")
    print("5) Generate Comparative Report (from existing results)")
    print("="*80)

def print_organism_menu():
    """Print organism selection menu"""
    print("\n" + "="*80)
    print("ORGANISM SELECTION")
    print("-"*80)
    print("1) E. coli           (Bacteria - Prokaryote)")
    print("2) B. subtilis       (Bacteria - Prokaryote)")
    print("3) Arabidopsis       (Plant - Eukaryote)")
    print("4) S. cerevisiae     (Yeast - Fungi)")
    print("5) All 4 organisms   (Batch processing)")
    print("="*80)

def print_mode_menu():
    """Print computation mode menu"""
    print("\n" + "="*80)
    print("COMPUTATION LEVEL")
    print("-"*80)
    print("A) FAST     - 100 iter, 1000 samples (~4-6 hrs per organism on i3)")
    print("B) BALANCED - 150 iter, 1500 samples (~8-12 hrs per organism on i3)")
    print("C) PRECISE  - 200 iter, 2000 samples (~24+ hrs per organism on i3)")
    print("D) TEST     - 20 iter, 500 samples (~15-20 min) [QUICK VERIFICATION]")
    print("="*80)

def get_main_choice():
    """Get main menu choice"""
    while True:
        print_main_menu()
        choice = input("Enter choice (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return int(choice)
        print("Invalid choice! Please enter 1-5.")

def get_organism_choice():
    """Get organism selection"""
    while True:
        print_organism_menu()
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            return ['ecoli']
        elif choice == '2':
            return ['bsubtilis']
        elif choice == '3':
            return ['arabidopsis']
        elif choice == '4':
            return ['yeast']
        elif choice == '5':
            return ['ecoli', 'bsubtilis', 'arabidopsis', 'yeast']
        else:
            print("Invalid choice! Please enter 1-5.")

def get_mode_choice():
    """Get computation mode"""
    while True:
        print_mode_menu()
        choice = input("Enter choice (A/B/C/D): ").strip().upper()
        
        if choice == 'A':
            return 'FAST', {'maxiter': 100, 'inner': 1000}
        elif choice == 'B':
            return 'BALANCED', {'maxiter': 150, 'inner': 1500}
        elif choice == 'C':
            return 'PRECISE', {'maxiter': 200, 'inner': 2000}
        elif choice == 'D':
            return 'TEST', {'maxiter': 20, 'inner': 500}
        else:
            print("Invalid choice! Please enter A, B, C, or D.")

# ============================================================================
# ENHANCED SESSION NAMING
# ============================================================================

def create_session_name(analysis_type, organisms, mode_name):
    """Create descriptive session name"""
    
    # Analysis type mapping
    analysis_names = {
        1: 'ParamEst',
        2: 'Robustness',
        3: 'Bayesian',
        4: 'CompleteAnalysis',
        5: 'Report'
    }
    
    # Organism names
    if len(organisms) == 4:
        org_name = 'AllOrganisms'
    elif len(organisms) == 1:
        org_map = {
            'ecoli': 'Ecoli',
            'bsubtilis': 'Bsubtilis',
            'arabidopsis': 'Arabidopsis',
            'yeast': 'Yeast'
        }
        org_name = org_map.get(organisms[0], 'Unknown')
    else:
        org_name = f'{len(organisms)}Organisms'
    
    # Create name
    session_num = len(list(Path("results").glob("Session*"))) + 1
    session_name = f"Session{session_num}_{analysis_names[analysis_type]}_{org_name}_{mode_name}"
    
    return session_name

# ============================================================================
# AUTO-VISUALIZATION AND DATA EXPORT
# ============================================================================

def run_post_analysis_exports(session_folder):
    """Run visualization and data export after analysis completes"""
    
    print("\n" + "="*80)
    print("POST-ANALYSIS: GENERATING OUTPUTS")
    print("="*80)
    print("\nAutomatically generating:")
    print("  [1/2] High-resolution visualizations")
    print("  [2/2] Excel & CSV data exports")
    print("="*80)
    
    # Run visualizations
    try:
        print("\n[1/2] Generating visualizations...")
        from generate_thesis_visualizations import ThesisVisualizer
        visualizer = ThesisVisualizer(session_folder)
        visualizer.generate_all()
        print("✓ Visualizations complete!")
    except Exception as e:
        print(f"⚠ Visualization generation failed: {e}")
        print("  (You can run manually: py -3 generate_thesis_visualizations.py)")
    
    # Run data exports
    try:
        print("\n[2/2] Exporting data tables...")
        from export_data_tables import DataExporter
        exporter = DataExporter(session_folder)
        exporter.export_all()
        print("✓ Data export complete!")
    except Exception as e:
        print(f"⚠ Data export failed: {e}")
        print("  (You can run manually: py -3 export_data_tables.py)")
    
    print("\n" + "="*80)
    print("ALL OUTPUTS GENERATED!")
    print("="*80)
    print(f"\nResults saved in: {session_folder}")
    print("\nGenerated:")
    print(f"  ✓ {session_folder}/visualizations/ (High-res plots)")
    print(f"  ✓ {session_folder}/data_exports/ (Excel & CSV files)")
    print("="*80)

# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    """Main program loop"""
    
    while True:
        # Print header
        print_header()
        
        # Get main menu choice
        choice = get_main_choice()
        
        # Option 5: Generate report (no organism/mode selection)
        if choice == 5:
            try:
                generate_comparative_report()
            except Exception as e:
                print(f"\nError generating report: {e}")
            input("\nPress ENTER to continue...")
            continue
        
        # For options 1-4: Get organism and mode selection
        organisms = get_organism_choice()
        mode_name, settings = get_mode_choice()
        
        # Confirmation
        print("\n" + "="*80)
        print("STARTING ANALYSIS")
        print("="*80)
        
        org_names = {
            'ecoli': 'E. coli',
            'bsubtilis': 'B. subtilis',
            'arabidopsis': 'Arabidopsis',
            'yeast': 'S. cerevisiae'
        }
        
        analysis_names = {
            1: 'Parameter Estimation',
            2: 'Robustness Testing',
            3: 'Bayesian + FISPO Analysis',
            4: 'Complete Analysis'
        }
        
        print(f"Analysis: {analysis_names[choice]}")
        print(f"Level: {mode_name}")
        
        # Show time estimate
        if mode_name == 'TEST':
            if len(organisms) == 1:
                time_est = "~15-20 minutes"
            else:
                time_est = f"~{len(organisms) * 15}-{len(organisms) * 20} minutes"
        else:
            time_est = "See menu for estimates"
        
        print(f"Estimated time: {time_est}")
        print("="*80)
        
        proceed = input("\nProceed? (Y/n): ").strip().lower()
        if proceed and proceed != 'y':
            print("\nCancelled.")
            continue
        
        # Create session folder with descriptive name
        session_name = create_session_name(choice, organisms, mode_name)
        session_folder = Path(f"results/{session_name}")
        session_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"\nSession: {session_name}")
        print(f"Location: {session_folder}")
        print("="*80)
        
        # Run selected analysis
        try:
            if choice == 1:
                run_parameter_estimation(organisms, mode_name, settings, session_folder)
            elif choice == 2:
                run_robustness_testing(organisms, mode_name, settings, session_folder)
            elif choice == 3:
                run_bayesian_fispo(organisms, mode_name, settings, session_folder)
            elif choice == 4:
                run_complete_analysis(organisms, mode_name, settings, session_folder)
            
            # Auto-generate visualizations and data exports
            if choice in [1, 4]:  # Parameter estimation or complete analysis
                run_post_analysis_exports(session_folder)
                
        except Exception as e:
            print(f"\n\nERROR: {e}")
            import traceback
            traceback.print_exc()
        
        # Ask to continue
        print("\n" + "="*80)
        again = input("Return to main menu? (Y/n): ").strip().lower()
        if again and again != 'y':
            break
    
    print("\n" + "="*80)
    print("PHASE 6 2.0 COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    main()
