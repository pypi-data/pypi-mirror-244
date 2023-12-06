import numpy as np
import pandas as pd
import plotnine as p9
from itertools import product
from scipy.stats import beta as beta_dist
from scipy.stats import t as t_dist
from . import bayes_factors
from . import exp_families
from scipy.special import betaln

def _remove_nan(y, z):
    '''
    Convenience function to remove observations with missing data.
    '''
    is_nan = np.isnan(y)
    if np.sum(is_nan) > 0:
        y = y[~is_nan].copy()
        z = z[:, ~is_nan].copy()
    return (y, z)

def fit_y_normal(model,
                 y,
                 x_new = None,
                 y_new = None,
                 index = None,
                 profile_labels = None,
                 start_profile_labels_from1 = False,
                 prior_alpha = 1.0,
                 prior_beta = 1.0,
                 prior_m = 0.0,
                 prior_lambda = 1.0,
                 figure_size = [10, 12],
                 font_size = 11,
                 facet_var = 'variable',
                 ncol = 4):
    '''
    Analyze the relationship between dependent variables (y) -
    that are assumed to be normally distributed - and the profiles.
    This is done without changing the model's other variational parameters.
    '''
    ##### SET UP DATA ETC #####
    y_names = pd.Categorical(y.columns.values, categories = y.columns.values, ordered = True)
    if index is None:
        y = y.copy()
    else:
        y = y.iloc[index].copy().transpose()
    n_y = y.shape[1] # number of dependent variables
        
    bayes_factor_df = pd.DataFrame(1.0,
                                   columns = ['bf10', 'frac_bf10'],
                                   index = y_names) # empty dataframe for results
        
    ##### COMPUTE REGULAR, FRACTIONAL, AND POSTERIOR BAYES FACTORS #####
    for j in range(n_y):
        y_j = y[y_names[j]].values
        bayes_factor_df.loc[y_names[j], 'bf10'] = bayes_factors.normal_shared_var(y_j, model.z_hat_1hot, prior_m, prior_lambda, prior_alpha, prior_beta)
        bayes_factor_df.loc[y_names[j], 'frac_bf10'] = bayes_factors.frac_normal_shared_var(y_j, model.z_hat_1hot, prior_m, prior_lambda, prior_alpha, prior_beta)
        bayes_factor_df.loc[y_names[j], 'post_bf10'] = bayes_factors.post_normal_shared_var(y_j, model.z_hat_1hot, prior_m, prior_lambda, prior_alpha, prior_beta)
        
    ##### PAIRWISE COMPARISONS (FRACTIONAL BAYES FACTORS) TO PROFILE 0 #####
    pairwise_log10_frac_bf10 = pd.DataFrame(0.0,
                                            columns = ['profile ' + str(t + start_profile_labels_from1) for t in range(1, model.n_profiles)],
                                            index = y_names)
    for j in range(n_y):
        for t in range(1, model.n_profiles):
            in_profiles = np.isin(model.z_hat, [0, t])
            y_used = y.loc[in_profiles, y_names[j]].values # only include data from people in these profiles
            z_hat_used = model.z_hat_1hot[:, in_profiles][[0, t], :]
            pairwise_log10_frac_bf10.loc[y_names[j], 'profile ' + str(t + start_profile_labels_from1)] = np.log10(bayes_factors.frac_normal_shared_var(y_used, z_hat_used, prior_m, prior_lambda, prior_alpha, prior_beta))
    
    ##### POSTERIOR HYPERPARAMETERS #####
    post_hpar = {'m': np.zeros([n_y, model.n_profiles]), 'lambda': np.zeros([n_y, model.n_profiles]), 'alpha': np.zeros(n_y), 'beta': np.zeros(n_y)}
    v_mu = np.zeros([n_y, model.n_profiles])
    for j in range(n_y):
        (y_j, z_hat_j) = _remove_nan(y[y_names[j]].values, model.z_hat_1hot)
        dist = exp_families.multi_group_normal({'m': prior_m, 'lambda': prior_lambda, 'alpha': prior_alpha, 'beta': prior_beta}, model.n_profiles)
        dist.update(y_j, z_hat_j)
        post_hpar['m'][j,:] = dist.hpar['m']
        post_hpar['lambda'][j,:] = dist.hpar['lambda']
        post_hpar['alpha'][j] = dist.hpar['alpha']
        post_hpar['beta'][j] = dist.hpar['beta']
        v_mu[j, :] = dist.hpar['beta']/(dist.hpar['lambda']*(dist.hpar['alpha'] - 1))
    
    ##### COMPUTE THE COEFFICIENT OF DETERMINATION (R^2) #####
    r2 = pd.Series(0.0, index = y_names)
    for j in range(n_y):
        (y_j, z_hat_j) = _remove_nan(y[y_names[j]].values, model.z_hat_1hot)
        y_hat = np.inner(post_hpar['m'][j, :], z_hat_j.T)
        ss_residuals = np.sum((y_j - y_hat)**2)
        ss_total = np.sum((y_j - np.mean(y_j))**2)
        r2[y_names[j]] = 1 - ss_residuals/ss_total
    
    ##### MAKE PLOT #####
    plot_df = pd.DataFrame(product(range(n_y), range(model.n_profiles)),
                                columns = ['j', 'profile'])
    plot_df['variable'] = y_names[plot_df['j'].values]
    plot_df['mu'] = 0.0
    plot_df['v'] = 0.0
    hard_m_mu = np.zeros([n_y, model.n_profiles])
    hard_v_mu = np.zeros([n_y, model.n_profiles])
    for r in range(plot_df.shape[0]):
        plot_df.loc[r, 'mu'] = post_hpar['m'][plot_df.iloc[r]['j'].astype(int), plot_df.iloc[r]['profile'].astype(int)]
        plot_df.loc[r, 'v'] = v_mu[plot_df.iloc[r]['j'].astype(int), plot_df.iloc[r]['profile'].astype(int)]
    plot_df['mu_minus'] = plot_df['mu'] - 1.96*np.sqrt(plot_df['v'])
    plot_df['mu_plus'] = plot_df['mu'] + 1.96*np.sqrt(plot_df['v'])
    if start_profile_labels_from1:
        plot_df['profile'] += 1
    plot_df['profile'] = plot_df['profile'].astype('string')
    
    if facet_var == 'profile':
        if profile_labels is None:
            plot = p9.ggplot(plot_df, p9.aes(x = 'variable', y = 'mu', ymin = 'mu_minus', ymax = 'mu_plus'))
        else:
            plot = p9.ggplot(plot_df, p9.aes(shape = 'profile label', x = 'variable', y = 'mu', ymin = 'mu_minus', ymax = 'mu_plus'))
    elif facet_var == 'variable' or n_y == 1:
        if profile_labels is None:
            plot = p9.ggplot(plot_df, p9.aes(x = 'profile', y = 'mu', ymin = 'mu_minus', ymax = 'mu_plus'))
        else:
            plot = p9.ggplot(plot_df, p9.aes(shape = 'profile label', x = 'profile', y = 'mu', ymin = 'mu_minus', ymax = 'mu_plus'))

    plot += p9.geom_point()
    plot += p9.geom_errorbar()
    plot += p9.theme_classic(base_size = font_size)
    plot += p9.theme(figure_size = figure_size)
    if not profile_labels is None:
        plot += p9.scale_shape_manual(values = len(profile_labels)*["o"]) # this is just a hack to display the legend (we don't want different shapes) 
        
    if n_y > 1:
        if facet_var == 'profile':
            plot += p9.facet_wrap('profile', scales = 'free_x', ncol = ncol)
        elif facet_var == 'variable':
            plot += p9.facet_wrap('variable', scales = 'free', ncol = ncol)
    
    output = {'plot': plot, 'plot_df': plot_df, 'bayes_factors': bayes_factor_df, 'log10_bayes_factors': np.log10(bayes_factor_df), 'pairwise_log10_frac_bf10': pairwise_log10_frac_bf10, 'r2': r2, 'post_hpar': post_hpar}
    
