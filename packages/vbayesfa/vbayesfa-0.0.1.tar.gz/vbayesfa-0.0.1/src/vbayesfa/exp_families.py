import numpy as np
import pandas as pd
from scipy.special import betaln, gammaln

# These classes are somewhat similar in spirit to this: https://pythonhosted.org/infpy/infpy.exp.html
# I used 1-indexing in the doc, so I'm using pseudo 1-indexing here to avoid mistakes in transcribing the math into Python.

class distribution:
        
    def tau_prime(self, y):
        T = self.T(y)
        n = y.shape[0]
        return [self.tau[j] + np.sum(T[j], axis = -1) for j in range(self.p)] + [self.tau[self.p] + n]
    
    def weighted_tau_prime(self, y, weights):
        '''
        Notes
        -----
        weights represents a weighting factor (should be from 0 to 1) for each 
        observation.
        '''
        T = self.T(y)
        n = np.sum(weights)
        return [self.tau[j] + np.sum(weights*T[j], axis = -1) for j in range(self.p)] + [self.tau[self.p] + n]    
    
    def update(self, y, weights = None):
        '''
        Perform conjugate prior updating.
        '''
        if weights is None:
            self.tau = self.tau_prime(y)
        else:
            self.tau = self.weighted_tau_prime(y, weights)
        self.hpar = self.tau_to_hpar(self.tau)
    
    def log_density(self, theta):
        '''
        Compute the log density of theta.
        '''
        return np.sum([np.sum(self.tau[j]*theta[j]) for j in range(self.p)]) - self.tau[self.p]*self.g(theta) - self.h(self.tau)
        
    def density(self, theta):
        return np.exp(self.log_density(theta))
        
    #def log_predictive(self, y):
    #    '''
    #    Compute the log predictive distribution of data.
    #    '''
        # ADD THIS
        
    #def predictive(self, y):
    #    return np.exp(self.log_predictive(y))
    
    def log_marginal(self, y):
        '''
        Compute the log of the marginal distribution of data.
        '''
        return -np.sum(self.f(y)) - self.h(self.tau) + self.h(self.tau_prime(y))            
        
    def weighted_log_marginal(self, y, weights):
        return -np.sum(weights*self.f(y)) - self.h(self.tau) + self.h(self.weighted_tau_prime(y, weights))
    
    def frac_log_marginal(self, y, frac):
        n = y.shape[0]
        return self.weighted_log_marginal(y = y, weights = frac*np.ones(n))
    
    def marginal(self, y):
        return np.exp(self.log_marginal(y))

class multi_group_distribution:
    '''
    This assumes no shared parameter (e.g. variance/precision) across groups.
    
    z gives 1-hot encoding of each observation's group (row = group, column = observation).
    
    n_t is the number of groups.
    
    I should revise __init__ in the future to allow the groups to have different starting hyperparameters.
    '''
    
    def __init__(self, base_dist, hpar, n_t):
        self.n_t = n_t
        self.dists = []
        for t in range(self.n_t):
            self.dists += [base_dist(hpar)]
        self.tau = [self.dists[t].tau for t in range(self.n_t)]
        self.hpar = [self.dists[t].hpar for t in range(self.n_t)]
        
    def hpar_table(self):
        '''
        Put all of the (conventional) hyperparameters in a table (Pandas data frame).
        '''
        hpar_names = list(self.dists[0].hpar.keys())
        table = pd.DataFrame(0.0, index = range(self.n_t), columns = hpar_names)
        for t in range(self.n_t):
            for hpar_name in hpar_names:
                table.loc[t, hpar_name] = self.dists[t].hpar[hpar_name]
        return table
        
    def update(self, y, z):
        for t in range(self.n_t):
            self.dists[t].update(y, weights = z[t,:])
            self.tau[t] = self.dists[t].tau
            self.hpar[t] = self.dists[t].hpar
            
    def log_density(self, theta):
        return np.sum([self.dists[t].log_density(theta[t]) for t in range(self.n_t)])
    
    def density(self, theta):
        return np.exp(self.log_density(theta))
    
    def log_marginal(self, y, z):
        z_flat = z.argmax(axis = 0) # encodes group in a single vector (not 1-hot encoding)
        return np.sum([self.dists[t].log_marginal(y[z_flat == t]) for t in range(self.n_t)])
    
    def frac_log_marginal(self, y, z, frac):
        return np.sum([self.dists[t].weighted_log_marginal(y, weights = frac[t]*z[t,:]) for t in range(self.n_t)])
    
    def marginal(self, y, z, frac):
        return np.exp(self.log_marginal(y, z, frac))
    
