# 📊 PortOptima

A Python tool for portfolio analysis and optimization using Modern Portfolio Theory (MPT).

## 📋 Overview

PortOptima is a practical implementation of portfolio theory concepts that helps analyze investment portfolios and explore optimization possibilities. This tool demonstrates how MPT principles can be applied to evaluate portfolio performance, visualize risk-return relationships, and suggest potentially improved asset allocations.

![Portfolio Optimization](https://img.shields.io/badge/Academic-Project-blue)

## 🖼️ Sample Outputs

Here's what the tool can generate:

### Asset Allocation Comparison

![Asset Allocation](modules/example_output/asset_allocation.png)

*Comparison between equal-weight allocation and optimized weights*

### Asset Correlation Matrix

![Correlation Matrix](modules/example_output/correlation_matrix.png)

*Correlation structure between assets in the portfolio*

### Efficient Frontier

![Efficient Frontier](modules/example_output/efficient_frontier.png)

*Risk-return tradeoff with randomly generated portfolios*

### Performance Metrics

![Performance Metrics](modules/example_output/performance_summary.png)

*Key metrics for the analyzed portfolio*

## ✨ Features

- **Data Retrieval**: Fetch historical price data for stocks using Yahoo Finance API
- **Portfolio Analysis**: Calculate basic risk and return metrics
- **Simulation**: Generate random portfolios to visualize the efficient frontier
- **Basic Optimization**: Find portfolios with improved Sharpe ratio or reduced volatility
- **Visualization**: Create charts of efficient frontier, allocations, and metrics
- **Command Line Interface**: Simple inputs for portfolio analysis

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/tan-ad/portoptima.git
   cd portoptima/modules
   ```

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## 💡 Usage

### Basic Example

Analyze a portfolio with equal weights:

```bash
python portfolio_analyzer.py --tickers AAPL MSFT GOOGL AMZN BRK-B
```

### Custom Weights

```bash
python portfolio_analyzer.py --tickers AAPL MSFT GOOGL AMZN BRK-B --weights 0.2 0.2 0.2 0.2 0.2
```

### Finding an Optimized Portfolio

```bash
python portfolio_analyzer.py --tickers AAPL MSFT GOOGL AMZN BRK-B --optimization max_sharpe
```

### Quick Demo

Run the example script for a demonstration:

```bash
python example.py
```

## ⌨️ Command-Line Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--tickers` | List of ticker symbols | Required |
| `--weights` | Portfolio weights | Equal weights |
| `--period` | Historical data period (e.g., 1y, 5y) | 5y |
| `--interval` | Data interval (1d, 1wk, 1mo) | 1d |
| `--risk-free-rate` | Annual risk-free rate | 0.02 |
| `--num-simulations` | Number of Monte Carlo simulations | 5000 |
| `--optimization` | Optimization target (max_sharpe, min_volatility) | max_sharpe |
| `--min-weight` | Minimum weight constraint | 0 |
| `--max-weight` | Maximum weight constraint | 1 |
| `--output-dir` | Directory to save output files | Current directory |

## ⚠️ Limitations

- This is an educational tool that implements theoretical concepts
- Results should not be used as the sole basis for actual investment decisions
- Historical performance does not guarantee future results
- The optimization is based on historical data only and doesn't account for forward-looking views
- Transaction costs, taxes, and liquidity constraints are not considered

## 🔧 Dependencies

- `numpy`: Numerical computations
- `pandas`: Data handling
- `matplotlib`: Visualization
- `scipy`: Optimization algorithms
- `yfinance`: Yahoo Finance API for historical data
- `seaborn`: Enhanced visualizations

## 📜 License

No license, do whatever you want with this.

---

*This tool was created as a learning project to explore portfolio theory concepts.* 🎓
