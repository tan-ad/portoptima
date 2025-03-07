import yfinance as yf
import pandas as pd
import numpy as np

def fetch_data(tickers, period='5y', interval='1d'):
    """
    Fetch historical price data for given tickers.
    
    Parameters:
    -----------
    tickers : list
        List of asset tickers
    period : str
        Period for historical data (e.g., '5y', '1y', '6mo')
    interval : str
        Data interval (e.g., '1d', '1wk', '1mo')
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with adjusted close prices
    """
    try:
        # Download data
        data = yf.download(tickers, period=period, interval=interval)
        
        if data.empty:
            raise ValueError("No data retrieved for the given tickers")
        
        # Check if 'Adj Close' exists in the columns
        if 'Adj Close' in data.columns:
            price_data = data['Adj Close']
        # If we have a multi-level column index
        elif isinstance(data.columns, pd.MultiIndex) and 'Adj Close' in data.columns.levels[0]:
            price_data = data['Adj Close']
        # Fallback to 'Close' if 'Adj Close' is not available
        elif 'Close' in data.columns:
            print("Warning: 'Adj Close' not found. Using 'Close' prices instead.")
            price_data = data['Close']
        elif isinstance(data.columns, pd.MultiIndex) and 'Close' in data.columns.levels[0]:
            print("Warning: 'Adj Close' not found. Using 'Close' prices instead.")
            price_data = data['Close']
        else:
            # If neither 'Adj Close' nor 'Close' is found, use the first available column
            print("Warning: Neither 'Adj Close' nor 'Close' found. Using first available price column.")
            price_data = data.iloc[:, 0]
        
        # If only one ticker, yfinance returns a Series; convert to DataFrame
        if isinstance(price_data, pd.Series):
            price_data = price_data.to_frame(name=tickers[0])
        
        return price_data
    except Exception as e:
        print(f"Error details: {str(e)}")
        print(f"Data columns: {data.columns if 'data' in locals() else 'No data retrieved'}")
        raise Exception(f"Error fetching data: {str(e)}")

def calculate_returns(prices, frequency='daily'):
    """
    Calculate returns from price data.
    
    Parameters:
    -----------
    prices : pd.DataFrame
        DataFrame with price data
    frequency : str
        Return frequency ('daily', 'weekly', 'monthly')
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with calculated returns
    """
    if frequency == 'daily':
        returns = prices.pct_change().dropna()
    elif frequency == 'weekly':
        returns = prices.resample('W').last().pct_change().dropna()
    elif frequency == 'monthly':
        returns = prices.resample('M').last().pct_change().dropna()
    else:
        raise ValueError("Invalid frequency. Choose from 'daily', 'weekly', or 'monthly'")
    
    return returns

def get_annualization_factor(frequency='daily'):
    """Return the annualization factor for the given frequency."""
    if frequency == 'daily':
        return 252  # Trading days in a year
    elif frequency == 'weekly':
        return 52
    elif frequency == 'monthly':
        return 12
    else:
        raise ValueError("Invalid frequency. Choose from 'daily', 'weekly', or 'monthly'")
