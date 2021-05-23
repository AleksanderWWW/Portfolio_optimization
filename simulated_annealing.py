# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 19:48:31 2021

@author: Aleksander
"""
import numpy as np


class AnnealingEngine:
    
    def __init__(self, func, cov_matrix, ind_er,  temp_0=100, d=0.1, alpha=0.9, max_iter=1000):
        self.func = func
        self.temp = temp_0
        self.n = len(ind_er)
        self.current_x = np.random.uniform(size=self.n)
        self.current_x = np.abs(self.current_x/np.sum(self.current_x))
        self.d = d
        self.alpha = alpha
        self.max_iter = max_iter
        self.k = 0
        self.optimized = False
        self.cov_matrix = cov_matrix
        self.ind_er = ind_er

    def validate_input(self):
        assert (type(self.temp) == float or type(self.temp) == int)
        assert (type(self.d) == float or type(self.d) == int)
        assert (type(self.alpha) == float or type(self.alpha) == int)
        assert (type(self.max_iter) == int and self.max_iter >= 0)
        
    def draw_candidate(self):
        candidate = self.current_x + np.random.uniform(low=-self.d, high=self.d, size=self.n)
        candidate = np.abs(candidate)  # absolute value
        return candidate/np.sum(candidate)  # weight scaling
    
    def prob_transition(self, candidate):
        """Probabilistic transition allows the algorithm to escape from local
        minima and explore the design space further"""
        A_k = min(1, np.e**(-1*(self.func(candidate, self.cov_matrix, self.ind_er) -
                                self.func(self.current_x, self.cov_matrix, self.ind_er)) / self.temp))

        if np.random.uniform(low=0, high=1) < A_k:
            # transition to a worse solution
            self.current_x = candidate
                
    def activate(self, candidate):
        if self.func(candidate, self.cov_matrix, self.ind_er) <= self.func(self.current_x, self.cov_matrix, self.ind_er):
            self.current_x = candidate
        else:
            self.prob_transition(candidate)          
                
    def cool_down(self):
        self.temp *= self.alpha
        
    def optimize(self):
        while self.k < self.max_iter:
            candidate = self.draw_candidate()
            self.activate(candidate)
            self.cool_down()
            self.k += 1
        self.optimized = True
      
    @property
    def get_result(self):
        if self.optimized:
            return self.current_x, -1*self.func(self.current_x, self.cov_matrix, self.ind_er)
        else:
            return "Not optimized"


def obj_func(weights, cov_matrix, ind_er, risk_factor=0.02):
    """Function calculates the sharpe ratio of a given weight vector and, since we aim for minimization,
    the result is first multiplied by -1 and then returned"""
    port_er = (weights * ind_er).sum()  # portfolio return
    port_var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()  # portfolio variance
    sd = np.sqrt(port_var)  # portfolio standard deviation
    if sd == 0:  # it can happen, although it is not very likely
        return 0
    volatility = sd * np.sqrt(250)  # Annual standard deviation = volatility
    sharpe_ratio = (port_er - risk_factor) / volatility
    return -1*sharpe_ratio




