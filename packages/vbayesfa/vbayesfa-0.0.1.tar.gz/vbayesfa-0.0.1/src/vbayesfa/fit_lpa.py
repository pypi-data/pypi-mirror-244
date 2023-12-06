import numpy as np
import functools
import multiprocessing
from itertools import product
from .lpa import lpa_model
from scipy.special import digamma

def fit_lpa(x, starting_hpar = None, n_workers = 4, restarts = 4, T = 20, prior_w1 = 3.0, prior_w2 = 1.0, prior_lambda_mu = 0.5, prior_strength_for_xi = 10.0, seed = 1234, tolerance = 1e-05, max_iter = 50, min_iter = 30):
    """
    Parameters
    ----------
    x: data frame or array
        Observed data (data frame or matrix).  If a matrix then rows are variables and columns
        are observations; if a data frame then rows are observations and columns are variables.
    starting_hpar: tuple, optional
        If None (default) then the initial hyperparameters will be sampled as normal.
        If specified, then it should be in as a dict with keys (phi, w1, w2, gamma1, gamma2).
    n_workers: int, optional
        Number of workers in the pool for parallel processing; should be less than
        or equal to the number of available CPUs.
    restarts: int, optional
        Number of random restarts per set of alpha and omega values.
    T: integer, optional
        Truncation level of the variational approximation.
    prior_w1: float, optional
        First prior hyperparameter on alpha.
    prior_w2: float, optional
        Second prior hyperparameter on alpha.
    prior_lambda_mu: float, optional
        Controls the width of the prior distribution on mu: 
        higher values -> tighter prior around 0.
    prior_strength_for_xi: float, optional
        Controls the strength of the gamma prior distribution on xi.
        This prior is assumed to have a mean of 1, with alpha = prior_strength_for_xi/2
        and beta = prior_strength_for_xi/2.
    seed: int, optional
        Random seed (determines starting conditions of each optimization).
    tolerance: float, optional
        Relative change in the ELBO at which the optimization should stop.
    max_iter: integer, optional
        Maximum number of iterations to run the optimization.
    min_iter: integer, optional
        Minimum number of iterations to run the optimization.
        
    Notes
    -----
    ***** ADD THESE *****
    """
    model_list = []
    final_elbo = []
    
    with multiprocessing.Pool(n_workers) as pool:
        fun = functools.partial(__model_fit_wrapper__, x = x, starting_hpar = starting_hpar, T = T, prior_w1 = prior_w1, prior_w2 = prior_w2, prior_lambda_mu = prior_lambda_mu, prior_strength_for_xi = prior_strength_for_xi, tolerance = tolerance, max_iter = max_iter, min_iter = min_iter)
        
        # generate random seeds for each model based on the seed parameter
        seed_list = []
        rng = np.random.default_rng(seed)
        for i in range(restarts):
            seed_list += [rng.integers(low = 1000, high = 9999)]
        
        results = pool.map(fun, seed_list)
        for result in results:
            model_list += [result]
            final_elbo += [result.elbo_list[-1]]
        
    final_elbo = np.array(final_elbo)
        
    return {'final_elbo': final_elbo, 'model_list': model_list, 'best_model': model_list[final_elbo.argmax()]}

def __model_fit_wrapper__(seed, x, starting_hpar, T, prior_w1, prior_w2, prior_lambda_mu, prior_strength_for_xi, tolerance, max_iter, min_iter):
    """
    Defines an LPA model and fits it to the data, returning the result.
    This function is only defined in order to get the parallelization to work.
    """
    new_model = lpa_model(x = x, T = T, prior_w1 = prior_w1, prior_w2 = prior_w2, prior_lambda_mu = prior_lambda_mu, prior_strength_for_xi = prior_strength_for_xi, seed = seed)
    if not starting_hpar is None:
        new_model.phi = starting_hpar['phi']
        new_model.w1 = starting_hpar['w1']
        new_model.w2 = starting_hpar['w2']
        new_model.E_alpha = new_model.w1/new_model.w2
        new_model.E_log_alpha = digamma(new_model.w1) - np.log(new_model.w2)
        new_model.gamma1 = starting_hpar['gamma1']
        new_model.gamma2 = starting_hpar['gamma2']
        for t in range(new_model.T):
            new_model.E_log_V[t] = digamma(new_model.gamma1[t]) - digamma(new_model.gamma1[t] + new_model.gamma2[t])
            new_model.E_log_1minusV[t] = digamma(new_model.gamma2[t]) - digamma(new_model.gamma1[t] + new_model.gamma2[t])
        for j in range(new_model.m):
            for t in range(new_model.T):
                new_model.tau1[j,t] = new_model.prior_tau1 + np.sum(new_model.mask[j,:]*new_model.phi[t,:]*new_model.x[j,:])
                new_model.tau4[j,t] = new_model.prior_tau4 + 0.5*np.sum(new_model.mask[j,:]*new_model.phi[t,:])
        new_model.update_conventional_hyperparameters()
        new_model.update_expectations_etc()
    new_model.fit(tolerance = tolerance, max_iter = max_iter, min_iter = min_iter)
    return new_model