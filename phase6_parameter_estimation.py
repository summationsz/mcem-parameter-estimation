"""
PHASE 6 PARAMETER ESTIMATION - FLEXIBLE DATA LOADING
====================================================
Detects data file structure automatically!
"""
import numpy as np
from scipy.integrate import solve_ivp
import time
from pathlib import Path

from glycolysis_model import GlycolysisModel
from tca_model import TCAModel
from my_mcem_fixed import run_mcem

def get_parameters_to_estimate(pathway='glycolysis'):
    """Get list of parameters to estimate"""
    
    if pathway == 'glycolysis':
        params = [
            'HXK_Vmax', 'HXK_Km_glucose',
            'PGI_Vmax', 'PGI_Km_G6P',
            'PFK_Vmax', 'PFK_Km_F6P',
            'ALD_Vmax', 'ALD_Km_F16BP',
            'TPI_Vmax', 'TPI_Km_DHAP',
            'GAPDH_Vmax', 'GAPDH_Km_GAP', 'GAPDH_Km_NAD',
            'PGK_Vmax', 'PGK_Km_13BPG',
            'GPM_Vmax', 'GPM_Km_3PG',
            'ENO_Vmax', 'ENO_Km_2PG',
            'PYK_Vmax', 'PYK_Km_PEP',
            'PDC_Km_pyruvate'
        ]
    else:  # tca
        params = [
            'CS_Vmax', 'CS_Km_AcCoA',
            'ACO_Vmax', 'ACO_Km_citrate',
            'ICDH_Vmax', 'ICDH_Km_isocitrate',
            'KGDH_Vmax', 'KGDH_Km_aKG',
            'SCS_Vmax', 'SCS_Km_SucCoA',
            'SDH_Vmax', 'SDH_Km_succinate',
            'FH_Vmax', 'FH_Km_fumarate',
            'MDH_Vmax', 'MDH_Km_malate'
        ]
    
    return params

def load_data_flexible(data_file):
    """Load data file - detects structure automatically"""
    
    data = np.load(data_file, allow_pickle=True)
    
    print(f"  Data file keys: {list(data.files)}")
    
    # Try to get time data
    if 't_observed' in data.files:
        t_obs = data['t_observed']
    elif 't' in data.files:
        t_obs = data['t']
    else:
        raise KeyError("Could not find time data (tried: 't_observed', 't')")
    
    # Try to get concentration data
    if 'y_observed' in data.files:
        y_obs = data['y_observed']
    elif 'y' in data.files:
        y_obs = data['y']
    else:
        raise KeyError("Could not find concentration data (tried: 'y_observed', 'y')")
    
    # Try to get observable indices
    if 'observable_idx' in data.files:
        obs_idx = data['observable_idx']
    else:
        # If no observable_idx, assume all metabolites are observable
        obs_idx = np.arange(y_obs.shape[0])
        print(f"  Note: No observable_idx found, using all {len(obs_idx)} metabolites")
    
    # Try to get true parameters
    if 'true_params' in data.files:
        true_params = data['true_params'].item()
        has_true_params = True
    else:
        true_params = None
        has_true_params = False
        print(f"  Note: No true_params found, will use default parameters")
    
    return t_obs, y_obs, obs_idx, true_params, has_true_params

