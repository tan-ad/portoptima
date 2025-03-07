# portoptima

A Python-based tool for investment portfolio analysis and optimization using Modern Portfolio Theory (MPT).

## Overview

This tool allows you to analyze an investment portfolio, calculate key risk and return metrics, generate an efficient frontier via Monte Carlo simulation, and optimize asset allocation. It evaluates your portfolio's performance and suggests an optimal asset allocation based on risk and return parameters.

## Features

- **Data Retrieval**: Fetch historical price data for a list of assets using Yahoo Finance.
- **Portfolio Analysis**: Calculate expected return, volatility, and Sharpe ratio.
- **Monte Carlo Simulation**: Generate random portfolios to visualize the efficient frontier.
- **Portfolio Optimization**: Find optimal portfolios that maximize Sharpe ratio or minimize variance.
- **Visualization**: Create charts of the efficient frontier, asset allocation, correlation matrix, and performance metrics.
- **Command Line Interface**: Simple CLI for data input and results display.

## Installation

1. Clone the repository:

   ``` bash
   git clone https://github.com/tan-ad/portoptima.git
   cd portfolio-optimizer
   ```

2. Create a virtual environment (optional but recommended):

   ``` bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:

   ``` bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

Run the analyzer with your portfolio:

```bash
python portfolio_analyzer.py --tickers AAPL MSFT GOOGL --weights 0.3 0.3 0.4
```

### Optional Parameters

- `--period 3y`: Set the period for historical data (default: 5y)
- `--interval 1wk`: Set the data interval (default: 1d)
- `--risk-free-rate 0.015`: Set the annual risk-free rate (default: 0.02)
- `--frequency weekly`: Set the return frequency (default: daily)
- `--num-simulations 5000`: Set the number of Monte Carlo simulations (default: 10000)
- `--optimization min_volatility`: Set the optimization target (default: sharpe)
- `--min-weight 0.05`: Set minimum weight for any asset (default: 0)
- `--max-weight 0.5`: Set maximum weight for any asset (default: 1)
- `--output-dir results`: Set directory to save output files (default: current directory)

### Example

Run the included example script for a quick demonstration:

```bash
python example.py
```

This will analyze a sample portfolio of tech stocks and save the visualizations in an `example_output` directory.

## Project Structure

- `data_handler.py`: Handles data acquisition and processing
- `portfolio.py`: Core portfolio analysis functionality
- `optimization.py`: Portfolio optimization features
- `visualization.py`: Plotting and visualization
- `portfolio_analyzer.py`: Main CLI application
- `example.py`: Example usage script
- `requirements.txt`: Dependencies

## Output

The tool generates:

- A detailed text summary of portfolio metrics
- Visual charts saved as PNG files:
  - Efficient frontier plot
  - Current vs. optimal asset allocation
  - Asset correlation matrix
  - Performance metrics summary

## Dependencies

- `numpy`: Numerical computations
- `pandas`: Data handling and manipulation
- `matplotlib`: Visualization
- `scipy`: Optimization algorithms
- `yfinance`: Yahoo Finance API for historical data
