import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
total_investment = 1200000  # INR
risk_free_rate = 0.07
risk_free_rate = 0.07
start_date = "2019-06-01"
end_date = "2025-06-01"
equity = {
    'POLYCAB.NS': 0.08,
    'FINCABLES.NS': 0.07,
    'CAPLIPOINT.NS': 0.10,
    'ASIANPAINT.NS': 0.10,
    'MPHASIS.NS': 0.10,
    'PERSISTENT.NS': 0.10,
    'TATAMOTORS.NS': 0.15,
    'VOLTAMP.NS': 0.15,
    'ABB.NS': 0.15
}

etfs = {
    'NIFTYBEES.NS': 0.70,
    'HDFCSML250.NS': 0.30}

commodity = {
    'GOLDBEES.NS': 1.00
}
asset_classes = {
    "Equity": 0.45,
    "ETF": 0.30,
    "Commodity": 0.25
}
all_assets = {**equity, **etfs, **commodity}
tickers = list(all_assets.keys())
price_data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)["Close"]
price_data = price_data.dropna()
print("price_data") 
print(price_data.head())
daily_returns = price_data.pct_change().dropna()
print("daily_returns")
annual_returns = daily_returns.mean() * 252
volatility = daily_returns.std() * np.sqrt(252)
print("volatility "),
sharpe_ratio = (annual_returns - risk_free_rate) / volatility
print("sharp_ratio"),
allocations = {ticker: all_assets[ticker] * asset_classes[
    "Equity" if ticker in equity else "ETF" if ticker in etfs else "Commodity"
] for ticker in all_assets}
print("allocations"),
investment_per_asset = {ticker: total_investment * allocations[ticker] for ticker in allocations}
print("investment_per_asset "),
normalized = price_data / price_data.iloc[0]
print("normalized "),
portfolio_value = pd.DataFrame({ticker: normalized[ticker] * investment_per_asset[ticker] for ticker in allocations})
portfolio_value["Total"] = portfolio_value.sum(axis=1)
print('portfolio_value["Total"]')
with pd.ExcelWriter("portfolio_screener.xlsx", engine="openpyxl") as writer:
    price_data.to_excel(writer, sheet_name="Price Data")
    daily_returns.to_excel(writer, sheet_name="Daily Returns")
    annual_returns.to_frame("Annual Return").to_excel(writer, sheet_name="Annual Returns")
    volatility.to_frame("Volatility").to_excel(writer, sheet_name="Volatility")
    sharpe_ratio.to_frame("Sharpe Ratio").to_excel(writer, sheet_name="Sharpe Ratio")
    portfolio_value.to_excel(writer, sheet_name="Portfolio Value")

print("✅ Portfolio analysis saved to 'portfolio_performance.xlsx'")
 
import pandas as pd     
equity_tickers = ['POLYCAB.NS', 'FINCABLES.NS', 'CAPLIPOINT.NS', 'ASIANPAINT.NS', 
                  'MPHASIS.NS', 'PERSISTENT.NS', 'TATAMOTORS.NS', 
                  'VOLTAMP.NS', 'ABB.NS']
etf_tickers = ['NIFTYBEES.NS', 'HDFCSML250.NS']
commodity_tickers = ['GOLDBEES.NS']  
daily_returns = price_data.pct_change().dropna()
asset_class_returns = pd.DataFrame({
    "Equity": daily_returns[equity_tickers].mean(axis=1),
    "ETF": daily_returns[etf_tickers].mean(axis=1),
    "Commodity": daily_returns[commodity_tickers].mean(axis=1)
})
print("Daily Returns by Asset Class:")
correlation_matrix = asset_class_returns.corr()
print("\nCorrelation Between Asset Classes:")
print(correlation_matrix)