class distribution_with_predictor:
    '''
    
    Notes
    -----
    It is assumed that the last axis in T, z, S(z) etc. represents individual observations, e.g. participants.
    Thus, np.sum(T[j], axis = -1) takes the sum across observations.
    '''
        
    def tau_prime(self, y, z):
        T = self.T(y, z)
        n = y.shape[0]
        return [self.tau[j] + np.sum(T[j], axis = -1) for j in range(self.p)] + [self.tau[self.p] + n, self.tau[self.p + 1] + np.sum(self.S(z), axis = -1)]
    
    def weighted_tau_prime(self, y, z, weights):
        '''
        Notes
        -----
        weights represents a weighting factor (should be from 0 to 1) for each 
        observation.
        '''
        T = self.T(y, z)
        n = np.sum(weights)
        return [self.tau[j] + np.sum(weights*T[j], axis = -1) for j in range(self.p)] + [self.tau[self.p] + n, self.tau[self.p + 1] + np.sum(weights*self.S(z), axis = -1)] 
    
    def update(self, y, z):
        '''
        Perform conjugate prior updating.
        '''
        self.tau = self.tau_prime(y, z)
        self.hpar = self.tau_to_hpar(self.tau)
    
    def log_density(self, theta):
        '''
        Compute the log density of theta.
        '''
        return np.sum([np.sum(self.tau[j]*theta[j]) for j in range(self.p)]) - self.tau[self.p]*self.g(theta) - np.sum(self.tau[self.p + 1]*self.k(theta)) - self.h(self.tau)
        
    def density(self, theta):
        return np.exp(self.log_density(theta))
        
    #def log_predictive(self, y, z):
    #    '''
    #    Compute the log predictive distribution of data.
    #    '''
        # ADD THIS
        
    #def predictive(self, y, z):
    #    return np.exp(self.log_predictive(y, z))
    
    def log_marginal(self, y, z):
        '''
        Compute the log of the marginal distribution of data.
        '''
        return -np.sum(self.f(y)) - self.h(self.tau) + self.h(self.tau_prime(y, z))
    
    def weighted_log_marginal(self, y, z, weights):
        return -np.sum(weights*self.f(y)) - self.h(self.tau) + self.h(self.weighted_tau_prime(y, z, weights))
    
    def marginal(self, y, z):
        return np.exp(self.log_marginal(y, z))   
    
class beta_bernoulli(distribution):
    
    def __init__(self, hpar = {'a': 1.0, 'b': 1.0}):
        '''
        Initialize the beta distribution over theta (log-odds) with given parameters.
        '''
        self.hpar = hpar # conventional hyperparameters
        self.tau = self.hpar_to_tau(self.hpar)
        self.p = 1 # number of likelihood parameters
    
    def hpar_to_tau(self, hpar):
        '''
        Convert conventional hyperparameters to natural ones (tau).
        '''
        return [hpar['a'] - 1, hpar['a'] + hpar['b'] - 2]
    
    def tau_to_hpar(self, tau):
        '''
        Convert natural hyperparameters (tau) to conventional ones.
        '''
        return {'a': tau[1-1] + 1, 'b': tau[2-1] - tau[1-1] + 1}
    
    def T(self, y):
        '''
        Compute sufficient statistics.
        '''
        return [y]
        
    def f(self, y):
        return 0.0*y
        
    def g(self, theta):
        return np.log(1 + np.exp(theta))
        
    def h(self, tau):
        hpar = self.tau_to_hpar(tau)
        return betaln(hpar['a'], hpar['b'])

class normal_known_precision(distribution):
    '''
    Normal likelihood with known precision (xi) and a normal
    prior on the mean (mu).
    
    DOUBLE CHECK THIS (SOMETHING SEEMS TO BE WRONG).
    '''
    def __init__(self, hpar = {'m_mu': 0.0, 'xi_mu': 1.0}, xi = 1.0):
        self.xi = xi
        self.sigma = 1/np.sqrt(self.xi)
        self.hpar = hpar
        self.tau = self.hpar_to_tau(self.hpar)
        self.p = 1
        
    def hpar_to_tau(self, hpar):
        '''
        Convert conventional hyperparameters to natural ones (tau).
        '''
        return [self.hpar['m_mu']*self.sigma*self.hpar['xi_mu'], self.hpar['xi_mu']/self.xi]
    
    def tau_to_hpar(self, tau):
        '''
        Convert natural hyperparameters (tau) to conventional ones.
        '''
        return {'m_mu': self.sigma*self.tau[1-1]/self.tau[2-1], 'xi_mu': self.xi*self.tau[2-1]}
    
    def par_to_theta(self, par):
        '''
        Convert conventional parameters to natural ones (theta).
        '''
        return np.array(par['mu']/self.sigma)
    
    def T(self, y):
        return [y/self.sigma]
    
    def f(self, y):
        return 0.5*(self.xi*y**2 + np.log(2*np.pi) - np.log(self.xi))
    
    def g(self, theta):
        return 0.5*theta**2
        
    def h(self, tau):
        hpar = self.tau_to_hpar(tau)
        return 0.5*(np.log(2*np.pi) + hpar['xi_mu']*hpar['m_mu']**2 - np.log(hpar['xi_mu']) + np.log(self.xi))
    
