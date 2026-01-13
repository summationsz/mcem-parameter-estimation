"""
PHASE 6 2.0: COMPLETE ANALYSIS MODULE (FULLY AUTOMATIC)
========================================================
Runs full validation suite WITHOUT pauses!
Perfect for overnight runs - no interaction needed!
"""
import numpy as np
from pathlib import Path
import time

from phase6_parameter_estimation import run_parameter_estimation
from phase6_robustness import run_robustness_testing
from phase6_bayesian_fispo import run_bayesian_fispo

def run_complete_analysis(organisms, mode_name, settings, session_folder):
    """
    Run complete analysis suite AUTOMATICALLY
    
    Runs in sequence WITHOUT pauses:
    1. Parameter Estimation
    2. Robustness Testing
    3. Bayesian + FISPO Analysis
    4. Generate comprehensive report
    
    Perfect for unattended overnight runs!
    """
    
    print("\n" + "="*80)
    print("COMPLETE ANALYSIS SUITE (AUTOMATIC MODE)")
    print("="*80)
    print("\nRunning full validation WITHOUT pauses:")
    print("  [1/3] Parameter Estimation")
    print("  [2/3] Robustness Testing")
    print("  [3/3] Bayesian + FISPO Analysis")
    print("\nNO USER INTERACTION NEEDED - Will run to completion!")
    print("="*80)
    
    total_start = time.time()
    
    # 1. Parameter Estimation
    print("\n\n" + "="*80)
    print("[1/3] PARAMETER ESTIMATION")
    print("="*80)
    try:
        run_parameter_estimation(organisms, mode_name, settings, session_folder)
        print("\n✓ Parameter estimation complete")
    except Exception as e:
        print(f"\n✗ Parameter estimation failed: {e}")
        import traceback
        traceback.print_exc()
    
    # NO PAUSE - Continue automatically!
    print("\n" + "-"*80)
    print("Continuing to robustness testing...")
    print("-"*80)
    time.sleep(2)  # Brief 2 second pause for readability
    
    # 2. Robustness Testing
    print("\n\n" + "="*80)
    print("[2/3] ROBUSTNESS TESTING")
    print("="*80)
    try:
        run_robustness_testing(organisms, mode_name, settings, session_folder)
        print("\n✓ Robustness testing complete")
    except Exception as e:
        print(f"\n✗ Robustness testing failed: {e}")
        import traceback
        traceback.print_exc()
    
    # NO PAUSE - Continue automatically!
    print("\n" + "-"*80)
    print("Continuing to Bayesian + FISPO analysis...")
    print("-"*80)
    time.sleep(2)  # Brief 2 second pause for readability
    
    # 3. Bayesian + FISPO
    print("\n\n" + "="*80)
    print("[3/3] BAYESIAN + FISPO ANALYSIS")
    print("="*80)
    try:
        run_bayesian_fispo(organisms, mode_name, settings, session_folder)
        print("\n✓ Bayesian + FISPO analysis complete")
    except Exception as e:
        print(f"\n✗ Bayesian + FISPO failed: {e}")
        import traceback
        traceback.print_exc()
    
    total_time = time.time() - total_start
    
    # Final summary
    print("\n\n" + "="*80)
    print("COMPLETE ANALYSIS FINISHED!")
    print("="*80)
    print(f"\nTotal runtime: {total_time/3600:.2f} hours")
    print(f"\nAll results saved in: {session_folder}")
    print("\nGenerated files:")
    print("  - parameter_estimation.npz")
    print("  - robustness.npz")
    print("  - bayesian_fispo.npz")
    print("="*80)
    
    # Save completion marker (with UTF-8 encoding for Windows)
    try:
        with open(session_folder / "COMPLETE_ANALYSIS.txt", 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("COMPLETE ANALYSIS SUMMARY\n")
            f.write("="*60 + "\n\n")
            f.write(f"Organisms: {', '.join(organisms)}\n")
            f.write(f"Mode: {mode_name}\n")
            f.write(f"Total runtime: {total_time/3600:.2f} hours\n\n")
            f.write("All analyses completed successfully! [OK]\n")
    except Exception as e:
        print(f"\nWarning: Could not write summary file: {e}")
