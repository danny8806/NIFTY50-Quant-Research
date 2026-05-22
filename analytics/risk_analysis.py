
import numpy as np

def volatility(returns):
    return returns.std() * np.sqrt(252)

def sharpe_ratio(returns, risk_free_rate=0.05):
    excess_return = returns.mean() * 252 - risk_free_rate
    return excess_return / volatility(returns)

def max_drawdown(cumulative_returns):
    rolling_max = cumulative_returns.cummax()
    drawdown = cumulative_returns / rolling_max - 1
    return drawdown.min()
