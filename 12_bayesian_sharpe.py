import yfinance as yf
import numpy as np
import pandas as pd
import pymc3 as pm
import matplotlib.pyplot as plt
from scipy.stats import norm
import multiprocessing as mp
import logging

# Set up the logger
logging.basicConfig(level=logging.INFO)

# Function to perform Bayesian estimation for a given date
def bayesian_estimation(date):
    logging.info(f"Performing Bayesian estimation for date: {date}")
    # Estimate Sharpe ratio using EWMA
    ewma_returns = log_returns.loc[:date].ewm(span=60).mean()  # 60-day EWMA of returns
    ewma_std = log_returns.loc[:date].ewm(span=60).std()  # 60-day EWMA of standard deviation
    ewma_sharpe = ewma_returns / ewma_std
    # Parameters for the normal prior
    mean_sharpe = ewma_sharpe.iloc[-1]
    std_sharpe = ewma_sharpe.std()
    with pm.Model() as model:
        # Define the prior for the Sharpe ratio
        sharpe = pm.Normal('sharpe', mu=mean_sharpe, sd=std_sharpe, shape=len(tickers))
        # Define the likelihood of the observed returns
        likelihood = pm.Normal('likelihood', mu=sharpe, sd=1, observed=log_returns.loc[:date])
        # Perform MCMC sampling to generate the posterior distribution
        trace = pm.sample(5000, tune=1000, cores=1)
    # Extract portfolio weights that maximize the expected Sharpe ratio
    max_sharpe_idx = np.argmax([np.mean(trace['sharpe'][:,i]) / np.std(trace['sharpe'][:,i]) for i in range(len(tickers))])
    weights = trace['sharpe'][max_sharpe_idx]
    # Normalize weights
    weights = weights / np.sum(np.abs(weights))
    # Store weights and returns
    return date, weights, np.dot(weights, log_returns.loc[date])

# Download historical data
logging.info("Downloading historical data...")
tickers = ['VOO', 'IEI', 'GLD']
start_date = '2008-01-01'
data = yf.download(tickers, start=start_date)
prices = data['Adj Close'].dropna()

# Compute log returns
logging.info("Computing log returns...")
log_returns = np.log(prices/prices.shift(1)).dropna()

# Create a multiprocessing Pool and parallelize the Bayesian estimation process
logging.info("Performing Bayesian estimations...")
pool = mp.Pool(mp.cpu_count())
results = pool.map(bayesian_estimation, log_returns.index[60:])  # Start from the 61st day to have enough data for EWMA calculation
pool.close()

# Unpack results
dates, weights_list, returns_list = zip(*results)
weights_dict = dict(zip(dates, weights_list))
returns_dict = dict(zip(dates, returns_list))

# Backtesting
logging.info("Backtesting...")
portfolio_returns = pd.Series(returns_dict)
portfolio_cumulative_returns = (1 + portfolio_returns).cumprod()

# Plot cumulative returns
logging.info("Plotting cumulative returns...")
plt.figure(figsize=(10,5))
plt.plot(portfolio_cumulative_returns)
plt.title('Backtest with Bayesian Portfolio')
plt.xlabel('Time')
plt.ylabel('Cumulative Portfolio Returns')
plt.grid(True)
plt.show()
