"""
Fixed Standalone Version of my_mcem.py - BUG FIXED!
====================================================

This is a modified version that removes the dependency on the parent package.
Changes:
- Removed `from ...myglobal import proc_global`
- Added multiprocessing setup directly in this file
- Made it work as a standalone module
- FIXED: ks_var initialization bug that caused UnboundLocalError

BUG FIX (2026-01-11):
- Added initialization of ks_var BEFORE the loop
- This prevents UnboundLocalError when optimization doesn't improve
- Now ks_var always has a value even if no improvement found

Original author: Erickson Fajiculay
Modified for standalone use: 2026
Bug fix: 2026-01-11
"""

import sys
import os
import warnings
import numpy as np
import multiprocessing

warnings.filterwarnings('ignore')

# Create a simple global object to replace proc_global
class ProcGlobal:
    """Simple replacement for proc_global module"""
    def __init__(self):
        self.mp = multiprocessing
        self.LST = []  # Shared list for multiprocessing

proc_global = ProcGlobal()


def log_likelihood(ks_var, custom_function, args=None):
    """This function evaluates the loglikelihood based on the definitons
    provided in the custom_function. Here, it is the negative of the sum
    of squared errors between true and estimated value.

    Args:
        ks_var (list): list of parameter values
        custom_function (function): user defined function to evaluate
            error
        args (tuple, optional): tuple of arguments needed by the
            custom_function. Defaults to None.

    Returns:
        float: loglikelihood value
    """
    result = custom_function(ks_var, args)
    loglike = -1.0 * np.sum(result ** 2)
    return loglike


def cost_value(ks_var, custom_function, args=None):
    """This function evaluates the cost function or objective function
    based on the definitions provided in the custom_function. Here, it
    is the sum of squared errors between true and estimated value.

    Args:
        ks_var (list): list of parameter values
        custom_function (function): user defined function to evaluate
            error
        args (tuple, optional): tuple of arguments needed by the
            custom_function. Defaults to None.

    Returns:
        float: sum of squared error
    """
    result = custom_function(ks_var, args)
    value = np.sum(result ** 2)
    return value


def exptn_maxtn(LST, r_rand, maxiter, inner_loop, n_pars, positive_only,
                likelihood, args, thr, show_progress=True, initial_guess=None):
    """The expectation maximization algorithm with progress tracking

    Args:
        LST (list): multiprocessing.Manager().list(). Empty List to store
            data from  each chain
        r_rand (float): Seeding  np.random.uniform(0, 1)  to each chain
        maxiter (int): Max number of iteration. Here, it is the product
            of the parameter  maxiter from run_mcem function  and  chain
            number
        inner_loop (int): number  of samples for each EM step multiplied
            by chain number. This is the product of the parameter  inner
            -loop from run_mcem function and chain number
        n_pars (int): number of parameters to be estimated
        positive_only (bool, optional): If  True, parameters can only be
            positive. Defaults to True.
        likelihood (function, optional): user/program defined  objective
            /error function to optimized
        args (tuple, optional): tuple  of arguments needed by likelihood
            function. Defaults to None.
        thr (float, optional): convergence criteria between iterations.
            Defaults to 1.0e-10.
        show_progress (bool): Show progress bar
        initial_guess (array): Initial parameter guess

    Returns:
        tuple: final parameter values and minimum error/cost function
    """
    
    np.random.seed(int(r_rand * 100))
    
    # Use provided initial guess or default
    if initial_guess is not None:
        mn_lst = np.array(initial_guess, dtype=float)
        # Initialize std as 20% of mean
        sd_lst = np.abs(mn_lst) * 0.2
    else:
        # Fallback to generic initialization
        mn_lst = np.array([3.0] * n_pars)
        sd_lst = np.array([1.5] * n_pars)
    
    # initialize variables
    er_min = 1.0e10
    
    # ====================================================================
    # BUG FIX: Initialize ks_var BEFORE the loop!
    # This prevents UnboundLocalError if optimization never improves
    # ====================================================================
    ks_var = mn_lst.copy()  # Start with initial guess
    
    # initialize storage
    chk_lst = []
    
    iterz = 0
    # begin iteration
    while iterz < maxiter:
        # Progress indicator
        if show_progress and iterz % 5 == 0:
            progress_pct = (iterz / maxiter) * 100
            bar_length = 40
            filled = int(bar_length * iterz / maxiter)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"\r  MCEM Progress: [{bar}] {progress_pct:.0f}% (Iter {iterz}/{maxiter}, SSE: {er_min:.2e})", end='', flush=True)
        
        # stores samples with final optimized likelihood
        xacept = []
        
        smpl_ik = 0
        mnew_lst = []
        sdnew_lst = []
        while smpl_ik < inner_loop:
            # sample new values from log-normal distribution
            if positive_only:
                ksnew_var = np.random.lognormal(
                    mean=np.log(mn_lst / np.sqrt(1 + (sd_lst / mn_lst) ** 2)),
                    sigma=np.sqrt(np.log(1 + (sd_lst / mn_lst) ** 2))
                )
            else:
                ksnew_var = np.random.normal(mn_lst, sd_lst)
            
            # calculate log-likelihood with new parameters
            lknew = log_likelihood(ksnew_var, likelihood, args)
            
            # metropolis acceptance
            if smpl_ik == 0 or np.exp(lknew - lkold) > np.random.uniform(0, 1):
                ksold_var = ksnew_var
                lkold = lknew
            
            #collect accepted parameters
            xacept.append(ksold_var)
            smpl_ik += 1
        
        # expectation step : calculate mean and standard dev of parameters
        xacept = np.array(xacept)
        mn_lst = np.mean(xacept, axis=0)
        sd_lst = np.std(xacept, axis=0)
        
        # keep track of parameters for convergence
        chk_lst.append(mn_lst)
        
        # Check for convergence
        if iterz >= 2:
            diff = np.sum(np.abs(chk_lst[-1] - chk_lst[-2]))
            if diff <= thr:
                if show_progress:
                    print(f"\r  MCEM Progress: [{'█'*bar_length}] 100% - CONVERGED at iteration {iterz}!" + " "*20)
                # Update ks_var with converged value
                ks_var = mn_lst
                break
        
        # calculate minimum error with current mean parameters
        er_cur = cost_value(mn_lst, likelihood, args)
        if er_cur < er_min:
            er_min = er_cur
            ks_var = mn_lst  # Update best parameters
        
        iterz += 1
    
    # Final progress update
    if show_progress:
        print(f"\r  MCEM Progress: [{'█'*bar_length}] 100% - Completed {iterz} iterations!" + " "*20)
        print()  # New line
    
    # Return mean, error, AND standard deviations for confidence intervals
    LST.append([ks_var, er_min, sd_lst])
    return (ks_var, er_min, sd_lst)


