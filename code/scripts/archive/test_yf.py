import yfinance as yf
import pandas as pd

# Test ICBP.JK price history
icbp = yf.Ticker("ICBP.JK")
hist = icbp.history(start="2010-10-01")
print("ICBP History shape:", hist.shape)
print("Start date:", hist.index[0] if not hist.empty else "None")
print("End date:", hist.index[-1] if not hist.empty else "None")
print("Sample columns:", hist.columns.tolist())

# Test JKSE
jkse = yf.Ticker("^JKSE")
hist_jkse = jkse.history(start="2010-10-01")
print("JKSE History shape:", hist_jkse.shape)

# Test financials from yfinance
print("\nFinancials available in yfinance:")
print("Financials shape:", icbp.financials.shape if icbp.financials is not None else "None")
print("Years in financials:", icbp.financials.columns.tolist() if icbp.financials is not None else [])
print("Balance sheet shape:", icbp.balance_sheet.shape if icbp.balance_sheet is not None else "None")
print("Cashflow shape:", icbp.cashflow.shape if icbp.cashflow is not None else "None")
print("Actions (dividends/splits):", len(icbp.actions))
