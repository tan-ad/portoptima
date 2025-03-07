import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from data_handler import fetch_data, calculate_returns
from portfolio import Portfolio
from optimization import simulate_random_portfolios, optimize_portfolio, get_efficient_frontier
from visualization import (
    plot_efficient_frontier, 
    plot_asset_allocation, 
    plot_correlation_matrix,
    plot_performance_summary
)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Analyze and optimize investment portfolios')
    
    # Required arguments
    parser.add_argument('--tickers', nargs='+', required=True, 
                        help='List of asset tickers (e.g., AAPL MSFT GOOGL)')
    
    # Optional arguments
    parser.add_argument('--weights', nargs='+', type=float, 
                        help='List of asset weights (must sum to 1)')
    parser.add_argument('--period', default='5y', 
                        help='Period for historical data (default: 5y)')
    parser.add_argument('--interval', default='1d', 
                        help='Data interval (default: 1d, options: 1d, 1wk, 1mo)')
    parser.add_argument('--risk-free-rate', type=float, default=0.02, 
                        help='Annual risk-free rate (default: 0.02)')
    parser.add_argument('--frequency', default='daily', 
                        help='Return frequency (default: daily, options: daily, weekly, monthly)')
    parser.add_argument('--num-simulations', type=int, default=10000, 
                        help='Number of simulated portfolios (default: 10000)')
    parser.add_argument('--optimization', default='sharpe', 
                        help='Optimization target (default: sharpe, options: sharpe, min_volatility, max_return)')
    parser.add_argument('--target-return', type=float, 
                        help='Target return for optimization (only if optimization=target_return)')
    parser.add_argument('--min-weight', type=float, default=0, 
                        help='Minimum weight for any asset (default: 0)')
    parser.add_argument('--max-weight', type=float, default=1, 
                        help='Maximum weight for any asset (default: 1)')
    parser.add_argument('--output-dir', default='output', 
                        help='Directory to save output files (default: current directory)')
    parser.add_argument('--no-show', action='store_true',
                        help='Do not show interactive plots (just save them)')
    
    return parser.parse_args()

def main():
    """Main function."""
    try:
        args = parse_arguments()
        
        # Create output directory if it doesn't exist
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
        
        # Get tickers and weights
        tickers = args.tickers
        
        # Set equal weights if not provided
        if args.weights:
            weights = args.weights
            if len(weights) != len(tickers):
                raise ValueError("Number of weights must match number of tickers")
            # Normalize weights to sum to 1
            if abs(sum(weights) - 1.0) > 1e-6:
                print(f"Warning: Weights sum to {sum(weights)}, normalizing to 1.0")
                weights = [w/sum(weights) for w in weights]
        else:
            weights = [1.0/len(tickers)] * len(tickers)  # Equal weights
        
        print(f"Fetching data for {tickers}...")
        prices = fetch_data(tickers, args.period, args.interval)
        
        # Check if we got data for all tickers
        if prices.shape[1] != len(tickers):
            print(f"Warning: Data only available for {prices.shape[1]} out of {len(tickers)} tickers")
            # Adjust weights for tickers we have data for
            if isinstance(prices.columns, pd.MultiIndex):
                available_tickers = list(set([col[1] for col in prices.columns]))
            else:
                available_tickers = prices.columns.tolist()
            print(f"Available tickers: {available_tickers}")
            
            # Create a mapping of available tickers to their original weights
            ticker_weight_map = {tick: w for tick, w in zip(tickers, weights)}
            
            # Adjust tickers and weights lists
            tickers = available_tickers
            weights = [ticker_weight_map.get(tick, 0) for tick in tickers]
            
            # Normalize weights again
            weights = [w/sum(weights) for w in weights]
            
            print(f"Adjusted portfolio: {list(zip(tickers, weights))}")
        
        print("Calculating returns...")
        returns = calculate_returns(prices, args.frequency)
        
        # Print data information for debugging
        print(f"Data period: {prices.index[0]} to {prices.index[-1]}")
        print(f"Number of data points: {len(prices)}")
        
        print("Creating portfolio...")
        current_portfolio = Portfolio(
            returns, 
            weights, 
            args.risk_free_rate, 
            args.frequency
        )
        
        print(f"Simulating {args.num_simulations} portfolios...")
        results, weights_record = simulate_random_portfolios(
            returns, 
            args.num_simulations, 
            args.risk_free_rate, 
            args.frequency
        )
        
        print("Optimizing portfolio...")
        optimal_portfolio = optimize_portfolio(
            returns, 
            args.risk_free_rate, 
            args.frequency, 
            args.optimization, 
            args.target_return, 
            args.min_weight, 
            args.max_weight
        )
        
        print("Generating efficient frontier...")
        efficient_frontier = get_efficient_frontier(
            returns, 
            args.risk_free_rate, 
            args.frequency, 
            points=50, 
            min_weight=args.min_weight, 
            max_weight=args.max_weight
        )
        
        # Print summary
        print("\n--- Portfolio Analysis Summary ---")
        print("\nCurrent Portfolio:")
        print(f"Expected Annual Return: {current_portfolio.metrics['expected_return']*100:.2f}%")
        print(f"Annual Volatility: {current_portfolio.metrics['volatility']*100:.2f}%")
        print(f"Sharpe Ratio: {current_portfolio.metrics['sharpe_ratio']:.2f}")
        
        print("\nOptimal Portfolio:")
        print(f"Expected Annual Return: {optimal_portfolio['metrics']['expected_return']*100:.2f}%")
        print(f"Annual Volatility: {optimal_portfolio['metrics']['volatility']*100:.2f}%")
        print(f"Sharpe Ratio: {optimal_portfolio['metrics']['sharpe_ratio']:.2f}")
        
        print("\nOptimal Asset Allocation:")
        for i, ticker in enumerate(tickers):
            print(f"{ticker}: {optimal_portfolio['weights'][i]*100:.2f}%")
        
        # Generate visualizations
        print("\nGenerating visualizations...")
        
        # Change to output directory
        original_dir = os.getcwd()
        os.chdir(args.output_dir)
        
        # Add risk-free rate to current_portfolio for the capital market line
        current_portfolio_dict = {
            'metrics': current_portfolio.metrics,
            'weights': current_portfolio.weights,
            'risk_free_rate': args.risk_free_rate
        }
        
        # Plot efficient frontier
        print("Plotting efficient frontier...")
        plt.figure(figsize=(12, 8))
        plot_efficient_frontier(
            results, 
            current_portfolio_dict, 
            optimal_portfolio, 
            efficient_frontier,
            show_plot=not args.no_show
        )
        
        # Plot asset allocation
        print("Plotting asset allocation...")
        plot_asset_allocation(
            {'weights': current_portfolio.weights}, 
            optimal_portfolio, 
            tickers,
            show_plot=not args.no_show
        )
        
        # Plot correlation matrix
        print("Plotting correlation matrix...")
        plot_correlation_matrix(
            returns,
            show_plot=not args.no_show
        )
        
        # Plot performance summary
        print("Plotting performance summary...")
        plot_performance_summary(
            optimal_portfolio,
            show_plot=not args.no_show
        )
        
        # Return to original directory
        os.chdir(original_dir)
        
        print("\nAnalysis complete!")
        print(f"Visualization files saved in: {os.path.abspath(args.output_dir)}")
    
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