def run_mcem(ks_lst, chains=1, maxiter=300, inner_loop=500,
             positive_only=True, likelihood=None, args=None):
    """Run MCEM with multiple chains

    Args:
        ks_lst (list): list of initial parameter values
        chains (int, optional): Number of parallel chains to run for the
            MCEM. Defaults to 1.
        maxiter (int, optional): Number  of iteration steps for the EM.
            Defaults to 300.
        inner_loop (int, optional): Sample size per EM  iteration. 
            Defaults to 500.
        positive_only (bool, optional): If  True, parameters can only be
            positive. Defaults to True.
        likelihood (function, optional): user/program defined objective/
            error function  to  optimized
        args (tuple): Tuple  of  (data,  conc, tvar,  sp_comp,  ks_dict,
            r_dict,  p_dict,  v_stoich,  c_miss,  k_miss, molar, rfile).
            Defaults  to None. See param_estimate module for  the proper
            definition of variables.

    Returns:
        tuple: (best_parameters, minimum_error, standard_deviations)
    """
    n_pars = len(ks_lst)
    xvar = 0.0
    
    if chains == 1:
        # Single chain - no multiprocessing
        np.random.seed(42)
        r_rand = np.random.uniform(0, 1)
        thr = 1.0e-10
        
        result = exptn_maxtn(
            [], r_rand, maxiter, inner_loop, n_pars, 
            positive_only, likelihood, args, thr,
            show_progress=True,
            initial_guess=ks_lst  # PASS THE INITIAL GUESS!
        )
        
        # Return all three: parameters, error, and std devs
        return result
    
    # Note: Multi-chain code below is preserved but not currently used on Windows
    # If needed in future, uncomment and fix multiprocessing for Windows
    
    # else:
    #     # Multiple chains with multiprocessing
    #     # Note: This may not work on Windows due to multiprocessing limitations
    #     # For Windows, use chains=1
    #     
    #     manager = multiprocessing.Manager()
    #     LST = manager.list()
    #     
    #     pool = multiprocessing.Pool(chains)
    #     np.random.seed(42)
    #     rands = [(xvar + 1) * np.random.uniform(0, 1) for xvar in range(chains)]
    # 
    #     thr = 1.0e-10
    #     results = [
    #         pool.apply_async(
    #             exptn_maxtn, args=(LST, rands[ih], maxiter * (ih + 1),
    #                                inner_loop * (ih + 1), n_pars, positive_only,
    #                                likelihood, args, thr)
    #         ) for ih in range(chains)
    #     ]
    # 
    #     ffvar = [result.get() for result in results]
    #     pool.close()
    #     pool.join()
    # 
    #     # Find best result across chains
    #     er_list = [result[1] for result in ffvar]
    #     er_min = min(er_list)
    #     
    #     ks_var = None
    #     for result in ffvar:
    #         if result[1] <= er_min:
    #             ks_var = result[0]
    #     
    #     return (ks_var, er_min)


if __name__ == "__main__":
    print("Fixed standalone version of my_mcem.py")
    print("Bug fix applied: ks_var initialization")
    print("Ready to use!")
