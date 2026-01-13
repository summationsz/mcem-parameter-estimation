"""
PHASE 6: COMPARATIVE REPORT GENERATOR (FIXED FOR NEW FORMAT)
============================================================
Generates text-based comparative report from Phase 6 results.
Works with the new parameter estimation data structure.
"""

import numpy as np
from pathlib import Path

def generate_comparative_report():
    """Generate comparative report from existing results"""
    
    print("\n" + "="*80)
    print("GENERATING COMPARATIVE REPORT")
    print("="*80)
    
    # Find available result sessions
    results_path = Path("results")
    
    if not results_path.exists():
        print("\n✗ Error: No 'results' folder found!")
        return
    
    # Get all sessions with parameter estimation results
    sessions = []
    for session_folder in sorted(results_path.glob("Session*")):
        param_file = session_folder / 'parameter_estimation.npz'
        if param_file.exists():
            sessions.append(session_folder)
    
    if not sessions:
        print("\n✗ Error: No sessions with parameter estimation results found!")
        print("  Run parameter estimation first (Option 1 or 4)")
        return
    
    # Show available sessions
    print("\nAvailable sessions:")
    for idx, session in enumerate(sessions, 1):
        print(f"  [{idx:2d}] {session.name}")
    
    print("\n" + "="*80)
    
    # Let user select session or use most recent
    choice = input(f"\nSelect session (1-{len(sessions)}) or ENTER for most recent: ").strip()
    
    if choice:
        try:
            session_idx = int(choice) - 1
            if 0 <= session_idx < len(sessions):
                selected_session = sessions[session_idx]
            else:
                print("Invalid choice! Using most recent.")
                selected_session = sessions[-1]
        except ValueError:
            print("Invalid input! Using most recent.")
            selected_session = sessions[-1]
    else:
        selected_session = sessions[-1]
    
    print(f"\nGenerating report for: {selected_session.name}")
    
    # Load results
    param_file = selected_session / 'parameter_estimation.npz'
    
    try:
        data = np.load(param_file, allow_pickle=True)
        results = data['results']
    except Exception as e:
        print(f"\n✗ Error loading results: {e}")
        return
    
    # Generate report
    report_file = selected_session / 'COMPARATIVE_REPORT.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("="*80 + "\n")
        f.write("PHASE 6 2.0: COMPARATIVE ANALYSIS REPORT\n")
        f.write("="*80 + "\n")
        f.write(f"\nSession: {selected_session.name}\n")
        f.write(f"Generated: {Path().absolute()}\n")
        f.write("\n" + "="*80 + "\n\n")
        
        # Overall Summary
        f.write("OVERALL SUMMARY\n")
        f.write("-"*80 + "\n")
        f.write(f"Total organisms analyzed: {len(results)}\n")
        
        total_params = sum(r['total_params'] for r in results)
        f.write(f"Total parameters estimated: {total_params}\n")
        
        all_errors = []
        for r in results:
            all_errors.append(r['overall_error'])
        
        f.write(f"Average error across all organisms: {np.mean(all_errors):.2f}%\n")
        f.write(f"Best performing organism: {results[np.argmin(all_errors)]['organism']} ({min(all_errors):.2f}%)\n")
        f.write(f"Total runtime: {sum(r['total_runtime'] for r in results)/3600:.2f} hours\n")
        f.write("\n")
        
        # Per-Organism Results
        f.write("="*80 + "\n")
        f.write("ORGANISM-SPECIFIC RESULTS\n")
        f.write("="*80 + "\n\n")
        
        for organism_result in results:
            organism = organism_result['organism']
            total_params = organism_result['total_params']
            overall_error = organism_result['overall_error']
            runtime = organism_result['total_runtime']
            
            f.write("-"*80 + "\n")
            f.write(f"ORGANISM: {organism}\n")
            f.write("-"*80 + "\n")
            f.write(f"Total parameters: {total_params}\n")
            f.write(f"Overall error: {overall_error:.2f}%\n")
            f.write(f"Runtime: {runtime/60:.1f} minutes ({runtime/3600:.2f} hours)\n")
            f.write("\n")
            
            # Pathway breakdown
            for pathway_data in organism_result['pathway_results']:
                pathway = pathway_data['pathway']
                n_params = len(pathway_data['parameters'])
                errors = pathway_data['errors']
                pathway_runtime = pathway_data['runtime']
                
                f.write(f"  {pathway.upper()} Pathway:\n")
                f.write(f"    Parameters: {n_params}\n")
                f.write(f"    Mean error: {np.mean(errors):.2f}%\n")
                f.write(f"    Median error: {np.median(errors):.2f}%\n")
                f.write(f"    Std dev: {np.std(errors):.2f}%\n")
                f.write(f"    Min error: {np.min(errors):.2f}%\n")
                f.write(f"    Max error: {np.max(errors):.2f}%\n")
                f.write(f"    Runtime: {pathway_runtime/60:.1f} min\n")
                f.write("\n")
        
        # Comparative Analysis
        f.write("="*80 + "\n")
        f.write("COMPARATIVE ANALYSIS\n")
        f.write("="*80 + "\n\n")
        
        # Sort by performance
        sorted_results = sorted(results, key=lambda x: x['overall_error'])
        
        f.write("Performance Ranking (by error):\n")
        f.write("-"*80 + "\n")
        for idx, r in enumerate(sorted_results, 1):
            f.write(f"  {idx}. {r['organism']:<20} {r['overall_error']:6.2f}%  ")
            f.write(f"({r['total_params']} params, {r['total_runtime']/3600:.2f} hrs)\n")
        
        f.write("\n")
        
        # Parameters by organism type
        f.write("Parameters by Kingdom:\n")
        f.write("-"*80 + "\n")
        
        kingdoms = {
            'Bacteria': ['E. coli', 'B. subtilis'],
            'Plant': ['Arabidopsis'],
            'Fungi': ['S. cerevisiae']
        }
        
        for kingdom, org_names in kingdoms.items():
            kingdom_results = [r for r in results if r['organism'] in org_names]
            if kingdom_results:
                avg_error = np.mean([r['overall_error'] for r in kingdom_results])
                total_params = sum(r['total_params'] for r in kingdom_results)
                f.write(f"  {kingdom:<15} {len(kingdom_results)} organism(s), ")
                f.write(f"{total_params} total params, {avg_error:.2f}% avg error\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*80 + "\n")
    
    print(f"\n✓ Report generated: {report_file}")
    print(f"\n{report_file.read_text(encoding='utf-8')}")
    print("\n" + "="*80)
    print("REPORT GENERATION COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    generate_comparative_report()
