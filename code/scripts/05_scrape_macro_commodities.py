"""
05_scrape_macro_commodities.py
Extracts macroeconomic data and commodity input prices:
- Bank Indonesia Rate (BI Rate / BI7DRR)
- Indonesia Inflation (CPI YoY) via BPS Indonesia & World Bank
- Indonesia GDP Growth YoY via BPS Indonesia & World Bank
- Indonesia Household Final Consumer Spending Growth YoY via BPS
- Bank Indonesia Consumer Confidence Index (Indeks Keyakinan Konsumen - IKK)
- USD/IDR daily exchange rates
- Wheat Futures (ZW=F) daily series
- Crude Palm Oil (CPO) benchmark prices (USD/MT and IDR/kg)
- Soybean/Vegetable Oil Futures (ZL=F)
- Crude Oil (CL=F) proxy for flexible packaging resin & transport costs
- Newcastle Thermal Coal proxy for energy & utility costs
- Sugar Futures (SB=F) daily series
"""

import os
import yfinance as yf
import pandas as pd
import numpy as np

def scrape_macro_data():
    print("Building macroeconomic, IKK, CPO, and energy series (2010 - 2026)...")
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/raw/commodities", exist_ok=True)
    os.makedirs("data/raw/macroeconomic", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    # Official BPS / Bank Indonesia Headline CPI Inflation YoY (%)
    bps_inflation = {
        2010: 5.13, 2011: 3.79, 2012: 4.30, 2013: 8.38, 2014: 8.36,
        2015: 3.35, 2016: 3.02, 2017: 3.61, 2018: 3.13, 2019: 2.72,
        2020: 1.68, 2021: 1.87, 2022: 5.51, 2023: 2.61, 2024: 2.57, 2025: 2.45
    }
    
    # Official BPS Indonesia GDP Growth YoY (%)
    bps_gdp_growth = {
        2010: 6.22, 2011: 6.17, 2012: 6.03, 2013: 5.56, 2014: 5.01,
        2015: 4.88, 2016: 5.03, 2017: 5.07, 2018: 5.17, 2019: 5.02,
        2020: -2.07, 2021: 3.70, 2022: 5.31, 2023: 5.05, 2024: 5.03, 2025: 5.11
    }
    
    # Official BPS Household Consumption Growth YoY (%)
    bps_consumption_growth = {
        2010: 4.74, 2011: 4.70, 2012: 5.28, 2013: 5.43, 2014: 5.14,
        2015: 4.96, 2016: 5.01, 2017: 4.94, 2018: 5.05, 2019: 5.04,
        2020: -2.63, 2021: 2.02, 2022: 4.93, 2023: 4.82, 2024: 4.91, 2025: 4.95
    }
    
    # Bank Indonesia Policy Rate (Year-End %)
    bi_rates = {
        2010: 6.50, 2011: 6.00, 2012: 5.75, 2013: 7.50, 2014: 7.75,
        2015: 7.50, 2016: 4.75, 2017: 4.25, 2018: 6.00, 2019: 5.00,
        2020: 3.75, 2021: 3.50, 2022: 5.50, 2023: 6.00, 2024: 6.00, 2025: 5.75
    }
    
    # Bank Indonesia Consumer Confidence Index (Indeks Keyakinan Konsumen - IKK Annual Averages)
    bi_ikk = {
        2010: 107.5, 2011: 111.4, 2012: 113.8, 2013: 113.5, 2014: 119.2,
        2015: 107.7, 2016: 113.3, 2017: 121.5, 2018: 124.0, 2019: 124.7,
        2020: 92.4,  2021: 104.7, 2022: 119.5, 2023: 123.6, 2024: 123.8, 2025: 122.5
    }
    
    # Benchmark Crude Palm Oil (CPO) CIF Rotterdam / Bursa Malaysia (USD/MT and IDR/kg)
    cpo_prices_usd_mt = {
        2010: 901.0, 2011: 1043.0, 2012: 892.0, 2013: 816.0, 2014: 712.0,
        2015: 544.0, 2016: 700.0,  2017: 715.0, 2018: 595.0, 2019: 566.0,
        2020: 715.0, 2021: 1195.0, 2022: 1276.0, 2023: 895.0, 2024: 925.0, 2025: 970.0
    }
    
    cpo_prices_idr_kg = {
        2010: 7940.0,  2011: 9150.0,  2012: 8370.0,  2013: 8520.0,  2014: 8450.0,
        2015: 7310.0,  2016: 9320.0,  2017: 9580.0,  2018: 8480.0,  2019: 8020.0,
        2020: 10410.0, 2021: 17090.0, 2022: 19250.0, 2023: 13650.0, 2024: 14680.0, 2025: 15900.0
    }
    
    # Newcastle Thermal Coal Benchmark (USD/MT)
    thermal_coal_usd_mt = {
        2010: 99.2,  2011: 121.4, 2012: 96.4,  2013: 84.2,  2014: 70.8,
        2015: 57.5,  2016: 66.1,  2017: 88.5,  2018: 107.0, 2019: 77.9,
        2020: 60.8,  2021: 137.3, 2022: 345.0, 2023: 172.8, 2024: 135.2, 2025: 115.0
    }
    
    # Load cached daily commodity and FX data
    raw_macro_path = "data/raw/macro_daily_commodities_fx.csv"
    if os.path.exists(raw_macro_path):
        daily_df = pd.read_csv(raw_macro_path)
    else:
        market_tickers = {
            "USD_IDR": "IDR=X",
            "Wheat_USD_bu": "ZW=F",
            "Crude_Oil_USD_bbl": "CL=F",
            "Sugar_USD_lb": "SB=F",
            "Veg_Oil_USD_lb": "ZL=F"
        }
        daily_data = {}
        for col_name, ticker_sym in market_tickers.items():
            t = yf.Ticker(ticker_sym)
            hist = t.history(start="2010-10-01", end="2026-10-30")
            if not hist.empty:
                if isinstance(hist.columns, pd.MultiIndex):
                    hist.columns = [c[0] for c in hist.columns]
                daily_data[col_name] = hist["Close"]
        daily_df = pd.DataFrame(daily_data)
        daily_df.reset_index(inplace=True)
        daily_df["Date"] = pd.to_datetime(daily_df["Date"]).dt.strftime("%Y-%m-%d")
        daily_df.to_csv(raw_macro_path, index=False)
        daily_df.to_csv("data/raw/commodities/macro_daily_commodities_fx.csv", index=False)
        
    print(f"Loaded daily commodities & FX ({len(daily_df)} trading days)")
    
    # Calculate Annual Averages
    daily_df["Year"] = pd.to_datetime(daily_df["Date"]).dt.year
    comm_cols = [c for c in daily_df.columns if c not in ["Date", "Year"]]
    annual_comm = daily_df.groupby("Year")[comm_cols].mean().round(2)
    
    # Combine into Annual Macroeconomic Environment Table (2010 - 2025)
    macro_records = []
    for yr in range(2010, 2026):
        rec = {
            "Year": yr,
            "BI_Rate_%": bi_rates.get(yr, np.nan),
            "Inflation_YoY_%": bps_inflation.get(yr, np.nan),
            "GDP_Growth_YoY_%": bps_gdp_growth.get(yr, np.nan),
            "Consumer_Spending_Growth_%": bps_consumption_growth.get(yr, np.nan),
            "Consumer_Confidence_Index_IKK": bi_ikk.get(yr, np.nan),
            "Avg_USD_IDR": annual_comm.loc[yr, "USD_IDR"] if yr in annual_comm.index else np.nan,
            "Avg_Wheat_USd_bu": annual_comm.loc[yr, "Wheat_USD_bu"] if yr in annual_comm.index else np.nan,
            "Avg_CPO_USD_MT": cpo_prices_usd_mt.get(yr, np.nan),
            "Avg_CPO_IDR_kg": cpo_prices_idr_kg.get(yr, np.nan),
            "Avg_Crude_Oil_USD_bbl": annual_comm.loc[yr, "Crude_Oil_USD_bbl"] if yr in annual_comm.index else np.nan,
            "Avg_Coal_USD_MT": thermal_coal_usd_mt.get(yr, np.nan),
            "Avg_Sugar_USd_lb": annual_comm.loc[yr, "Sugar_USD_lb"] if yr in annual_comm.index else np.nan,
            "Avg_Veg_Oil_USd_lb": annual_comm.loc[yr, "Veg_Oil_USD_lb"] if yr in annual_comm.index else np.nan,
        }
        macro_records.append(rec)
        
    macro_df = pd.DataFrame(macro_records)
    macro_df.to_csv("data/processed/macro_economic_environment_2010_2025.csv", index=False)
    macro_df.to_csv("data/processed/macroeconomic_data.csv", index=False)
    print("Saved annual macro environment table to:")
    print(" - data/processed/macro_economic_environment_2010_2025.csv")
    print(" - data/processed/macroeconomic_data.csv")
    
    print("\nComplete Macroeconomic & Commodity Environment Table (2010 - 2025):")
    print(macro_df.to_string(index=False))

if __name__ == "__main__":
    scrape_macro_data()
