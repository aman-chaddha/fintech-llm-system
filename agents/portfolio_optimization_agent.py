import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Sample assets and their historical returns
assets = ['AAPL', 'GOOGL', 'AMZN', 'BTC', 'ETH']
asset_prices = {
    'AAPL': [150, 153, 157, 155, 158],
    'GOOGL': [2800, 2850, 2825, 2875, 2900],
    'AMZN': [3400, 3450, 3475, 3420, 3500],
    'BTC': [40000, 40500, 42000, 43000, 44000],
    'ETH': [2800, 2900, 2950, 3000, 3100]
}

# Calculate daily returns for each asset
def calculate_returns(prices):
    returns = {}
    for asset, price in prices.items():
        returns[asset] = np.diff(price) / price[:-1]  # simple returns formula
    return returns

# Calculate portfolio statistics: return, variance, and covariance
def portfolio_statistics(weights, mean_returns, cov_matrix):
    portfolio_return = np.sum(mean_returns * weights)
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    portfolio_volatility = np.sqrt(portfolio_variance)
    return portfolio_return, portfolio_volatility

# Objective function: Minimize negative Sharpe ratio
def objective_function(weights, mean_returns, cov_matrix, risk_free_rate=0.01):
    portfolio_return, portfolio_volatility = portfolio_statistics(weights, mean_returns, cov_matrix)
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    return -sharpe_ratio  # negative because we want to maximize Sharpe ratio

# Constraints: weights must sum to 1
def constraint(weights):
    return np.sum(weights) - 1

# Portfolio optimization function
def optimize_portfolio(returns_data):
    # Calculate mean returns and covariance matrix
    mean_returns = np.mean(returns_data, axis=0)
    cov_matrix = np.cov(returns_data.T)

    # Initial guess for the weights (equally distributed)
    num_assets = len(mean_returns)
    initial_weights = np.ones(num_assets) / num_assets

    # Bounds for the weights: each weight between 0 and 1
    bounds = tuple((0, 1) for _ in range(num_assets))

    # Constraints: sum of weights equals 1
    constraints = ({'type': 'eq', 'fun': constraint})

    # Optimize portfolio
    result = minimize(objective_function, initial_weights, args=(mean_returns, cov_matrix),
                      method='SLSQP', bounds=bounds, constraints=constraints)

    return result.x  # Optimal portfolio weights

# Main function to run the portfolio optimization
def portfolio_optimization():
    # Convert asset prices into a DataFrame
    prices_df = pd.DataFrame(asset_prices)

    # Calculate returns for each asset
    returns_data = pd.DataFrame(calculate_returns(asset_prices))

    # Optimize the portfolio
    optimal_weights = optimize_portfolio(returns_data)

    # Display the optimal portfolio weights
    print("Optimal Portfolio Weights:")
    for i, asset in enumerate(assets):
        print(f"{asset}: {optimal_weights[i] * 100:.2f}%")

if __name__ == "__main__":
    portfolio_optimization()
