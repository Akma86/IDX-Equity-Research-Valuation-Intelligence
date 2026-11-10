"""
02_scrape_stock_market_data.py
Pulls and processes daily OHLCV, adjusted close, and trading volume for ICBP.JK and IHSG (^JKSE)
from IPO date (October 2010) through present.
Computes technical indicators, moving averages, RSI, MACD, rolling volatility, beta,
52-week high/low, maximum drawdown, and relative performance vs IHSG benchmark,
as well as monthly and annual return series matching Data.md Section 2.2.
"""

import os
import yfinance as yf
import pandas as pd
import numpy as np

def scrape_stock_data():
    print("Scraping historical stock market data for ICBP.JK and IHSG (^JKSE)...")
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/raw/stock_market", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    start_date = "2010-10-01"
    end_date = "2026-10-30"
    
    # Check if raw files exist; if so, load them, or download if needed
    raw_icbp_path = "data/raw/icbp_daily_ohlcv_2010_2026.csv"
    raw_ihsg_path = "data/raw/ihsg_benchmark_daily_2010_2026.csv"
    
    if os.path.exists(raw_icbp_path) and os.path.exists(raw_ihsg_path):
        print("Loading cached daily OHLCV data from data/raw/...")
        icbp_raw = pd.read_csv(raw_icbp_path, index_col=0, parse_dates=True)
        ihsg_raw = pd.read_csv(raw_ihsg_path, index_col=0, parse_dates=True)
    else:
        print("Downloading fresh daily data from Yahoo Finance...")
        icbp_raw = yf.download("ICBP.JK", start=start_date, end=end_date, progress=False)
        if isinstance(icbp_raw.columns, pd.MultiIndex):
            icbp_raw.columns = [col[0] for col in icbp_raw.columns]
        icbp_raw.to_csv(raw_icbp_path)
        icbp_raw.to_csv("data/raw/stock_market/icbp_daily_ohlcv_2010_2026.csv")
        
        ihsg_raw = yf.download("^JKSE", start=start_date, end=end_date, progress=False)
        if isinstance(ihsg_raw.columns, pd.MultiIndex):
            ihsg_raw.columns = [col[0] for col in ihsg_raw.columns]
        ihsg_raw.to_csv(raw_ihsg_path)
        ihsg_raw.to_csv("data/raw/stock_market/ihsg_benchmark_daily_2010_2026.csv")
        
    print(f"ICBP daily records: {len(icbp_raw)}, IHSG daily records: {len(ihsg_raw)}")
    
    # 3. Create merged master dataset
    df = pd.DataFrame(index=icbp_raw.index)
    df["ICBP_Open"] = icbp_raw["Open"]
    df["ICBP_High"] = icbp_raw["High"]
    df["ICBP_Low"] = icbp_raw["Low"]
    df["ICBP_Close"] = icbp_raw["Close"]
    df["ICBP_AdjClose"] = icbp_raw.get("Adj Close", icbp_raw["Close"])
    df["ICBP_Volume"] = icbp_raw["Volume"]
    df["ICBP_Turnover_IDR"] = df["ICBP_Close"] * df["ICBP_Volume"]
    
    # Align with IHSG
    df = df.join(ihsg_raw[["Open", "High", "Low", "Close", "Volume"]].rename(columns={
        "Open": "IHSG_Open",
        "High": "IHSG_High",
        "Low": "IHSG_Low",
        "Close": "IHSG_Close",
        "Volume": "IHSG_Volume"
    }))
    
    # Forward fill missing weekend/holiday data
    df["IHSG_Close"] = df["IHSG_Close"].ffill()
    
    # Daily Returns
    df["ICBP_Daily_Return_%"] = df["ICBP_AdjClose"].pct_change() * 100.0
    df["IHSG_Daily_Return_%"] = df["IHSG_Close"].pct_change() * 100.0
    
    # Normalized Base 100 performance
    first_icbp = df["ICBP_AdjClose"].dropna().iloc[0]
    first_ihsg = df["IHSG_Close"].dropna().iloc[0]
    df["ICBP_Base100"] = (df["ICBP_AdjClose"] / first_icbp) * 100.0
    df["IHSG_Base100"] = (df["IHSG_Close"] / first_ihsg) * 100.0
    
    # Cumulative Return %
    df["ICBP_Cum_Return_%"] = (df["ICBP_Base100"] - 100.0)
    df["IHSG_Cum_Return_%"] = (df["IHSG_Base100"] - 100.0)
    
    # Relative Performance vs IHSG
    df["ICBP_vs_IHSG_Spread_%"] = df["ICBP_Cum_Return_%"] - df["IHSG_Cum_Return_%"]
    df["ICBP_IHSG_Ratio"] = df["ICBP_AdjClose"] / df["IHSG_Close"]
    
    # Moving Averages
    df["ICBP_SMA_20"] = df["ICBP_Close"].rolling(window=20).mean()
    df["ICBP_SMA_50"] = df["ICBP_Close"].rolling(window=50).mean()
    df["ICBP_SMA_200"] = df["ICBP_Close"].rolling(window=200).mean()
    
    # Average Trading Volume (20D and 30D)
    df["ICBP_Volume_SMA_20"] = df["ICBP_Volume"].rolling(window=20).mean()
    df["ICBP_Volume_SMA_30"] = df["ICBP_Volume"].rolling(window=30).mean()
    
    # 52-Week High and Low (Rolling 252 trading days)
    df["ICBP_52W_High"] = df["ICBP_High"].rolling(window=252, min_periods=1).max()
    df["ICBP_52W_Low"] = df["ICBP_Low"].rolling(window=252, min_periods=1).min()
    
    # 14-day RSI (Wilder's Exponential Smoothing)
    delta = df["ICBP_AdjClose"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["ICBP_RSI_14"] = 100.0 - (100.0 / (1.0 + rs))
    
    # MACD (12, 26, 9)
    ema_12 = df["ICBP_AdjClose"].ewm(span=12, adjust=False).mean()
    ema_26 = df["ICBP_AdjClose"].ewm(span=26, adjust=False).mean()
    df["ICBP_MACD_Line"] = ema_12 - ema_26
    df["ICBP_MACD_Signal"] = df["ICBP_MACD_Line"].ewm(span=9, adjust=False).mean()
    df["ICBP_MACD_Hist"] = df["ICBP_MACD_Line"] - df["ICBP_MACD_Signal"]
    
    # Rolling 30-day annualized volatility (252 trading days)
    df["ICBP_Vol_30D_Ann_%"] = (df["ICBP_Daily_Return_%"] / 100.0).rolling(window=30).std() * np.sqrt(252) * 100.0
    df["IHSG_Vol_30D_Ann_%"] = (df["IHSG_Daily_Return_%"] / 100.0).rolling(window=30).std() * np.sqrt(252) * 100.0
    
    # Rolling 252-day Beta vs IHSG
    cov_roll = (df["ICBP_Daily_Return_%"] / 100.0).rolling(252).cov(df["IHSG_Daily_Return_%"] / 100.0)
    var_roll = (df["IHSG_Daily_Return_%"] / 100.0).rolling(252).var()
    df["ICBP_Beta_1Y"] = cov_roll / var_roll
    
    # Maximum Drawdown (cumulative peak-to-trough drop %)
    cum_max = df["ICBP_AdjClose"].cummax()
    df["ICBP_Drawdown_%"] = ((df["ICBP_AdjClose"] - cum_max) / cum_max) * 100.0
    df["ICBP_Max_Drawdown_%"] = df["ICBP_Drawdown_%"].cummin()
    
    df.reset_index(inplace=True)
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    
    # Save daily datasets
    df.to_csv("data/processed/icbp_master_stock_market_daily.csv", index=False)
    df.to_csv("data/processed/stock_performance.csv", index=False)
    print("Master stock market daily series saved to data/processed/icbp_master_stock_market_daily.csv and stock_performance.csv")
    
    # -------------------------------------------------------------
    # Derive Monthly Returns Table
    # -------------------------------------------------------------
    df_date = df.copy()
    df_date["Date"] = pd.to_datetime(df_date["Date"])
    df_date.set_index("Date", inplace=True)
    
    monthly_icbp = df_date["ICBP_AdjClose"].resample("ME").last().pct_change() * 100.0
    monthly_ihsg = df_date["IHSG_Close"].resample("ME").last().pct_change() * 100.0
    monthly_vol = df_date["ICBP_Volume"].resample("ME").sum()
    
    monthly_df = pd.DataFrame({
        "Month": monthly_icbp.index.strftime("%Y-%m"),
        "ICBP_MonthEnd_Close": df_date["ICBP_Close"].resample("ME").last().values,
        "ICBP_Monthly_Return_%": monthly_icbp.values,
        "IHSG_Monthly_Return_%": monthly_ihsg.values,
        "ICBP_Monthly_Volume": monthly_vol.values
    }).dropna()
    monthly_df.to_csv("data/processed/icbp_monthly_returns_2010_2026.csv", index=False)
    print("Saved monthly returns to data/processed/icbp_monthly_returns_2010_2026.csv")
    
    # -------------------------------------------------------------
    # Derive Annual Returns Table
    # -------------------------------------------------------------
    annual_icbp = df_date["ICBP_AdjClose"].resample("YE").last().pct_change() * 100.0
    annual_ihsg = df_date["IHSG_Close"].resample("YE").last().pct_change() * 100.0
    annual_vol = df_date["ICBP_Volume"].resample("YE").sum()
    
    annual_df = pd.DataFrame({
        "Year": annual_icbp.index.year,
        "ICBP_YearEnd_Close": df_date["ICBP_Close"].resample("YE").last().values,
        "ICBP_Annual_Return_%": annual_icbp.values,
        "IHSG_Annual_Return_%": annual_ihsg.values,
        "Annual_Outperformance_%": annual_icbp.values - annual_ihsg.values,
        "ICBP_Annual_Volume": annual_vol.values
    }).dropna()
    annual_df.to_csv("data/processed/icbp_annual_returns_2010_2025.csv", index=False)
    print("Saved annual returns to data/processed/icbp_annual_returns_2010_2025.csv")
    
    # Print technical highlights
    latest = df.iloc[-1]
    print("\nLatest Stock Market Snapshot:")
    print(f"Date: {latest['Date']}")
    print(f"ICBP Close: Rp {latest['ICBP_Close']:,.0f}")
    print(f"14-Day RSI: {latest['ICBP_RSI_14']:.2f}")
    print(f"MACD (Line / Signal): {latest['ICBP_MACD_Line']:.2f} / {latest['ICBP_MACD_Signal']:.2f}")
    print(f"52-Week Range: Rp {latest['ICBP_52W_Low']:,.0f} - Rp {latest['ICBP_52W_High']:,.0f}")
    print(f"Current Drawdown from Peak: {latest['ICBP_Drawdown_%']:.2f}% (Max Drawdown: {latest['ICBP_Max_Drawdown_%']:.2f}%)")
    print(f"ICBP Cumulative Return: {latest['ICBP_Cum_Return_%']:.2f}% vs IHSG: {latest['IHSG_Cum_Return_%']:.2f}%")
    print(f"Latest 1-Year Beta vs IHSG: {latest['ICBP_Beta_1Y']:.2f}")

if __name__ == "__main__":
    scrape_stock_data()