#    if not y_new is None:
        # TOTALLY REVISE THIS
        ##### GET THE APPROXIMATE LOG POSTERIOR PREDICTIVE (p(y | x)) AND PREDICTED MEAN FOR NEW DATA #####
#        n_new = y_new.shape[0]
#        log_post_pred = pd.DataFrame(0.0, index = y_new.index, columns = y_new.columns)
#        post_pred_mean = pd.DataFrame(0.0, index = y_new.index, columns = y_new.columns)
#        phi_new = model.classify_new_data(x_new) # approximately p(z_new = t | x_new, old data)
#        for j in range(n_y):
#            var = y_new.columns[j]
#            post_pred_by_profile = np.zeros([model.T, n_new])
#            for t in range(model.T):
                # https://en.wikipedia.org/wiki/Conjugate_prior#When_likelihood_function_is_a_continuous_distribution ** DOUBLE CHECK THIS **
#                t_dist_sd = np.sqrt(beta[j]*(lamb[j, t] + 1)/(alpha[j]*lamb[j, t]))
#                post_pred_by_profile[t, :] = t_dist.pdf(y_new.loc[:, var],
#                                                        df = 2*alpha[j],
#                                                        loc = m[j, t],
#                                                        scale = t_dist_sd)
#            log_post_pred.loc[:, var] = np.log(np.sum(post_pred_by_profile*phi_new, axis = 0))
#            post_pred_mean.loc[:, var] = np.inner(m[j, :], phi_new.T)
            
        ##### COMPUTE THE PREDICTIVE COEFFICIENT OF DETERMINATION #####
