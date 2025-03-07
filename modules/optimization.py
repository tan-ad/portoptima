import numpy as np
import pandas as pd
from scipy.optimize import minimize
from portfolio import Portfolio

def simulate_random_portfolios(returns, num_simulations=10000, risk_free_rate=0.02, frequency='daily'):
    """
    Generate random portfolios and calculate metrics.
    
    Parameters:
    -----------
    returns : pd.DataFrame
        DataFrame with asset returns
    num_simulations : int
        Number of simulated portfolios
    risk_free_rate : float
        Annual risk-free rate
    frequency : str
        Return frequency ('daily', 'weekly', 'monthly')
    
    Returns:
    --------
    tuple
        (results, weights_record)
        results: array with [return, volatility, sharpe ratio] for each portfolio
        weights_record: array with weights for each portfolio
    """
    num_assets = returns.shape[1]
    results = np.zeros((num_simulations, 3))  # Return, volatility, Sharpe ratio
    weights_record = np.zeros((num_simulations, num_assets))
    
    for i in range(num_simulations):
        # Generate random weights
        weights = np.random.random(num_assets)
        weights = weights / np.sum(weights)  # Normalize to sum to 1
        weights_record[i, :] = weights
        
        # Calculate portfolio metrics
        portfolio = Portfolio(returns, weights, risk_free_rate, frequency)
        metrics = portfolio.metrics
        
        results[i, 0] = metrics['expected_return']
        results[i, 1] = metrics['volatility']
        results[i, 2] = metrics['sharpe_ratio']
    
    return results, weights_record

def optimize_portfolio(returns, risk_free_rate=0.02, frequency='daily', 
                        target='sharpe', target_return=None, min_weight=0, max_weight=1):
    """
    Optimize portfolio based on target.
    
    Parameters:
    -----------
    returns : pd.DataFrame
        DataFrame with asset returns
    risk_free_rate : float
        Annual risk-free rate
    frequency : str
        Return frequency ('daily', 'weekly', 'monthly')
    target : str
        Optimization target ('sharpe', 'min_volatility', 'max_return', 'target_return')
    target_return : float, optional
        Target return if target='target_return'
    min_weight : float
        Minimum weight for any asset
    max_weight : float
        Maximum weight for any asset
    
    Returns:
    --------
    dict
        Dictionary with optimal weights and metrics
    """
    num_assets = returns.shape[1]
    
    # Create initial portfolio with equal weights
    initial_weights = np.array([1/num_assets] * num_assets)
    portfolio = Portfolio(returns, initial_weights, risk_free_rate, frequency)
    
    # Define constraints
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]  # Weights sum to 1
    
    if target == 'target_return' and target_return is not None:
        ann_factor = portfolio.get_annualization_factor()
        expected_returns = portfolio.expected_returns
        constraints.append({
            'type': 'eq',
            'fun': lambda x: ann_factor * np.sum(expected_returns * x) - target_return
        })
    
    # Define bounds
    bounds = tuple((min_weight, max_weight) for _ in range(num_assets))
    
    # Define objective function based on target
    if target == 'sharpe':
        def objective(weights):
            portfolio.update_weights(weights)
            return -portfolio.metrics['sharpe_ratio']
    elif target == 'min_volatility':
        def objective(weights):
            portfolio.update_weights(weights)
            return portfolio.metrics['volatility']
    elif target == 'max_return':
        def objective(weights):
            portfolio.update_weights(weights)
            return -portfolio.metrics['expected_return']
    elif target == 'target_return':
        def objective(weights):
            portfolio.update_weights(weights)
            return portfolio.metrics['volatility']
    else:
        raise ValueError("Invalid optimization target")
    
    # Optimize
    result = minimize(objective, initial_weights, method='SLSQP', 
                      bounds=bounds, constraints=constraints)
    
    if not result['success']:
        raise ValueError(f"Optimization failed: {result['message']}")
    
    # Calculate metrics for the optimized portfolio
    optimal_weights = result['x']
    portfolio.update_weights(optimal_weights)
    
    return {
        'weights': optimal_weights,
        'metrics': portfolio.metrics
    }

def get_efficient_frontier(returns, risk_free_rate=0.02, frequency='daily', 
                           points=50, min_weight=0, max_weight=1):
    """
    Generate the efficient frontier.
    
    Parameters:
    -----------
    returns : pd.DataFrame
        DataFrame with asset returns
    risk_free_rate : float
        Annual risk-free rate
    frequency : str
        Return frequency ('daily', 'weekly', 'monthly')
    points : int
        Number of points on the efficient frontier
    min_weight : float
        Minimum weight for any asset
    max_weight : float
        Maximum weight for any asset
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with returns and volatilities for the efficient frontier
    """
    # Find min and max return portfolios
    min_vol_portfolio = optimize_portfolio(returns, risk_free_rate, frequency, 
                                          'min_volatility', min_weight=min_weight, 
                                          max_weight=max_weight)
    max_return_portfolio = optimize_portfolio(returns, risk_free_rate, frequency, 
                                             'max_return', min_weight=min_weight, 
                                             max_weight=max_weight)
    
    min_return = min_vol_portfolio['metrics']['expected_return']
    max_return = max_return_portfolio['metrics']['expected_return']
    
    # Generate target returns
    target_returns = np.linspace(min_return, max_return, points)
    
    # Calculate efficient frontier
    efficient_frontier = []
    for target_return in target_returns:
        try:
            portfolio = optimize_portfolio(returns, risk_free_rate, frequency, 
                                          'target_return', target_return=target_return,
                                          min_weight=min_weight, max_weight=max_weight)
            
            efficient_frontier.append({
                'return': portfolio['metrics']['expected_return'],
                'volatility': portfolio['metrics']['volatility']
            })
        except:
            # Skip if optimization fails
            continue
    
    return pd.DataFrame(efficient_frontier)
