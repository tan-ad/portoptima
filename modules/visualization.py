import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_efficient_frontier(results, current_portfolio, optimal_portfolio, efficient_frontier=None, show_plot=True):
    """
    Plot the efficient frontier and highlight current and optimal portfolios.
    
    Parameters:
    -----------
    results : np.ndarray
        Array with [return, volatility, sharpe ratio] for simulated portfolios
    current_portfolio : dict
        Dictionary with current portfolio metrics
    optimal_portfolio : dict
        Dictionary with optimal portfolio metrics
    efficient_frontier : pd.DataFrame, optional
        DataFrame with efficient frontier points
    show_plot : bool, default=True
        Whether to display the plot (plt.show()) or just save to file
    """
    # Plot simulated portfolios
    plt.scatter(results[:, 1], results[:, 0], c=results[:, 2], cmap='viridis', 
                marker='o', s=10, alpha=0.3)
    plt.colorbar(label='Sharpe Ratio')
    
    # Plot efficient frontier if provided
    if efficient_frontier is not None:
        plt.plot(efficient_frontier['volatility'], efficient_frontier['return'], 
                'r-', linewidth=3, label='Efficient Frontier')
    
    # Highlight current portfolio
    plt.scatter(current_portfolio['metrics']['volatility'], 
                current_portfolio['metrics']['expected_return'], 
                marker='*', color='red', s=200, label='Current Portfolio')
    
    # Highlight optimal portfolio
    plt.scatter(optimal_portfolio['metrics']['volatility'], 
                optimal_portfolio['metrics']['expected_return'], 
                marker='X', color='green', s=200, label='Optimal Portfolio')
    
    # Add capital market line if maximizing Sharpe ratio
    max_sharpe_port = optimal_portfolio
    if max_sharpe_port is not None:
        x_values = [0, max_sharpe_port['metrics']['volatility'] * 1.5]
        y_values = [current_portfolio['risk_free_rate'], 
                   current_portfolio['risk_free_rate'] + 
                   max_sharpe_port['metrics']['sharpe_ratio'] * x_values[1]]
        plt.plot(x_values, y_values, 'g--', label='Capital Market Line')
    
    plt.title('Portfolio Optimization')
    plt.xlabel('Volatility (Risk)')
    plt.ylabel('Expected Annual Return')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('efficient_frontier.png')
    print("Saved efficient frontier plot to 'efficient_frontier.png'")
    
    if show_plot:
        plt.show()
    else:
        plt.close()

def plot_asset_allocation(current_portfolio, optimal_portfolio, assets, show_plot=True):
    """
    Plot pie charts comparing current and optimal asset allocations.
    
    Parameters:
    -----------
    current_portfolio : dict
        Dictionary with current portfolio weights
    optimal_portfolio : dict
        Dictionary with optimal portfolio weights
    assets : list
        List of asset names
    show_plot : bool, default=True
        Whether to display the plot (plt.show()) or just save to file
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    # Current allocation
    ax1.pie(current_portfolio['weights'], labels=assets, autopct='%1.1f%%')
    ax1.set_title('Current Asset Allocation')
    
    # Optimal allocation
    ax2.pie(optimal_portfolio['weights'], labels=assets, autopct='%1.1f%%')
    ax2.set_title('Optimal Asset Allocation')
    
    plt.tight_layout()
    plt.savefig('asset_allocation.png')
    print("Saved asset allocation plot to 'asset_allocation.png'")
    
    if show_plot:
        plt.show()
    else:
        plt.close()

def plot_correlation_matrix(returns, show_plot=True):
    """
    Plot correlation matrix of asset returns.
    
    Parameters:
    -----------
    returns : pd.DataFrame
        DataFrame with asset returns
    show_plot : bool, default=True
        Whether to display the plot (plt.show()) or just save to file
    """
    corr_matrix = returns.corr()
    
    plt.figure(figsize=(10, 8))
    plt.imshow(corr_matrix, cmap='coolwarm')
    plt.colorbar(label='Correlation')
    
    # Add correlation values
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix)):
            plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', 
                    ha='center', va='center', color='black')
    
    plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=45)
    plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
    
    plt.title('Asset Correlation Matrix')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png')
    print("Saved correlation matrix plot to 'correlation_matrix.png'")
    
    if show_plot:
        plt.show()
    else:
        plt.close()

def plot_performance_summary(portfolio, show_plot=True):
    """
    Plot summary of portfolio performance metrics.
    
    Parameters:
    -----------
    portfolio : dict
        Dictionary with portfolio metrics
    show_plot : bool, default=True
        Whether to display the plot (plt.show()) or just save to file
    """
    metrics = [
        ('Expected Return', portfolio['metrics']['expected_return'] * 100),
        ('Volatility', portfolio['metrics']['volatility'] * 100),
        ('Sharpe Ratio', portfolio['metrics']['sharpe_ratio'])
    ]
    
    labels, values = zip(*metrics)
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.2f}', ha='center', va='bottom')
    
    plt.title('Portfolio Performance Metrics')
    plt.ylabel('Value')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('performance_summary.png')
    print("Saved performance summary plot to 'performance_summary.png'")
    
    if show_plot:
        plt.show()
    else:
        plt.close()
