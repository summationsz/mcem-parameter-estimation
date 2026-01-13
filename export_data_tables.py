"""
DATA EXPORT MODULE - EXCEL & CSV GENERATION
============================================
Exports Phase 6 results to Excel workbooks and CSV files for easy analysis.

Generates:
- Master Excel workbook with multiple sheets
- Individual CSV files for each analysis
- Summary tables and statistics
"""

import numpy as np
import pandas as pd
from pathlib import Path
import json

class DataExporter:
    """Export Phase 6 results to Excel and CSV formats"""
    
    def __init__(self, results_folder):
        """Initialize with results folder path"""
        self.results_folder = Path(results_folder)
        self.output_folder = self.results_folder / 'data_exports'
        self.output_folder.mkdir(exist_ok=True)
        
        print(f"\n{'='*70}")
        print(f"DATA EXPORT GENERATOR")
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
        
        print(f"✓ Loaded results for {len(results)} organisms\n")
        return results
    
    def export_parameter_table(self, results):
        """Export parameter estimation results to Excel/CSV"""
        
        print("  [1/5] Exporting parameter tables...")
        
        all_data = []
        
        for organism_result in results:
            organism = organism_result['organism']
            
            for pathway_data in organism_result['pathway_results']:
                pathway = pathway_data['pathway']
                params = pathway_data['parameters']
                
                if 'true_values' in pathway_data:
                    true_vals = pathway_data['true_values']
                else:
                    true_vals = pathway_data['initial_guess']
                
                estimated = pathway_data['estimated']
                errors = pathway_data['errors']
                
                if 'std_devs' in pathway_data:
                    std_devs = pathway_data['std_devs']
                else:
                    std_devs = [0] * len(params)
                
                for i, param in enumerate(params):
                    all_data.append({
                        'Organism': organism,
                        'Pathway': pathway.upper(),
                        'Parameter': param,
                        'True_Value': true_vals[i],
                        'Estimated_Value': estimated[i],
                        'Std_Dev': std_devs[i],
                        'Absolute_Error': abs(estimated[i] - true_vals[i]),
                        'Relative_Error_%': errors[i],
                    })
        
        df = pd.DataFrame(all_data)
        
        # Export to Excel
        excel_file = self.output_folder / 'parameter_estimates.xlsx'
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # All data
            df.to_excel(writer, sheet_name='All_Parameters', index=False)
            
            # By organism
            for organism in df['Organism'].unique():
                org_df = df[df['Organism'] == organism]
                sheet_name = organism.replace(' ', '_')[:31]  # Excel limit
                org_df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"    ✓ Excel: {excel_file.name}")
        
        # Export to CSV
        csv_file = self.output_folder / 'parameter_estimates.csv'
        df.to_csv(csv_file, index=False)
        print(f"    ✓ CSV: {csv_file.name}")
        
        return df
    
    def export_summary_statistics(self, results):
        """Export summary statistics to Excel/CSV"""
        
        print("  [2/5] Exporting summary statistics...")
        
        summary_data = []
        
        for organism_result in results:
            organism = organism_result['organism']
            total_params = organism_result['total_params']
            overall_error = organism_result['overall_error']
            total_runtime = organism_result['total_runtime']
            
            for pathway_data in organism_result['pathway_results']:
                pathway = pathway_data['pathway']
                errors = pathway_data['errors']
                runtime = pathway_data['runtime']
                
                summary_data.append({
                    'Organism': organism,
                    'Pathway': pathway.upper(),
                    'Num_Parameters': len(pathway_data['parameters']),
                    'Mean_Error_%': np.mean(errors),
                    'Median_Error_%': np.median(errors),
                    'Std_Error_%': np.std(errors),
                    'Min_Error_%': np.min(errors),
                    'Max_Error_%': np.max(errors),
                    'Runtime_Minutes': runtime / 60,
                    'Runtime_Hours': runtime / 3600,
                })
        
        df = pd.DataFrame(summary_data)
        
        # Export to Excel
        excel_file = self.output_folder / 'summary_statistics.xlsx'
        df.to_excel(excel_file, index=False)
        print(f"    ✓ Excel: {excel_file.name}")
        
        # Export to CSV
        csv_file = self.output_folder / 'summary_statistics.csv'
        df.to_csv(csv_file, index=False)
        print(f"    ✓ CSV: {csv_file.name}")
        
        return df
    
    def export_organism_comparison(self, results):
        """Export organism comparison table"""
        
        print("  [3/5] Exporting organism comparison...")
        
        comparison_data = []
        
        for organism_result in results:
            organism = organism_result['organism']
            
            glyc_data = [p for p in organism_result['pathway_results'] if p['pathway'] == 'glycolysis']
            tca_data = [p for p in organism_result['pathway_results'] if p['pathway'] == 'tca']
            
            glyc_error = np.mean(glyc_data[0]['errors']) if glyc_data else None
            tca_error = np.mean(tca_data[0]['errors']) if tca_data else None
            
            comparison_data.append({
                'Organism': organism,
                'Total_Parameters': organism_result['total_params'],
                'Glycolysis_Params': len(glyc_data[0]['parameters']) if glyc_data else 0,
                'TCA_Params': len(tca_data[0]['parameters']) if tca_data else 0,
                'Glycolysis_Error_%': glyc_error if glyc_error else 'N/A',
                'TCA_Error_%': tca_error if tca_error else 'N/A',
                'Overall_Error_%': organism_result['overall_error'],
                'Total_Runtime_Hours': organism_result['total_runtime'] / 3600,
            })
        
        df = pd.DataFrame(comparison_data)
        
        # Export to Excel
        excel_file = self.output_folder / 'organism_comparison.xlsx'
        df.to_excel(excel_file, index=False)
        print(f"    ✓ Excel: {excel_file.name}")
        
        # Export to CSV
        csv_file = self.output_folder / 'organism_comparison.csv'
        df.to_csv(csv_file, index=False)
        print(f"    ✓ CSV: {csv_file.name}")
        
        return df
    
    def export_error_distributions(self, results):
        """Export error distribution data"""
        
        print("  [4/5] Exporting error distributions...")
        
        all_errors = []
        
        for organism_result in results:
            organism = organism_result['organism']
            
            for pathway_data in organism_result['pathway_results']:
                pathway = pathway_data['pathway']
                errors = pathway_data['errors']
                
                for error in errors:
                    all_errors.append({
                        'Organism': organism,
                        'Pathway': pathway.upper(),
                        'Relative_Error_%': error
                    })
        
        df = pd.DataFrame(all_errors)
        
        # Export to CSV
        csv_file = self.output_folder / 'error_distributions.csv'
        df.to_csv(csv_file, index=False)
        print(f"    ✓ CSV: {csv_file.name}")
        
        return df
    
    def export_master_workbook(self, param_df, summary_df, comparison_df, error_df):
        """Create master Excel workbook with all data"""
        
        print("  [5/5] Creating master workbook...")
        
        master_file = self.output_folder / 'MASTER_Results.xlsx'
        
        with pd.ExcelWriter(master_file, engine='openpyxl') as writer:
            # Summary page
            comparison_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Statistics
            summary_df.to_excel(writer, sheet_name='Statistics', index=False)
            
            # All parameters
            param_df.to_excel(writer, sheet_name='All_Parameters', index=False)
            
            # Error distributions
            error_df.to_excel(writer, sheet_name='Error_Distributions', index=False)
            
            # By organism
            for organism in param_df['Organism'].unique():
                org_params = param_df[param_df['Organism'] == organism]
                sheet_name = organism.replace(' ', '_')[:31]
                org_params.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"    ✓ Master: {master_file.name}")
        
        return master_file
    
    def export_all(self):
        """Export all data formats"""
        
        results = self.load_results()
        
        print("Exporting data to Excel and CSV formats...\n")
        
        # Export all formats
        param_df = self.export_parameter_table(results)
        summary_df = self.export_summary_statistics(results)
        comparison_df = self.export_organism_comparison(results)
        error_df = self.export_error_distributions(results)
        
        # Create master workbook
        master_file = self.export_master_workbook(param_df, summary_df, comparison_df, error_df)
        
        print(f"\n{'='*70}")
        print("DATA EXPORT COMPLETE!")
        print(f"{'='*70}")
        print(f"\nGenerated files in: {self.output_folder}")
        print("\nFiles created:")
        print("  ✓ MASTER_Results.xlsx (All data in one workbook)")
        print("  ✓ parameter_estimates.xlsx & .csv")
        print("  ✓ summary_statistics.xlsx & .csv")
        print("  ✓ organism_comparison.xlsx & .csv")
        print("  ✓ error_distributions.csv")
        print("\nAll files are ready for:")
        print("  - Excel analysis and pivot tables")
        print("  - Statistical software (R, Python)")
        print("  - Thesis tables and appendices")
        print("  - Presentation slides")
        print(f"{'='*70}\n")

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) < 2:
        print("\nUsage: py -3 export_data_tables.py <results_folder>")
        print("\nExample: py -3 export_data_tables.py results/Session14")
        results_folder = input("\nEnter results folder path: ").strip()
    else:
        results_folder = sys.argv[1]
    
    if not Path(results_folder).exists():
        print(f"\n✗ Error: Results folder not found: {results_folder}")
        return
    
    exporter = DataExporter(results_folder)
    exporter.export_all()

if __name__ == "__main__":
    main()