def estimate_pathway(pathway, organism_folder, settings, mode_name):
    """Estimate parameters for one pathway"""
    
    org_folder = Path(organism_folder)
    
    # Find data file
    if pathway == 'glycolysis':
        data_files = list(org_folder.glob('experimental_data_glycolysis.npz'))
        if not data_files:
            data_files = list(org_folder.glob('experimental_data.npz'))
    else:  # tca
        data_files = list(org_folder.glob('experimental_data_tca.npz'))
    
    if not data_files:
        print(f"\n❌ Data file not found for {pathway}")
        return None
    
    data_file = data_files[0]
    print(f"✓ Loading: {data_file.name}")
    
    # Load data flexibly
    t_obs, y_obs, obs_idx, true_params, has_true_params = load_data_flexible(data_file)
    
    # Get parameters to estimate
    params_to_est = get_parameters_to_estimate(pathway)
    
    print(f"✓ Loaded {len(t_obs)} time points, {y_obs.shape[0]} metabolites")
    print(f"✓ Estimating {len(params_to_est)} parameters")
    
    # Get initial guesses
    if has_true_params:
        # Phase 5 style: perturb true values
        np.random.seed(42 if pathway == 'glycolysis' else 43)
        initial_guess = np.array([true_params[p] for p in params_to_est])
        initial_guess = initial_guess * (1 + 0.25 * (np.random.rand(len(params_to_est)) - 0.5))
        fixed_params = {k: v for k, v in true_params.items() if k not in params_to_est}
    else:
        # Use default from kinetic_parameters
        from kinetic_parameters import GLYCOLYSIS_PARAMS, TCA_PARAMS
        param_source = GLYCOLYSIS_PARAMS if pathway == 'glycolysis' else TCA_PARAMS
        
        # Filter to available params
        available_params = [p for p in params_to_est if p in param_source]
        params_to_est = available_params
        
        # Perturb defaults
        np.random.seed(42 if pathway == 'glycolysis' else 43)
        initial_guess = np.array([param_source[p] for p in params_to_est])
        initial_guess = initial_guess * (1 + 0.25 * (np.random.rand(len(params_to_est)) - 0.5))
        fixed_params = param_source.copy()
    
    # Likelihood function
    def likelihood(param_values, args):
        data, time_points, obs_idx, fix_params, p_names = args
        
        full_params = fix_params.copy()
        for i, pname in enumerate(p_names):
            full_params[pname] = param_values[i]
        
        try:
            if pathway == 'glycolysis':
                model = GlycolysisModel(full_params)
            else:
                model = TCAModel(full_params)
            
            y0 = model.get_initial_state()
            
            sol = solve_ivp(
                model.ode_system,
                t_span=[0, time_points[-1]],
                y0=y0,
                t_eval=time_points,
                method='LSODA',
                rtol=1e-6,
                atol=1e-8
            )
            
            if not sol.success:
                return np.ones(data.size) * 1e10
            
            y_model = sol.y[obs_idx, :]
            residuals = (y_model - data).flatten()
            
            return residuals
        except Exception as e:
            return np.ones(data.size) * 1e10
    
    args = (y_obs, t_obs, obs_idx, fixed_params, params_to_est)
    
    # Run MCEM
    print(f"\n🚀 Running MCEM ({mode_name})...")
    print(f"   Iterations: {settings['maxiter']}, Samples: {settings['inner']}")
    
    start_time = time.time()
    
    ks_est, er_min, std_est = run_mcem(
        ks_lst=initial_guess.tolist(),
        chains=1,
        maxiter=settings['maxiter'],
        inner_loop=settings['inner'],
        positive_only=True,
        likelihood=likelihood,
        args=args
    )
    
    runtime = time.time() - start_time
    
    # Calculate results
    estimated = np.array(ks_est)
    std_devs = np.array(std_est)
    
    # Calculate errors if we have true values
    if has_true_params:
        true_values = np.array([true_params[p] for p in params_to_est])
        errors = np.abs((estimated - true_values) / true_values) * 100
    else:
        # Without true values, calculate convergence metric
        true_values = initial_guess  # Just for storage
        errors = np.abs((estimated - initial_guess) / initial_guess) * 100
    
    print(f"\n{'='*60}")
    print(f"{pathway.upper()} RESULTS")
    print(f"{'='*60}")
    if has_true_params:
        print(f"Average Error: {np.mean(errors):.2f}%")
    else:
        print(f"Average Change from Initial: {np.mean(errors):.2f}%")
    print(f"Runtime: {runtime/60:.1f} minutes ({runtime/3600:.2f} hours)")
    print(f"{'='*60}")
    
    return {
        'pathway': pathway,
        'parameters': params_to_est,
        'initial_guess': initial_guess.tolist(),
        'estimated': estimated.tolist(),
        'errors': errors.tolist(),
        'std_devs': std_devs.tolist(),
        'runtime': runtime,
        'has_true_params': has_true_params
    }

