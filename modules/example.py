import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from data_handler import fetch_data, calculate_returns
from portfolio import Portfolio
from optimization import simulate_random_portfolios, optimize_portfolio, get_efficient_frontier
from visualization import (
    plot_efficient_frontier, 
    plot_asset_allocation, 
    plot_correlation_matrix,
    plot_performance_summary
)

def run_example():
    """Run an example portfolio analysis."""
    # Define example portfolio
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'BRK-B']
    weights = [0.2, 0.2, 0.2, 0.2, 0.2]  # Equal weights for simplicity
    
    print("Portfolio Analyzer Example")
    print("--------------------------")
    print(f"Analyzing portfolio with tickers: {tickers}")
    
    try:
        # Fetch historical data
        print("Fetching historical data...")
        prices = fetch_data(tickers, period='5y', interval='1d')
        
        # Show data sample
        print("\nPrice data sample:")
        print(prices.head())
        
        # Calculate returns
        print("\nCalculating returns...")
        returns = calculate_returns(prices, frequency='daily')
        
        print("\nReturns data sample:")
        print(returns.head())
        
        # Create current portfolio
        print("\nCreating portfolio object...")
        current_portfolio = Portfolio(returns, weights, risk_free_rate=0.02, frequency='daily')
        
        # Print current portfolio metrics
        print("\nCurrent Portfolio Metrics:")
        print(f"Expected Annual Return: {current_portfolio.metrics['expected_return']*100:.2f}%")
        print(f"Annual Volatility: {current_portfolio.metrics['volatility']*100:.2f}%")
        print(f"Sharpe Ratio: {current_portfolio.metrics['sharpe_ratio']:.2f}")
        
        # Simulate random portfolios
        print("\nRunning Monte Carlo simulation (this may take a moment)...")
        num_simulations = 5000  # Reduced for quicker execution in example
        results, weights_record = simulate_random_portfolios(
            returns, num_simulations, risk_free_rate=0.02, frequency='daily'
        )
        
        # Optimize portfolio
        print("\nOptimizing portfolio for maximum Sharpe ratio...")
        optimal_portfolio = optimize_portfolio(
            returns, risk_free_rate=0.02, frequency='daily', target='sharpe'
        )
        
        # Print optimal portfolio metrics
        print("\nOptimal Portfolio Metrics:")
        print(f"Expected Annual Return: {optimal_portfolio['metrics']['expected_return']*100:.2f}%")
        print(f"Annual Volatility: {optimal_portfolio['metrics']['volatility']*100:.2f}%")
        print(f"Sharpe Ratio: {optimal_portfolio['metrics']['sharpe_ratio']:.2f}")
        
        # Print optimal asset allocation
        print("\nOptimal Asset Allocation:")
        for i, ticker in enumerate(returns.columns):
            print(f"{ticker}: {optimal_portfolio['weights'][i]*100:.2f}%")
        
        # Generate efficient frontier
        print("\nGenerating efficient frontier...")
        efficient_frontier = get_efficient_frontier(
            returns, risk_free_rate=0.02, frequency='daily', points=50
        )
        
        # Add risk-free rate to current_portfolio for the capital market line
        current_portfolio_dict = {
            'metrics': current_portfolio.metrics,
            'weights': current_portfolio.weights,
            'risk_free_rate': 0.02
        }
        
        # Visualizations
        print("\nGenerating visualizations...")
        
        # Create output directory if it doesn't exist
        output_dir = 'example_output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Change working directory to save plots in output directory
        original_dir = os.getcwd()
        os.chdir(output_dir)
        
        # Set show_plot to False to prevent blocking
        show_plots = False
        
        # Plot efficient frontier
        print("Plotting efficient frontier...")
        plt.figure(figsize=(12, 8))
        plot_efficient_frontier(
            results, 
            current_portfolio_dict, 
            optimal_portfolio, 
            efficient_frontier,
            show_plot=show_plots
        )
        
        # Plot asset allocation
        print("Plotting asset allocation...")
        plot_asset_allocation(
            {'weights': current_portfolio.weights}, 
            optimal_portfolio, 
            list(returns.columns),
            show_plot=show_plots
        )
        
        # Plot correlation matrix
        print("Plotting correlation matrix...")
        plot_correlation_matrix(returns, show_plot=show_plots)
        
        # Plot performance summary
        print("Plotting performance summary...")
        plot_performance_summary(optimal_portfolio, show_plot=show_plots)
        
        # Return to original directory
        os.chdir(original_dir)
        
        print(f"\nAnalysis complete! Visualizations saved in the '{output_dir}' directory.")
    
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_example()