#        predictive_r2 = pd.Series(0.0, index = y_names)
#        for var in y_names:
#            ss_residuals = np.sum((y_new[var] - post_pred_mean[var])**2)
#            ss_total = np.sum((y_new[var] - y_new[var].mean())**2)
#            predictive_r2[var] = 1 - ss_residuals/ss_total

#        output['predictive_r2'] = predictive_r2 # TOTALLY REVISE THIS
    return output
    
def fit_y_bernoulli(model, 
                    y,
                    index = None,
                    profile_labels = None,
                    start_profile_labels_from1 = False,
                    prior_a = 0.5,
                    prior_b = 0.5,
                    y_names = None, 
                    figure_size = [10, 8], 
                    font_size = 11, 
                    facet_var = 'variable', 
                    ncol = 4):
    '''
    Analyze the relationship between dependent variables (y) -
    that are assumed to be Bernoulli distributed - and the profiles.
    This is done without changing the model's other variational parameters.
    
    Notes
    -----
    We assume y_i | z_i = t ~ Bernoulli(psi_t).
    '''
    ##### SET UP DATA ETC #####
    y_names = pd.Categorical(y.columns.values, categories = y.columns.values, ordered = True)
    if index is None:
        y = y.copy()
    else:
        y = y.iloc[index].copy().transpose()
    n_y = y.shape[1] # number of dependent variables
    bayes_factor_df = pd.DataFrame(1.0,
                                   columns = ['bf10', 'frac_bf10'],
                                   index = y_names) # empty dataframe for results
    
    ##### COMPUTE BAYES FACTORS AND FRACTIONAL BAYES FACTORS #####
    for j in range(n_y):
        y_j = y[y_names[j]].values
        bayes_factor_df.loc[y_names[j], 'bf10'] = bayes_factors.bernoulli(y_j,
                                                                          model.z_hat_1hot,
                                                                          prior_a,
                                                                          prior_b)
        bayes_factor_df.loc[y_names[j], 'frac_bf10'] = bayes_factors.frac_bernoulli(y_j,
                                                                                    model.z_hat_1hot,
                                                                                    prior_a,
                                                                                    prior_b)
        bayes_factor_df.loc[y_names[j], 'post_bf10'] = bayes_factors.post_bernoulli(y_j,
                                                                                    model.z_hat_1hot,
                                                                                    prior_a,
                                                                                    prior_b)
    ##### POSTERIOR HYPERPARAMETERS #####
    post_hpar = dict()
    for j in range(n_y):
        (y_j, z_hat_j) = _remove_nan(y[y_names[j]].values, model.z_hat_1hot)
        dist = exp_families.multi_group_distribution(exp_families.beta_bernoulli, {'a': prior_a, 'b': prior_b}, model.n_profiles)
        dist.update(y_j, z_hat_j)
        post_hpar[y_names[j]] = dist.hpar_table()
        
    ##### PAIRWISE COMPARISONS (FRACTIONAL BAYES FACTORS) TO PROFILE 0 #####
    pairwise_log10_frac_bf10 = pd.DataFrame(0.0,
                                            columns = ['profile ' + str(t + start_profile_labels_from1) for t in range(1, model.n_profiles)],
                                            index = y_names)
    for j in range(n_y):
        for t in range(1, model.n_profiles):
            in_profiles = np.isin(model.z_hat, [0, t])
            y_used = y.loc[in_profiles, y_names[j]].values # only include data from people in these profiles
            z_hat_used = model.z_hat_1hot[:, in_profiles][[0, t], :]
            pairwise_log10_frac_bf10.loc[y_names[j], 'profile ' + str(t + start_profile_labels_from1)] = np.log10(bayes_factors.frac_bernoulli(y_used, z_hat_used, prior_a, prior_b))
    
    
    ##### COMPUTE THE BRIER SKILL SCORE (BSS) #####
    bss = pd.Series(0.0, index = y_names)
    for j in range(n_y):
        E_psi = post_hpar[y_names[j]]['a']/(post_hpar[y_names[j]]['a'] + post_hpar[y_names[j]]['b'])
        (y_j, z_hat_j) = _remove_nan(y[y_names[j]].values, model.z_hat_1hot)
        y_hat = np.inner(E_psi, z_hat_j.T)
        n_j = y_j.shape[0]
        Brier_skill = np.sum((y_j - y_hat)**2)/n_j
        reference_skill = np.sum((y_j - np.mean(y_j))**2)/n_j
        bss[y_names[j]] = 1 - Brier_skill/reference_skill
    
    ##### MAKE PLOT #####
    plot_df = pd.DataFrame(product(y_names, range(model.n_profiles)),
                           columns = ['variable', 'profile'])
    plot_df['E_psi'] = 0.0
    plot_df['lower'] = 0.0
    plot_df['upper'] = 0.0
    for j in range(n_y):
        rows_j = plot_df['variable'] == y_names[j]
        plot_df.loc[rows_j, 'E_psi'] = np.array(post_hpar[y_names[j]]['a']/(post_hpar[y_names[j]]['a'] + post_hpar[y_names[j]]['b']))
        plot_df.loc[rows_j, 'lower'] = beta_dist.ppf(0.05, post_hpar[y_names[j]]['a'], post_hpar[y_names[j]]['b'])
        plot_df.loc[rows_j, 'upper'] = beta_dist.ppf(0.95, post_hpar[y_names[j]]['a'], post_hpar[y_names[j]]['b'])
    if start_profile_labels_from1:
        plot_df['profile'] += 1
    plot_df['profile'] = plot_df['profile'].astype('string')
    if not profile_labels is None:
        plot_df['profile label'] = int(plot_df.shape[0]/len(profile_labels))*profile_labels

    if facet_var == 'profile':
        if profile_labels is None:
            plot = p9.ggplot(plot_df, p9.aes(x = 'variable', y = 'E_psi', ymin = 'lower', ymax = 'upper'))
        else:
            plot = p9.ggplot(plot_df, p9.aes(shape = 'profile label', x = 'variable', y = 'E_psi', ymin = 'lower', ymax = 'upper'))
    elif facet_var == 'variable' or n_y == 1:
        if profile_labels is None:
            plot = p9.ggplot(plot_df, p9.aes(x = 'profile', y = 'E_psi', ymin = 'lower', ymax = 'upper'))
        else:
            plot = p9.ggplot(plot_df, p9.aes(shape = 'profile label', x = 'profile', y = 'E_psi', ymin = 'lower', ymax = 'upper'))

        plot += p9.geom_point()
        plot += p9.geom_errorbar()
        plot += p9.theme_classic(base_size = font_size)
        plot += p9.theme(figure_size = figure_size)
        if not profile_labels is None:
            plot += p9.scale_shape_manual(values = len(profile_labels)*["o"]) # this is just a hack to display the legend (we don't want different shapes)

        if n_y > 1:
            if facet_var == 'profile':
                plot += p9.facet_wrap('profile', scales = 'free_x', ncol = ncol)
            elif facet_var == 'variable':
                plot += p9.facet_wrap('variable', scales = 'free', ncol = ncol)

    return {'plot': plot, 'plot_df': plot_df, 'bayes_factors': bayes_factor_df, 'log10_bayes_factors': np.log10(bayes_factor_df), 'pairwise_log10_frac_bf10': pairwise_log10_frac_bf10, 'Brier_skill_score': bss, 'post_hpar': post_hpar}