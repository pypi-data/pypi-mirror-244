import numpy as np
import pandas as pd
import plotnine as p9
from copy import copy
from itertools import combinations, product
from scipy.stats import norm as norm_dist
from scipy.stats import beta as beta_dist
from scipy.stats import multinomial as multinomial_dist
from scipy.stats import gamma as gamma_dist
from scipy.stats import t as t_dist
from scipy.special import digamma, loggamma

def lin_reg(x, y, x_test = None, y_test = None, prior_pseudo_obs = 10):
    """
    Bayesian linear regression with a conjugate prior.
    
    Notes
    -----
    
    The regression weights (w) and precisions (xi) have a multi-mean normal-gamma prior with the following hyperparameters:
        m_w = 0
        Lambda_w = (prior_pseudo_obs/T)*I ***** CHECK *****
        alpha_xi = prior_pseudo_obs/2
        beta_xi = prior_pseudo_obs/2
        
        The fact that the prior alpha_xi = prior beta_xi implies that the prior distribution on xi
        has a mean of 1.
    """
    ##### FINISH #####