class normal_gamma_normal(distribution):
    
    def __init__(self, hpar = {'m': 0.0, 'lambda': 1.0, 'alpha': 1.0, 'beta': 1.0}):
        self.hpar = hpar
        self.tau = self.hpar_to_tau(self.hpar)
        self.p = 2
    
    def hpar_to_tau(self, hpar):
        '''
        Convert conventional hyperparameters to natural ones (tau).
        '''
        return [hpar['lambda']*hpar['m'],
                -hpar['beta'] - 0.5*hpar['lambda']*hpar['m']**2,
                2*hpar['alpha'] - 1]
    
    def tau_to_hpar(self, tau):
        '''
        Convert natural hyperparameters (tau) to conventional ones.
        '''
        return {'m': tau[1-1]/tau[3-1],
                'lambda': tau[3-1],
                'alpha': 0.5*(tau[3-1] + 1),
                'beta': -0.5*tau[1-1]**2/tau[3-1] - tau[2-1]}
    
    def par_to_theta(self, par):
        '''
        Convert conventional parameters to natural ones (theta).
        '''
        return np.array([par['mu']/par['sigma']**2, 1/par['sigma']**2])
    
    def T(self, y):
        return [y, -0.5*y**2]      
        
    def f(self, y):
        n = y.shape[0]
        return np.array(n*[0.5*np.log(2*np.pi)])
        
    def g(self, theta):
        return 0.5*(theta[1-1]**2/theta[2-1] - np.log(theta[2-1]))
        
    def h(self, tau):
        hpar = self.tau_to_hpar(tau)
        return 0.5*np.log(2*np.pi) + gammaln(hpar['alpha']) - hpar['alpha']*np.log(hpar['beta']) - 0.5*np.log(hpar['lambda'])
    
class multi_group_normal(distribution_with_predictor):
    '''
    Notes
    -----
    z is an n_t x n array indicating group membership.
    z[t, i] = 1 if observation i is in group t and = 0 otherwise.
    
    theta = [xi*mu, xi]
    mu = the vector of the means for y in each group
    xi = the precision of y (shared across groups)
    '''
    
    def __init__(self, hpar = {'m': 0.0, 'lambda': 1.0, 'alpha': 1.0, 'beta': 1.0}, n_t = 2):
        '''
        Parameters
        ----------
        hpar: dict
            Initial (conventional) hyperparameters.
        n_t: int
            Number of groups.
        '''
        self.n_t = n_t
        self.hpar = {'m': hpar['m']*np.ones(n_t), 
                     'lambda': hpar['lambda']*np.ones(n_t), 
                     'alpha': hpar['alpha'], 
                     'beta': hpar['alpha']}
        self.tau = self.hpar_to_tau(self.hpar)
        self.p = 2
    
    def hpar_to_tau(self, hpar):
        '''
        Convert conventional hyperparameters to natural ones (tau).
        '''
        return [hpar['lambda']*hpar['m'], 
                -hpar['beta'] - 0.5*np.sum(hpar['lambda']*hpar['m']**2),
                2*hpar['alpha'] + self.n_t - 2,
                0.5*hpar['lambda']]
    
    def tau_to_hpar(self, tau):
        return {'m': 0.5*tau[1-1]/tau[4-1],
                'lambda': 2*tau[4-1],
                'alpha': 0.5*(tau[3-1] - self.n_t) + 1,
                'beta': -tau[2-1] - 0.25*np.sum(tau[1-1]**2/tau[4-1])}
    
    def T(self, y, z):
        return [z*y, -0.5*y**2]
    
    def S(self, z):
        return 0.5*z
    
    def f(self, y):
        n = y.shape[0]
        return np.array(n*[0.5*np.log(2*np.pi)])
        
    def g(self, theta):
        return -0.5*np.log(theta[2-1])
        
    def k(self, theta):
        return theta[1-1]**2/theta[2-1]
        
    def h(self, tau):
        hpar = self.tau_to_hpar(tau)
        return 0.5*self.n_t*np.log(2*np.pi) + gammaln(hpar['alpha']) - hpar['alpha']*np.log(hpar['beta']) - 0.5*np.sum(np.log(hpar['lambda']))
        
    