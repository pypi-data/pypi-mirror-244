import numpy as np
from . import exp_families

def normal_shared_var(y, z, prior_m = 0.0, prior_lambda = 1.0, prior_alpha = 1.0, prior_beta = 1.0):
    (y, z) = _remove_nan(y, z)
    n_t = z.shape[0] # number of groups
    hpar = {'m': prior_m, 'lambda': prior_lambda, 'alpha': prior_alpha, 'beta': prior_beta} # prior hyperparameters
    H1 = exp_families.multi_group_normal(hpar, n_t)
    H0 = exp_families.normal_gamma_normal(hpar)
    log_bf10 = H1.log_marginal(y, z) - H0.log_marginal(y)
    return np.exp(log_bf10)

def post_normal_shared_var(y, z, prior_m = 0.0, prior_lambda = 1.0, prior_alpha = 1.0, prior_beta = 1.0):
    (y, z) = _remove_nan(y, z)
    n_t = z.shape[0] # number of groups
    hpar = {'m': prior_m, 'lambda': prior_lambda, 'alpha': prior_alpha, 'beta': prior_beta} # prior hyperparameters
    H1 = exp_families.multi_group_normal(hpar, n_t)
    H0 = exp_families.normal_gamma_normal(hpar)
    H1.update(y, z)
    H0.update(y)
    log_bf10 = H1.log_marginal(y, z) - H0.log_marginal(y)
    return np.exp(log_bf10)

def frac_normal_shared_var(y, z, prior_m = 0.0, prior_lambda = 1.0, prior_alpha = 1.0, prior_beta = 1.0):
    (y, z) = _remove_nan(y, z)    
    n_per_group = z.sum(axis = -1)
    z_flat = z.argmax(axis = 0) # encodes group in a single vector (not 1-hot encoding)
    frac = 1/np.sqrt(n_per_group) # different training fractions for each group
    n_t = z.shape[0] # number of groups
    hpar = {'m': prior_m, 'lambda': prior_lambda, 'alpha': prior_alpha, 'beta': prior_beta} # prior hyperparameters
    H1 = exp_families.multi_group_normal(hpar, n_t)
    H0 = exp_families.normal_gamma_normal(hpar)
    log_bf10 = (H1.log_marginal(y, z) - H1.weighted_log_marginal(y, z, weights = frac[z_flat])) - (H0.log_marginal(y) - H0.weighted_log_marginal(y, weights = frac[z_flat]))
    return np.exp(log_bf10)

def normal_dif_var(y, z, prior_m = 0.0, prior_lambda = 1.0, prior_alpha = 1.0, prior_beta = 1.0):
    (y, z) = _remove_nan(y, z)
    n_t = z.shape[0] # number of groups
    hpar = {'m': prior_m, 'lambda': prior_lambda, 'alpha': prior_alpha, 'beta': prior_beta} # prior hyperparameters
    H1 = exp_families.multi_group_distribution(exp_families.normal_gamma_normal, hpar, n_t)
    H0 = exp_families.normal_gamma_normal(hpar)
    log_bf10 = H1.log_marginal(y, z) - H0.log_marginal(y)
    return np.exp(log_bf10)

def frac_normal_dif_var(y, z, prior_m = 0.0, prior_lambda = 1.0, prior_alpha = 1.0, prior_beta = 1.0):
    (y, z) = _remove_nan(y, z)
    n_per_group = z.sum(axis = -1)
    z_flat = z.argmax(axis = 0) # encodes group in a single vector (not 1-hot encoding)
    frac = 1/np.sqrt(n_per_group) # different training fractions for each group
    n_t = z.shape[0] # number of groups
    hpar = {'m': prior_m, 'lambda': prior_lambda, 'alpha': prior_alpha, 'beta': prior_beta} # prior hyperparameters
    H1 = exp_families.multi_group_distribution(exp_families.normal_gamma_normal, hpar, n_t)
    H0 = exp_families.normal_gamma_normal(hpar)
    log_bf10 = (H1.log_marginal(y, z) - H1.frac_log_marginal(y, z, frac = frac)) - (H0.log_marginal(y) - H0.weighted_log_marginal(y, weights = frac[z_flat]))
    return np.exp(log_bf10)

def bernoulli(y, z, prior_a = 0.5, prior_b = 0.5):
    (y, z) = _remove_nan(y, z)
    n_t = z.shape[0] # number of groups
    H1 = exp_families.multi_group_distribution(exp_families.beta_bernoulli, 
                                               {'a': prior_a, 'b': prior_b}, 
                                               n_t)
    H0 = exp_families.beta_bernoulli({'a': prior_a, 'b': prior_b})
    log_bf10 = H1.log_marginal(y, z) - H0.log_marginal(y)
    return np.exp(log_bf10)

def post_bernoulli(y, z, prior_a = 0.5, prior_b = 0.5):
    (y, z) = _remove_nan(y, z)
    n_t = z.shape[0] # number of groups
    H1 = exp_families.multi_group_distribution(exp_families.beta_bernoulli, 
                                               {'a': prior_a, 'b': prior_b}, 
                                               n_t)
    H0 = exp_families.beta_bernoulli({'a': prior_a, 'b': prior_b})
    H1.update(y, z)
    H0.update(y)
    log_bf10 = H1.log_marginal(y, z) - H0.log_marginal(y)
    return np.exp(log_bf10)

def frac_bernoulli(y, z, prior_a = 0.5, prior_b = 0.5):
    (y, z) = _remove_nan(y, z)
    n_per_group = z.sum(axis = -1)
    z_flat = z.argmax(axis = 0) # encodes group in a single vector (not 1-hot encoding)
    frac = 1/np.sqrt(n_per_group) # different training fractions for each group
    n_t = z.shape[0] # number of groups
    H1 = exp_families.multi_group_distribution(exp_families.beta_bernoulli, 
                                               {'a': prior_a, 'b': prior_b}, 
                                               n_t)
    H0 = exp_families.beta_bernoulli({'a': prior_a, 'b': prior_b})
    log_bf10 = (H1.log_marginal(y, z) - H1.frac_log_marginal(y, z, frac = frac)) - (H0.log_marginal(y) - H0.weighted_log_marginal(y, weights = frac[z_flat]))
    return np.exp(log_bf10)

def _remove_nan(y, z):
    '''
    Convenience function to remove observations with missing data.
    '''
    is_nan = np.isnan(y)
    if np.sum(is_nan) > 0:
        y = y[~is_nan].copy()
        z = z[:, ~is_nan].copy()
    return (y, z)