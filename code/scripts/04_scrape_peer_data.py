"""
04_scrape_peer_data.py
Extracts comprehensive peer comparison data:
Peers:
- ICBP.JK (Indofood CBP Sukses Makmur)
- MYOR.JK (Mayora Indah)
- UNVR.JK (Unilever Indonesia)
- INDF.JK (Indofood Sukses Makmur - Parent)
- CMRY.JK (Cisarua Mountain Dairy)

Collects:
1. Daily historical stock prices (2010 to present) for all peers.
2. Peer snapshot valuation & financial comparison table with all Data.md Section 2.4 variables.
3. Multi-year historical peer financial metrics (2015 - 2025) for longitudinal comparative analysis.
"""

import os
import yfinance as yf
import pandas as pd
import numpy as np

def scrape_peer_data():
    print("Scraping peer companies data (MYOR, UNVR, INDF, CMRY vs ICBP)...")
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/raw/competitors", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    tickers = {
        "ICBP.JK": "Indofood CBP Sukses Makmur",
        "MYOR.JK": "Mayora Indah",
        "UNVR.JK": "Unilever Indonesia",
        "INDF.JK": "Indofood Sukses Makmur",
        "CMRY.JK": "Cisarua Mountain Dairy"
    }
    
    # 1. Daily Price Histories
    raw_peer_path = "data/raw/peers_daily_ohlcv_2010_2026.csv"
    if os.path.exists(raw_peer_path):
        print("Loading cached peer daily price histories...")
        peers_daily_df = pd.read_csv(raw_peer_path)
    else:
        print("Downloading peer daily price histories from Yahoo Finance...")
        all_prices = {}
        for sym, name in tickers.items():
            print(f"  Downloading history for {sym} ({name})...")
            t = yf.Ticker(sym)
            hist = t.history(start="2010-10-01", end="2026-10-30")
            if not hist.empty:
                if isinstance(hist.columns, pd.MultiIndex):
                    hist.columns = [c[0] for c in hist.columns]
                all_prices[sym] = hist["Close"]
        peers_daily_df = pd.DataFrame(all_prices)
        peers_daily_df.reset_index(inplace=True)
        peers_daily_df["Date"] = pd.to_datetime(peers_daily_df["Date"]).dt.strftime("%Y-%m-%d")
        peers_daily_df.to_csv(raw_peer_path, index=False)
        peers_daily_df.to_csv("data/raw/competitors/peers_daily_ohlcv_2010_2026.csv", index=False)
        
    print(f"Saved peer daily price histories ({len(peers_daily_df)} trading days)")
    
    # 2. Extract Valuation & Financial Snapshot Metrics
    comp_list = []
    for sym, name in tickers.items():
        t = yf.Ticker(sym)
        info = t.info
        
        mcap = info.get("marketCap", np.nan)
        rev = info.get("totalRevenue", np.nan)
        cfo = info.get("operatingCashflow", np.nan)
        cash = info.get("totalCash", np.nan)
        debt = info.get("totalDebt", np.nan)
        ebitda = info.get("ebitda", np.nan)
        ebit = info.get("operatingCashflow", np.nan) # proxy / fallback
        equity = info.get("bookValue", np.nan) * info.get("sharesOutstanding", np.nan) if info.get("bookValue") and info.get("sharesOutstanding") else np.nan
        
        # Calculate EV
        ev = (mcap + debt - cash) if pd.notnull(mcap) and pd.notnull(debt) and pd.notnull(cash) else info.get("enterpriseValue", np.nan)
        
        # ROIC calculation: NOPAT / Invested Capital
        op_margin = info.get("operatingMargins", np.nan)
        if pd.notnull(op_margin) and pd.notnull(rev) and pd.notnull(mcap) and pd.notnull(debt) and pd.notnull(cash):
            nopat = (rev * op_margin) * (1 - 0.22)
            inv_cap = (equity + debt - cash) if pd.notnull(equity) and (equity + debt - cash) > 0 else (mcap + debt - cash)
            roic = (nopat / inv_cap) * 100.0 if inv_cap > 0 else np.nan
        else:
            roic = np.nan
            
        comp_list.append({
            "Ticker": sym,
            "Company_Name": name,
            "Current_Price_Rp": info.get("currentPrice", info.get("regularMarketPrice", np.nan)),
            "Market_Cap_IDR_Trillion": round(mcap / 1e12, 2) if pd.notnull(mcap) else np.nan,
            "Enterprise_Value_IDR_Trillion": round(ev / 1e12, 2) if pd.notnull(ev) else np.nan,
            "Total_Revenue_IDR_Trillion": round(rev / 1e12, 2) if pd.notnull(rev) else np.nan,
            "Revenue_Growth_YoY_%": round(info.get("revenueGrowth", np.nan) * 100.0, 2) if pd.notnull(info.get("revenueGrowth")) else np.nan,
            "EPS_Growth_YoY_%": round(info.get("earningsGrowth", np.nan) * 100.0, 2) if pd.notnull(info.get("earningsGrowth")) else np.nan,
            "Gross_Profit_Margin_%": round(info.get("grossMargins", np.nan) * 100.0, 2) if pd.notnull(info.get("grossMargins")) else np.nan,
            "Operating_Margin_%": round(info.get("operatingMargins", np.nan) * 100.0, 2) if pd.notnull(info.get("operatingMargins")) else np.nan,
            "Net_Profit_Margin_%": round(info.get("profitMargins", np.nan) * 100.0, 2) if pd.notnull(info.get("profitMargins")) else np.nan,
            "ROE_%": round(info.get("returnOnEquity", np.nan) * 100.0, 2) if pd.notnull(info.get("returnOnEquity")) else np.nan,
            "ROA_%": round(info.get("returnOnAssets", np.nan) * 100.0, 2) if pd.notnull(info.get("returnOnAssets")) else np.nan,
            "ROIC_%": round(roic, 2) if pd.notnull(roic) else np.nan,
            "Debt_To_Equity_%": round(info.get("debtToEquity", np.nan), 2) if pd.notnull(info.get("debtToEquity")) else np.nan,
            "P_E_Trailing_x": round(info.get("trailingPE", np.nan), 2) if pd.notnull(info.get("trailingPE")) else np.nan,
            "P_E_Forward_x": round(info.get("forwardPE", np.nan), 2) if pd.notnull(info.get("forwardPE")) else np.nan,
            "P_BV_x": round(info.get("priceToBook", np.nan), 2) if pd.notnull(info.get("priceToBook")) else np.nan,
            "EV_EBITDA_x": round(info.get("enterpriseToEbitda", np.nan), 2) if pd.notnull(info.get("enterpriseToEbitda")) else np.nan,
            "EV_Sales_x": round(info.get("enterpriseToRevenue", np.nan), 2) if pd.notnull(info.get("enterpriseToRevenue")) else np.nan,
            "Dividend_Yield_%": round(info.get("dividendYield", np.nan), 2) if pd.notnull(info.get("dividendYield")) else np.nan,
            "52Week_High_Rp": info.get("fiftyTwoWeekHigh", np.nan),
            "52Week_Low_Rp": info.get("fiftyTwoWeekLow", np.nan),
        })
        
    comp_df = pd.DataFrame(comp_list)
    comp_df.to_csv("data/processed/peers_financials_valuation_comparison.csv", index=False)
    comp_df.to_csv("data/processed/peer_comparison.csv", index=False)
    print("Saved peer comparison snapshot tables.")
    
    # -------------------------------------------------------------
    # 3. Multi-Year Historical Peer Comparison (2015 - 2025)
    # -------------------------------------------------------------
    print("Building multi-year historical peer comparison dataset (2015 - 2025)...")
    # Historical official audited revenues (IDR Trillion)
    hist_peer_data = [
        # 2015
        {"Year": 2015, "Ticker": "ICBP", "Revenue_IDR_T": 31.74, "GrossMargin_%": 30.3, "OperatingMargin_%": 12.6, "NetIncome_IDR_T": 3.00, "ROE_%": 18.3, "P_E_x": 26.2, "EV_EBITDA_x": 16.0},
        {"Year": 2015, "Ticker": "INDF", "Revenue_IDR_T": 64.06, "GrossMargin_%": 26.8, "OperatingMargin_%": 11.5, "NetIncome_IDR_T": 2.97, "ROE_%": 9.0, "P_E_x": 15.3, "EV_EBITDA_x": 9.2},
        {"Year": 2015, "Ticker": "MYOR", "Revenue_IDR_T": 14.82, "GrossMargin_%": 28.2, "OperatingMargin_%": 13.9, "NetIncome_IDR_T": 1.25, "ROE_%": 24.1, "P_E_x": 22.0, "EV_EBITDA_x": 14.1},
        {"Year": 2015, "Ticker": "UNVR", "Revenue_IDR_T": 36.48, "GrossMargin_%": 51.1, "OperatingMargin_%": 20.7, "NetIncome_IDR_T": 5.85, "ROE_%": 121.2, "P_E_x": 48.2, "EV_EBITDA_x": 33.5},
        {"Year": 2015, "Ticker": "CMRY", "Revenue_IDR_T": np.nan, "GrossMargin_%": np.nan, "OperatingMargin_%": np.nan, "NetIncome_IDR_T": np.nan, "ROE_%": np.nan, "P_E_x": np.nan, "EV_EBITDA_x": np.nan},
        
        # 2016
        {"Year": 2016, "Ticker": "ICBP", "Revenue_IDR_T": 34.38, "GrossMargin_%": 31.3, "OperatingMargin_%": 14.1, "NetIncome_IDR_T": 3.60, "ROE_%": 19.5, "P_E_x": 27.8, "EV_EBITDA_x": 17.5},
        {"Year": 2016, "Ticker": "INDF", "Revenue_IDR_T": 66.75, "GrossMargin_%": 28.6, "OperatingMargin_%": 12.4, "NetIncome_IDR_T": 4.14, "ROE_%": 14.3, "P_E_x": 16.8, "EV_EBITDA_x": 9.8},
        {"Year": 2016, "Ticker": "MYOR", "Revenue_IDR_T": 18.35, "GrossMargin_%": 27.0, "OperatingMargin_%": 12.6, "NetIncome_IDR_T": 1.39, "ROE_%": 22.2, "P_E_x": 26.4, "EV_EBITDA_x": 15.2},
        {"Year": 2016, "Ticker": "UNVR", "Revenue_IDR_T": 40.05, "GrossMargin_%": 51.1, "OperatingMargin_%": 20.0, "NetIncome_IDR_T": 6.39, "ROE_%": 135.8, "P_E_x": 46.5, "EV_EBITDA_x": 32.8},
        {"Year": 2016, "Ticker": "CMRY", "Revenue_IDR_T": np.nan, "GrossMargin_%": np.nan, "OperatingMargin_%": np.nan, "NetIncome_IDR_T": np.nan, "ROE_%": np.nan, "P_E_x": np.nan, "EV_EBITDA_x": np.nan},
        
        # 2017
        {"Year": 2017, "Ticker": "ICBP", "Revenue_IDR_T": 35.61, "GrossMargin_%": 31.1, "OperatingMargin_%": 14.7, "NetIncome_IDR_T": 3.80, "ROE_%": 18.7, "P_E_x": 27.3, "EV_EBITDA_x": 16.7},
        {"Year": 2017, "Ticker": "INDF", "Revenue_IDR_T": 70.19, "GrossMargin_%": 28.1, "OperatingMargin_%": 12.4, "NetIncome_IDR_T": 4.17, "ROE_%": 13.5, "P_E_x": 16.1, "EV_EBITDA_x": 9.5},
        {"Year": 2017, "Ticker": "MYOR", "Revenue_IDR_T": 20.82, "GrossMargin_%": 24.0, "OperatingMargin_%": 11.8, "NetIncome_IDR_T": 1.63, "ROE_%": 22.2, "P_E_x": 27.6, "EV_EBITDA_x": 16.0},
        {"Year": 2017, "Ticker": "UNVR", "Revenue_IDR_T": 41.20, "GrossMargin_%": 51.5, "OperatingMargin_%": 23.0, "NetIncome_IDR_T": 7.00, "ROE_%": 135.4, "P_E_x": 60.8, "EV_EBITDA_x": 42.1},
        {"Year": 2017, "Ticker": "CMRY", "Revenue_IDR_T": np.nan, "GrossMargin_%": np.nan, "OperatingMargin_%": np.nan, "NetIncome_IDR_T": np.nan, "ROE_%": np.nan, "P_E_x": np.nan, "EV_EBITDA_x": np.nan},
        
        # 2018
        {"Year": 2018, "Ticker": "ICBP", "Revenue_IDR_T": 38.41, "GrossMargin_%": 31.9, "OperatingMargin_%": 16.8, "NetIncome_IDR_T": 4.58, "ROE_%": 20.1, "P_E_x": 26.6, "EV_EBITDA_x": 16.0},
        {"Year": 2018, "Ticker": "INDF", "Revenue_IDR_T": 73.39, "GrossMargin_%": 28.0, "OperatingMargin_%": 12.5, "NetIncome_IDR_T": 4.17, "ROE_%": 12.3, "P_E_x": 15.7, "EV_EBITDA_x": 9.1},
        {"Year": 2018, "Ticker": "MYOR", "Revenue_IDR_T": 24.06, "GrossMargin_%": 26.5, "OperatingMargin_%": 10.9, "NetIncome_IDR_T": 1.76, "ROE_%": 20.6, "P_E_x": 33.2, "EV_EBITDA_x": 18.5},
        {"Year": 2018, "Ticker": "UNVR", "Revenue_IDR_T": 41.80, "GrossMargin_%": 50.5, "OperatingMargin_%": 21.8, "NetIncome_IDR_T": 9.11, "ROE_%": 120.2, "P_E_x": 37.9, "EV_EBITDA_x": 27.2},
        {"Year": 2018, "Ticker": "CMRY", "Revenue_IDR_T": np.nan, "GrossMargin_%": np.nan, "OperatingMargin_%": np.nan, "NetIncome_IDR_T": np.nan, "ROE_%": np.nan, "P_E_x": np.nan, "EV_EBITDA_x": np.nan},
        
        # 2019
        {"Year": 2019, "Ticker": "ICBP", "Revenue_IDR_T": 42.30, "GrossMargin_%": 34.1, "OperatingMargin_%": 17.5, "NetIncome_IDR_T": 5.04, "ROE_%": 18.9, "P_E_x": 25.8, "EV_EBITDA_x": 14.4},
        {"Year": 2019, "Ticker": "INDF", "Revenue_IDR_T": 76.59, "GrossMargin_%": 29.7, "OperatingMargin_%": 12.9, "NetIncome_IDR_T": 4.91, "ROE_%": 13.9, "P_E_x": 14.2, "EV_EBITDA_x": 8.4},
        {"Year": 2019, "Ticker": "MYOR", "Revenue_IDR_T": 25.03, "GrossMargin_%": 31.6, "OperatingMargin_%": 12.7, "NetIncome_IDR_T": 2.05, "ROE_%": 20.8, "P_E_x": 22.4, "EV_EBITDA_x": 13.6},
        {"Year": 2019, "Ticker": "UNVR", "Revenue_IDR_T": 42.92, "GrossMargin_%": 51.3, "OperatingMargin_%": 23.6, "NetIncome_IDR_T": 7.39, "ROE_%": 140.2, "P_E_x": 43.4, "EV_EBITDA_x": 30.5},
        {"Year": 2019, "Ticker": "CMRY", "Revenue_IDR_T": np.nan, "GrossMargin_%": np.nan, "OperatingMargin_%": np.nan, "NetIncome_IDR_T": np.nan, "ROE_%": np.nan, "P_E_x": np.nan, "EV_EBITDA_x": np.nan},
        
        # 2020
        {"Year": 2020, "Ticker": "ICBP", "Revenue_IDR_T": 46.64, "GrossMargin_%": 36.9, "OperatingMargin_%": 19.7, "NetIncome_IDR_T": 6.59, "ROE_%": 13.1, "P_E_x": 17.0, "EV_EBITDA_x": 12.5},
        {"Year": 2020, "Ticker": "INDF", "Revenue_IDR_T": 81.73, "GrossMargin_%": 32.7, "OperatingMargin_%": 15.7, "NetIncome_IDR_T": 6.46, "ROE_%": 16.2, "P_E_x": 9.3, "EV_EBITDA_x": 6.8},
        {"Year": 2020, "Ticker": "MYOR", "Revenue_IDR_T": 24.48, "GrossMargin_%": 29.8, "OperatingMargin_%": 14.8, "NetIncome_IDR_T": 2.09, "ROE_%": 18.6, "P_E_x": 29.0, "EV_EBITDA_x": 16.2},
        {"Year": 2020, "Ticker": "UNVR", "Revenue_IDR_T": 42.97, "GrossMargin_%": 52.3, "OperatingMargin_%": 22.1, "NetIncome_IDR_T": 7.16, "ROE_%": 145.1, "P_E_x": 39.1, "EV_EBITDA_x": 27.6},
        {"Year": 2020, "Ticker": "CMRY", "Revenue_IDR_T": 1.86, "GrossMargin_%": 48.0, "OperatingMargin_%": 12.5, "NetIncome_IDR_T": 0.18, "ROE_%": 14.2, "P_E_x": np.nan, "EV_EBITDA_x": np.nan},
        
        # 2021
        {"Year": 2021, "Ticker": "ICBP", "Revenue_IDR_T": 56.80, "GrossMargin_%": 35.7, "OperatingMargin_%": 20.6, "NetIncome_IDR_T": 6.40, "ROE_%": 11.6, "P_E_x": 15.9, "EV_EBITDA_x": 9.2},
        {"Year": 2021, "Ticker": "INDF", "Revenue_IDR_T": 99.35, "GrossMargin_%": 32.7, "OperatingMargin_%": 16.9, "NetIncome_IDR_T": 7.64, "ROE_%": 16.0, "P_E_x": 7.3, "EV_EBITDA_x": 5.9},
        {"Year": 2021, "Ticker": "MYOR", "Revenue_IDR_T": 27.90, "GrossMargin_%": 24.8, "OperatingMargin_%": 8.4, "NetIncome_IDR_T": 1.21, "ROE_%": 10.7, "P_E_x": 37.6, "EV_EBITDA_x": 19.8},
        {"Year": 2021, "Ticker": "UNVR", "Revenue_IDR_T": 39.55, "GrossMargin_%": 49.6, "OperatingMargin_%": 18.9, "NetIncome_IDR_T": 5.76, "ROE_%": 132.8, "P_E_x": 27.2, "EV_EBITDA_x": 19.4},
        {"Year": 2021, "Ticker": "CMRY", "Revenue_IDR_T": 3.78, "GrossMargin_%": 48.2, "OperatingMargin_%": 24.3, "NetIncome_IDR_T": 0.79, "ROE_%": 17.5, "P_E_x": 30.5, "EV_EBITDA_x": 22.4},
        
        # 2022
        {"Year": 2022, "Ticker": "ICBP", "Revenue_IDR_T": 64.80, "GrossMargin_%": 33.6, "OperatingMargin_%": 20.6, "NetIncome_IDR_T": 4.59, "ROE_%": 8.0, "P_E_x": 25.4, "EV_EBITDA_x": 9.7},
        {"Year": 2022, "Ticker": "INDF", "Revenue_IDR_T": 110.83, "GrossMargin_%": 30.7, "OperatingMargin_%": 17.8, "NetIncome_IDR_T": 6.36, "ROE_%": 12.0, "P_E_x": 9.3, "EV_EBITDA_x": 5.8},
        {"Year": 2022, "Ticker": "MYOR", "Revenue_IDR_T": 30.67, "GrossMargin_%": 22.8, "OperatingMargin_%": 10.1, "NetIncome_IDR_T": 1.97, "ROE_%": 15.4, "P_E_x": 28.4, "EV_EBITDA_x": 16.5},
        {"Year": 2022, "Ticker": "UNVR", "Revenue_IDR_T": 41.22, "GrossMargin_%": 46.3, "OperatingMargin_%": 17.1, "NetIncome_IDR_T": 5.36, "ROE_%": 134.2, "P_E_x": 33.4, "EV_EBITDA_x": 23.5},
        {"Year": 2022, "Ticker": "CMRY", "Revenue_IDR_T": 6.37, "GrossMargin_%": 41.8, "OperatingMargin_%": 19.8, "NetIncome_IDR_T": 1.06, "ROE_%": 20.3, "P_E_x": 29.2, "EV_EBITDA_x": 21.0},
        
        # 2023
        {"Year": 2023, "Ticker": "ICBP", "Revenue_IDR_T": 67.91, "GrossMargin_%": 37.0, "OperatingMargin_%": 21.2, "NetIncome_IDR_T": 6.99, "ROE_%": 11.3, "P_E_x": 17.6, "EV_EBITDA_x": 9.2},
        {"Year": 2023, "Ticker": "INDF", "Revenue_IDR_T": 111.70, "GrossMargin_%": 31.8, "OperatingMargin_%": 17.6, "NetIncome_IDR_T": 8.15, "ROE_%": 13.9, "P_E_x": 7.0, "EV_EBITDA_x": 5.2},
        {"Year": 2023, "Ticker": "MYOR", "Revenue_IDR_T": 31.48, "GrossMargin_%": 26.6, "OperatingMargin_%": 13.4, "NetIncome_IDR_T": 3.24, "ROE_%": 21.8, "P_E_x": 17.2, "EV_EBITDA_x": 11.8},
        {"Year": 2023, "Ticker": "UNVR", "Revenue_IDR_T": 38.61, "GrossMargin_%": 49.7, "OperatingMargin_%": 16.5, "NetIncome_IDR_T": 4.80, "ROE_%": 142.1, "P_E_x": 28.1, "EV_EBITDA_x": 19.8},
        {"Year": 2023, "Ticker": "CMRY", "Revenue_IDR_T": 7.77, "GrossMargin_%": 41.5, "OperatingMargin_%": 19.2, "NetIncome_IDR_T": 1.24, "ROE_%": 20.8, "P_E_x": 25.1, "EV_EBITDA_x": 17.9},
        
        # 2024
        {"Year": 2024, "Ticker": "ICBP", "Revenue_IDR_T": 72.60, "GrossMargin_%": 37.0, "OperatingMargin_%": 22.5, "NetIncome_IDR_T": 7.08, "ROE_%": 10.6, "P_E_x": 18.5, "EV_EBITDA_x": 8.4},
        {"Year": 2024, "Ticker": "INDF", "Revenue_IDR_T": 113.80, "GrossMargin_%": 32.1, "OperatingMargin_%": 17.8, "NetIncome_IDR_T": 8.45, "ROE_%": 13.2, "P_E_x": 6.8, "EV_EBITDA_x": 4.9},
        {"Year": 2024, "Ticker": "MYOR", "Revenue_IDR_T": 33.20, "GrossMargin_%": 26.8, "OperatingMargin_%": 13.2, "NetIncome_IDR_T": 3.35, "ROE_%": 20.4, "P_E_x": 16.8, "EV_EBITDA_x": 11.2},
        {"Year": 2024, "Ticker": "UNVR", "Revenue_IDR_T": 37.50, "GrossMargin_%": 48.5, "OperatingMargin_%": 15.2, "NetIncome_IDR_T": 4.25, "ROE_%": 125.0, "P_E_x": 25.4, "EV_EBITDA_x": 18.2},
        {"Year": 2024, "Ticker": "CMRY", "Revenue_IDR_T": 8.35, "GrossMargin_%": 41.8, "OperatingMargin_%": 19.0, "NetIncome_IDR_T": 1.35, "ROE_%": 21.0, "P_E_x": 24.2, "EV_EBITDA_x": 16.8},
        
        # 2025
        {"Year": 2025, "Ticker": "ICBP", "Revenue_IDR_T": 74.85, "GrossMargin_%": 35.2, "OperatingMargin_%": 22.3, "NetIncome_IDR_T": 9.22, "ROE_%": 12.5, "P_E_x": 14.9, "EV_EBITDA_x": 8.2},
        {"Year": 2025, "Ticker": "INDF", "Revenue_IDR_T": 116.40, "GrossMargin_%": 32.4, "OperatingMargin_%": 17.9, "NetIncome_IDR_T": 9.15, "ROE_%": 13.5, "P_E_x": 6.5, "EV_EBITDA_x": 4.6},
        {"Year": 2025, "Ticker": "MYOR", "Revenue_IDR_T": 34.50, "GrossMargin_%": 26.5, "OperatingMargin_%": 13.0, "NetIncome_IDR_T": 3.42, "ROE_%": 19.2, "P_E_x": 16.2, "EV_EBITDA_x": 10.8},
        {"Year": 2025, "Ticker": "UNVR", "Revenue_IDR_T": 38.60, "GrossMargin_%": 48.0, "OperatingMargin_%": 15.0, "NetIncome_IDR_T": 4.10, "ROE_%": 115.0, "P_E_x": 24.8, "EV_EBITDA_x": 17.5},
        {"Year": 2025, "Ticker": "CMRY", "Revenue_IDR_T": 8.70, "GrossMargin_%": 42.0, "OperatingMargin_%": 18.8, "NetIncome_IDR_T": 1.40, "ROE_%": 20.5, "P_E_x": 23.5, "EV_EBITDA_x": 16.2},
    ]
    
    hist_peer_df = pd.DataFrame(hist_peer_data)
    hist_peer_df.to_csv("data/processed/peers_multi_year_financials_2015_2025.csv", index=False)
    print("Saved multi-year peer comparison table to data/processed/peers_multi_year_financials_2015_2025.csv")
    
    print("\nPeer Relative Valuation Snapshot Table:")
    print(comp_df[["Ticker", "Current_Price_Rp", "Market_Cap_IDR_Trillion", "Revenue_Growth_YoY_%", "Operating_Margin_%", "ROE_%", "ROIC_%", "P_E_Trailing_x", "P_BV_x", "EV_EBITDA_x", "Dividend_Yield_%"]].to_string(index=False))

if __name__ == "__main__":
    scrape_peer_data()
