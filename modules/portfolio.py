import numpy as np
import pandas as pd

class Portfolio:
    """
    Class for analyzing investment portfolios.
    """
    
    def __init__(self, returns, weights=None, risk_free_rate=0.02, frequency='daily'):
        """
        Initialize a Portfolio object.
        
        Parameters:
        -----------
        returns : pd.DataFrame
            DataFrame with asset returns
        weights : array-like, optional
            Asset weights. If None, equal weighting is assumed.
        risk_free_rate : float
            Annual risk-free rate
        frequency : str
            Return frequency ('daily', 'weekly', 'monthly')
        """
        self.returns = returns
        self.assets = returns.columns.tolist()
        self.num_assets = len(self.assets)
        
        # Set weights (equal by default)
        if weights is None:
            self.weights = np.array([1.0/self.num_assets] * self.num_assets)
        else:
            weights = np.array(weights)
            # Ensure weights sum to 1
            if not np.isclose(sum(weights), 1.0):
                weights = weights / sum(weights)
            self.weights = weights
            
        self.risk_free_rate = risk_free_rate
        self.frequency = frequency
        
        # Calculate metrics
        self.expected_returns = self._calculate_expected_returns()
        self.cov_matrix = self._calculate_covariance_matrix()
        self.metrics = self.calculate_metrics()
    
    def _calculate_expected_returns(self):
        """Calculate expected returns for each asset."""
        return self.returns.mean()
    
    def _calculate_covariance_matrix(self):
        """Calculate covariance matrix of returns."""
        return self.returns.cov()
    
    def get_annualization_factor(self):
        """Return the annualization factor for the frequency."""
        if self.frequency == 'daily':
            return 252  # Trading days in a year
        elif self.frequency == 'weekly':
            return 52
        elif self.frequency == 'monthly':
            return 12
        else:
            raise ValueError("Invalid frequency")
    
    def calculate_metrics(self):
        """Calculate portfolio metrics."""
        # Annualization factor
        ann_factor = self.get_annualization_factor()
        
        # Portfolio expected return (annualized)
        portfolio_return = np.sum(self.expected_returns * self.weights) * ann_factor
        
        # Portfolio volatility (annualized)
        portfolio_volatility = np.sqrt(
            np.dot(self.weights.T, np.dot(self.cov_matrix * ann_factor, self.weights))
        )
        
        # Sharpe ratio
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        
        return {
            'expected_return': portfolio_return,
            'volatility': portfolio_volatility,
            'sharpe_ratio': sharpe_ratio
        }
    
    def update_weights(self, new_weights):
        """Update portfolio weights and recalculate metrics."""
        # Ensure weights sum to 1
        new_weights = np.array(new_weights)
        if not np.isclose(sum(new_weights), 1.0):
            new_weights = new_weights / sum(new_weights)
        
        self.weights = new_weights
        self.metrics = self.calculate_metrics()
        
        return self.metrics
