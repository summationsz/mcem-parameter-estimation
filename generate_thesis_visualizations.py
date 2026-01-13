"""
THESIS-QUALITY VISUALIZATION GENERATOR (WITH FOLDER SELECTOR)
==============================================================
Can run in two modes:
1. With command line argument: py -3 script.py results/SessionX
2. Interactive mode: Shows menu of available sessions

Produces 12 files per organism:
- 9 individual plots (300 DPI, high-res)
- 2 grouped plots (related analyses)
- 1 overview plot (all 9 for reference)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from pathlib import Path
import json

# High-quality settings
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.linewidth'] = 1.2

class ThesisVisualizer:
    """Generate publication-quality visualizations"""
    
    def __init__(self, results_folder):
        """Initialize with results folder path"""
        self.results_folder = Path(results_folder)
        self.output_folder = self.results_folder / 'visualizations'
        self.output_folder.mkdir(exist_ok=True)
        
        print(f"\n{'='*70}")
        print(f"THESIS VISUALIZATION GENERATOR")
        print(f"{'='*70}")
        print(f"Results: {self.results_folder}")
        print(f"Output: {self.output_folder}")
        print(f"{'='*70}\n")
    
    def load_results(self):
        """Load results from npz file"""
        result_file = self.results_folder / 'parameter_estimation.npz'
        
        if not result_file.exists():
            raise FileNotFoundError(f"Results file not found: {result_file}")
        
        data = np.load(result_file, allow_pickle=True)
        results = data['results']
        
        print(f"✓ Loaded results for {len(results)} organisms")
        return results
    
    def create_individual_plots(self, organism_result, organism_name):
        """Create individual high-res plots"""
        
        print(f"\n  Creating individual plots for {organism_name}...")
        
        org_folder = self.output_folder / organism_name.replace(' ', '_')
        org_folder.mkdir(exist_ok=True)
        
        pathway_results = organism_result['pathway_results']
        
        plot_count = 0
        
        for pathway_data in pathway_results:
            pathway = pathway_data['pathway']
            params = pathway_data['parameters']
            estimated = np.array(pathway_data['estimated'])
            
            if 'true_values' in pathway_data:
                true_vals = np.array(pathway_data['true_values'])
            else:
                true_vals = np.array(pathway_data['initial_guess'])
            
            errors = pathway_data['errors']
            
            # Plot 1: Parameter Estimates vs True Values
            plot_count += 1
            fig, ax = plt.subplots(figsize=(10, 6))
            x = np.arange(len(params))
            ax.scatter(x, true_vals, label='True Values', marker='o', s=80, alpha=0.6, color='blue')
            ax.scatter(x, estimated, label='Estimated', marker='x', s=80, alpha=0.6, color='red')
            ax.set_xlabel('Parameter Index', fontsize=12, fontweight='bold')
            ax.set_ylabel('Parameter Value', fontsize=12, fontweight='bold')
            ax.set_title(f'{organism_name} - {pathway.upper()}: Parameter Estimation', 
                        fontsize=14, fontweight='bold')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(org_folder / f'{plot_count:02d}_{pathway}_param_estimates.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"    ✓ Plot {plot_count}: {pathway} parameter estimates")
            
            # Plot 2: Relative Errors
            plot_count += 1
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['green' if e < 10 else 'orange' if e < 20 else 'red' for e in errors]
            ax.bar(x, errors, color=colors, alpha=0.7, edgecolor='black', linewidth=1.2)
            ax.axhline(y=np.mean(errors), color='blue', linestyle='--', linewidth=2, 
                      label=f'Mean Error: {np.mean(errors):.2f}%')
            ax.set_xlabel('Parameter Index', fontsize=12, fontweight='bold')
            ax.set_ylabel('Relative Error (%)', fontsize=12, fontweight='bold')
            ax.set_title(f'{organism_name} - {pathway.upper()}: Estimation Errors', 
                        fontsize=14, fontweight='bold')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            plt.savefig(org_folder / f'{plot_count:02d}_{pathway}_errors.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"    ✓ Plot {plot_count}: {pathway} errors")
            
            # Plot 3: Error Distribution
            plot_count += 1
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(errors, bins=20, color='skyblue', edgecolor='black', linewidth=1.2, alpha=0.7)
            ax.axvline(x=np.mean(errors), color='red', linestyle='--', linewidth=2, 
                      label=f'Mean: {np.mean(errors):.2f}%')
            ax.axvline(x=np.median(errors), color='green', linestyle='--', linewidth=2, 
                      label=f'Median: {np.median(errors):.2f}%')
            ax.set_xlabel('Relative Error (%)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
            ax.set_title(f'{organism_name} - {pathway.upper()}: Error Distribution', 
                        fontsize=14, fontweight='bold')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            plt.savefig(org_folder / f'{plot_count:02d}_{pathway}_error_dist.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"    ✓ Plot {plot_count}: {pathway} error distribution")
        
        # Overall organism summary plots
        all_errors = []
        for pathway_data in pathway_results:
            all_errors.extend(pathway_data['errors'])
        
        # Plot: Overall Error Summary
        plot_count += 1
        fig, ax = plt.subplots(figsize=(10, 6))
        pathway_names = [p['pathway'].upper() for p in pathway_results]
        pathway_errors = [np.mean(p['errors']) for p in pathway_results]
        colors_pathway = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        ax.bar(pathway_names, pathway_errors, color=colors_pathway[:len(pathway_names)], 
               alpha=0.7, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Mean Relative Error (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'{organism_name} - Overall Pathway Performance', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(org_folder / f'{plot_count:02d}_overall_pathway_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"    ✓ Plot {plot_count}: Overall pathway performance")
        
        # Plot: Box plot of all errors
        plot_count += 1
        fig, ax = plt.subplots(figsize=(10, 6))
        error_data = [p['errors'] for p in pathway_results]
        bp = ax.boxplot(error_data, tick_labels=pathway_names, patch_artist=True,
                       widths=0.6, showmeans=True)
        for patch, color in zip(bp['boxes'], colors_pathway[:len(pathway_names)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        ax.set_ylabel('Relative Error (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'{organism_name} - Error Distribution by Pathway', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(org_folder / f'{plot_count:02d}_error_boxplot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"    ✓ Plot {plot_count}: Error boxplot")
        
        return plot_count
    
    def create_grouped_plots(self, organism_result, organism_name):
        """Create 2 grouped plots combining related analyses"""
        
        print(f"\n  Creating grouped plots for {organism_name}...")
        
        org_folder = self.output_folder / organism_name.replace(' ', '_')
        pathway_results = organism_result['pathway_results']
        
        # Grouped Plot 1: Parameter Estimates (all pathways)
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
        
        for idx, pathway_data in enumerate(pathway_results):
            pathway = pathway_data['pathway']
            params = pathway_data['parameters']
            estimated = np.array(pathway_data['estimated'])
            
            if 'true_values' in pathway_data:
                true_vals = np.array(pathway_data['true_values'])
            else:
                true_vals = np.array(pathway_data['initial_guess'])
            
            ax = fig.add_subplot(gs[idx])
            x = np.arange(len(params))
            ax.scatter(x, true_vals, label='True', marker='o', s=60, alpha=0.6)
            ax.scatter(x, estimated, label='Estimated', marker='x', s=60, alpha=0.6)
            ax.set_xlabel('Parameter Index', fontsize=11, fontweight='bold')
            ax.set_ylabel('Value', fontsize=11, fontweight='bold')
            ax.set_title(f'{pathway.upper()} Pathway', fontsize=12, fontweight='bold')
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
        
        fig.suptitle(f'{organism_name} - All Pathways Parameter Estimation', 
                    fontsize=16, fontweight='bold')
        plt.savefig(org_folder / 'GROUPED_01_all_pathways_estimates.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"    ✓ Grouped plot 1: All pathways estimates")
        
        # Grouped Plot 2: Error Analysis (all pathways)
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
        
        for idx, pathway_data in enumerate(pathway_results):
            pathway = pathway_data['pathway']
            errors = pathway_data['errors']
            
            ax = fig.add_subplot(gs[idx])
            x = np.arange(len(errors))
            colors = ['green' if e < 10 else 'orange' if e < 20 else 'red' for e in errors]
            ax.bar(x, errors, color=colors, alpha=0.7, edgecolor='black')
            ax.axhline(y=np.mean(errors), color='blue', linestyle='--', linewidth=2,
                      label=f'Mean: {np.mean(errors):.2f}%')
            ax.set_xlabel('Parameter Index', fontsize=11, fontweight='bold')
            ax.set_ylabel('Error (%)', fontsize=11, fontweight='bold')
            ax.set_title(f'{pathway.upper()} Errors', fontsize=12, fontweight='bold')
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3, axis='y')
        
        fig.suptitle(f'{organism_name} - All Pathways Error Analysis', 
                    fontsize=16, fontweight='bold')
        plt.savefig(org_folder / 'GROUPED_02_all_pathways_errors.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"    ✓ Grouped plot 2: All pathways errors")
    
    def create_overview_plot(self, organism_result, organism_name):
        """Create 1 overview plot with all 9 sub-analyses"""
        
        print(f"\n  Creating overview plot for {organism_name}...")
        
        org_folder = self.output_folder / organism_name.replace(' ', '_')
        pathway_results = organism_result['pathway_results']
        
        fig = plt.figure(figsize=(20, 12))
        gs = GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.4)
        
        plot_idx = 0
        
        for pathway_data in pathway_results:
            pathway = pathway_data['pathway']
            params = pathway_data['parameters']
            estimated = np.array(pathway_data['estimated'])
            
            if 'true_values' in pathway_data:
                true_vals = np.array(pathway_data['true_values'])
            else:
                true_vals = np.array(pathway_data['initial_guess'])
            
            errors = pathway_data['errors']
            
            # Sub-plot 1: Estimates
            ax = fig.add_subplot(gs[plot_idx])
            x = np.arange(len(params))
            ax.scatter(x, true_vals, label='True', marker='o', s=40, alpha=0.6)
            ax.scatter(x, estimated, label='Est', marker='x', s=40, alpha=0.6)
            ax.set_title(f'{pathway.upper()}: Estimates', fontsize=10, fontweight='bold')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
            plot_idx += 1
            
            # Sub-plot 2: Errors
            ax = fig.add_subplot(gs[plot_idx])
            colors = ['green' if e < 10 else 'orange' if e < 20 else 'red' for e in errors]
            ax.bar(x, errors, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
            ax.axhline(y=np.mean(errors), color='blue', linestyle='--', linewidth=1.5)
            ax.set_title(f'{pathway.upper()}: Errors', fontsize=10, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            plot_idx += 1
            
            # Sub-plot 3: Distribution
            ax = fig.add_subplot(gs[plot_idx])
            ax.hist(errors, bins=15, color='skyblue', edgecolor='black', linewidth=0.8, alpha=0.7)
            ax.axvline(x=np.mean(errors), color='red', linestyle='--', linewidth=1.5)
            ax.set_title(f'{pathway.upper()}: Distribution', fontsize=10, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            plot_idx += 1
        
        fig.suptitle(f'{organism_name} - Complete Analysis Overview', 
                    fontsize=18, fontweight='bold')
        plt.savefig(org_folder / 'OVERVIEW_complete_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"    ✓ Overview plot: Complete analysis")
    
    def generate_all(self):
        """Generate all visualizations for all organisms"""
        
        results = self.load_results()
        
        summary = []
        
        for organism_result in results:
            organism_name = organism_result['organism']
            
            print(f"\n{'='*70}")
            print(f"PROCESSING: {organism_name}")
            print(f"{'='*70}")
            
            # Individual plots
            n_individual = self.create_individual_plots(organism_result, organism_name)
            
            # Grouped plots
            self.create_grouped_plots(organism_result, organism_name)
            
            # Overview plot
            self.create_overview_plot(organism_result, organism_name)
            
            total_files = n_individual + 3
            
            org_folder = self.output_folder / organism_name.replace(' ', '_')
            
            summary.append({
                'organism': organism_name,
                'files': total_files,
                'folder': str(org_folder)
            })
            
            print(f"\n  ✓ Generated {total_files} visualization files")
            print(f"  ✓ Saved in: {org_folder}")
        
        # Print final summary
        print(f"\n{'='*70}")
        print("VISUALIZATION GENERATION COMPLETE!")
        print(f"{'='*70}")
        print(f"\nGenerated visualizations for {len(summary)} organisms:")
        print(f"\nOutput location: {self.output_folder}")
        for item in summary:
            print(f"\n  {item['organism']}:")
            print(f"    Files: {item['files']}")
            print(f"    Folder: {item['folder']}")
        
        print(f"\n{'='*70}")
        print("All plots are 300 DPI, publication-ready!")
        print("Use individual plots for detailed analysis in thesis.")
        print("Use grouped/overview plots for presentations.")
        print(f"{'='*70}\n")

def select_results_folder():
    """Interactive folder selection"""
    
    results_path = Path("results")
    
    if not results_path.exists():
        print("\n✗ Error: 'results' folder not found!")
        print("  Make sure you're in the Phase 6 2.0 directory.")
        return None
    
    # Get all session folders
    session_folders = sorted(results_path.glob("Session*"), reverse=True)
    
    if not session_folders:
        print("\n✗ Error: No session folders found in 'results'!")
        return None
    
    print("\n" + "="*70)
    print("AVAILABLE RESULT SESSIONS")
    print("="*70)
    print("\nSelect a session to visualize:\n")
    
    for idx, folder in enumerate(session_folders, 1):
        # Check if results exist
        has_results = (folder / 'parameter_estimation.npz').exists()
        has_viz = (folder / 'visualizations').exists()
        has_exports = (folder / 'data_exports').exists()
        
        status = []
        if has_results:
            status.append("✓ Results")
        if has_viz:
            status.append("✓ Viz")
        if has_exports:
            status.append("✓ Exports")
        
        status_str = " | ".join(status) if status else "⚠ No results"
        
        print(f"  [{idx:2d}] {folder.name:<50} {status_str}")
    
    print("\n" + "="*70)
    
    while True:
        try:
            choice = input(f"\nEnter choice (1-{len(session_folders)}) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(session_folders):
                selected = session_folders[choice_num - 1]
                
                # Verify it has results
                if not (selected / 'parameter_estimation.npz').exists():
                    print(f"\n⚠ Warning: {selected.name} has no parameter_estimation.npz file!")
                    retry = input("Select anyway? (y/N): ").strip().lower()
                    if retry != 'y':
                        continue
                
                return selected
            else:
                print(f"Invalid choice! Please enter 1-{len(session_folders)}")
        
        except ValueError:
            print("Invalid input! Please enter a number.")
    
    return None

def main():
    """Main function with enhanced interface"""
    import sys
    
    # Mode 1: Command line argument
    if len(sys.argv) >= 2:
        results_folder = sys.argv[1]
        
        if not Path(results_folder).exists():
            print(f"\n✗ Error: Results folder not found: {results_folder}")
            return
        
        print("\n" + "="*70)
        print("RUNNING IN DIRECT MODE")
        print("="*70)
        
    # Mode 2: Interactive selection
    else:
        print("\n" + "="*70)
        print("THESIS VISUALIZATION GENERATOR")
        print("="*70)
        print("\nRunning in INTERACTIVE MODE...")
        
        results_folder = select_results_folder()
        
        if results_folder is None:
            print("\nCancelled.")
            return
    
    # Run visualization
    visualizer = ThesisVisualizer(results_folder)
    visualizer.generate_all()
    
    # Ask about data export
    print("\n" + "="*70)
    export_data = input("\nGenerate Excel/CSV data exports too? (Y/n): ").strip().lower()
    
    if not export_data or export_data == 'y':
        try:
            from export_data_tables import DataExporter
            exporter = DataExporter(results_folder)
            exporter.export_all()
        except Exception as e:
            print(f"\n⚠ Data export failed: {e}")
            print("  (You can run manually: py -3 export_data_tables.py)")
    
    print("\n" + "="*70)
    print("ALL DONE!")
    print("="*70)
    print(f"\nOutputs saved in: {results_folder}")
    print("  ✓ visualizations/ folder")
    if not export_data or export_data == 'y':
        print("  ✓ data_exports/ folder")
    print("="*70)

if __name__ == "__main__":
    main()