def estimate_organism(organism_name, organism_folder, settings, mode):
    """Estimate parameters for one organism"""
    
    print(f"\n{'='*80}")
    print(f"PROCESSING: {organism_name.upper()}")
    print(f"{'='*80}")
    print(f"Mode: {mode}")
    print(f"Iterations: {settings['maxiter']}, Samples: {settings['inner']}")
    print("-"*80)
    
    org_folder = Path(organism_folder)
    
    # Check what data files exist
    has_glycolysis = len(list(org_folder.glob('experimental_data*.npz'))) > 0
    has_tca = len(list(org_folder.glob('experimental_data_tca.npz'))) > 0
    
    if not has_glycolysis:
        raise FileNotFoundError(f"No experimental data found in {org_folder}")
    
    all_results = []
    
    # Estimate glycolysis
    if has_glycolysis:
        print("\n" + "-"*80)
        print("GLYCOLYSIS PATHWAY")
        print("-"*80)
        
        result = estimate_pathway('glycolysis', organism_folder, settings, mode)
        if result:
            all_results.append(result)
    
    # Estimate TCA if data exists
    if has_tca:
        print("\n" + "-"*80)
        print("TCA CYCLE PATHWAY")
        print("-"*80)
        
        result = estimate_pathway('tca', organism_folder, settings, mode)
        if result:
            all_results.append(result)
    
    # Overall summary
    if all_results:
        total_params = sum(len(r['parameters']) for r in all_results)
        all_errors = []
        for r in all_results:
            all_errors.extend(r['errors'])
        total_runtime = sum(r['runtime'] for r in all_results)
        
        print(f"\n{'='*80}")
        print(f"ORGANISM SUMMARY: {organism_name}")
        print(f"{'='*80}")
        print(f"Total parameters estimated: {total_params}")
        print(f"Overall average error: {np.mean(all_errors):.2f}%")
        print(f"Total runtime: {total_runtime/60:.1f} minutes ({total_runtime/3600:.2f} hours)")
        print(f"{'='*80}")
        
        # Save to organism folder
        org_results = org_folder / 'results'
        org_results.mkdir(exist_ok=True)
        np.savez(org_results / 'estimation.npz',
                results=all_results,
                organism=organism_name,
                total_params=total_params,
                total_runtime=total_runtime)
        
        return np.mean(all_errors), total_runtime, {
            'organism': organism_name,
            'total_params': total_params,
            'pathway_results': all_results,
            'overall_error': np.mean(all_errors),
            'total_runtime': total_runtime,
            'mode': mode
        }
    
    return None, 0, None

def run_parameter_estimation(organisms, mode_name, settings, session_folder):
    """Main parameter estimation function"""
    
    print("\n" + "="*80)
    print("PARAMETER ESTIMATION")
    print("="*80)
    
    # Map organism codes to folders and names
    org_map = {
        'ecoli': ('Bio-Database/BACTERIA/Escherichia_coli', 'E. coli'),
        'bsubtilis': ('Bio-Database/BACTERIA/Bacillus_subtilis', 'B. subtilis'),
        'arabidopsis': ('Bio-Database/PLANTS/Arabidopsis_thaliana', 'Arabidopsis'),
        'yeast': ('Bio-Database/FUNGI/Saccharomyces_cerevisiae', 'S. cerevisiae')
    }
    
    all_results = []
    
    for organism in organisms:
        folder, name = org_map[organism]
        err, rt, res_dict = estimate_organism(name, folder, settings, mode_name)
        
        if res_dict:
            all_results.append(res_dict)
    
    # Save combined results
    session_folder.mkdir(parents=True, exist_ok=True)
    
    if all_results:
        np.savez(session_folder / 'parameter_estimation.npz', results=all_results)
    
    # Print final summary
    print("\n" + "="*80)
    print("PARAMETER ESTIMATION COMPLETE!")
    print("="*80)
    
    if all_results:
        print(f"\nTotal runtime: {sum(r['total_runtime'] for r in all_results)/3600:.2f} hours\n")
        print("Results:")
        print("-"*80)
        print(f"{'Organism':<20} {'Params':<8} {'Error':<8} {'Time'}")
        print("-"*80)
        for r in all_results:
            print(f"{r['organism']:<20} {r['total_params']:<8} "
                  f"{r['overall_error']:6.2f}%  {r['total_runtime']/60:6.1f} min")
        print("="*80)
    
    print(f"\nResults saved: {session_folder}")
    print("="*80)
