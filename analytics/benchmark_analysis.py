
import statsmodels.api as sm

def beta_alpha(stock_returns, benchmark_returns):
    benchmark_returns = sm.add_constant(benchmark_returns)
    model = sm.OLS(stock_returns, benchmark_returns).fit()

    alpha = model.params.iloc[0]
    beta = model.params.iloc[1]

    return alpha, beta
