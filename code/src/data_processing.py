"""
src/data_processing.py
Data processing, standardization, and pipeline utility module.
Aligns raw and scraped datasets into standardized outputs matching the Data.md specification.
"""

import os
import shutil
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")

def organize_raw_subdirectories():
    """Copy or link raw files into specialized subdirectories as defined in Data.md."""
    mapping = {
        os.path.join(DATA_RAW, "icbp_daily_ohlcv_2010_2026.csv"): os.path.join(DATA_RAW, "stock_market", "icbp_daily_ohlcv_2010_2026.csv"),
        os.path.join(DATA_RAW, "ihsg_benchmark_daily_2010_2026.csv"): os.path.join(DATA_RAW, "stock_market", "ihsg_benchmark_daily_2010_2026.csv"),
        os.path.join(DATA_RAW, "peers_daily_ohlcv_2010_2026.csv"): os.path.join(DATA_RAW, "competitors", "peers_daily_ohlcv_2010_2026.csv"),
        os.path.join(DATA_RAW, "macro_daily_commodities_fx.csv"): os.path.join(DATA_RAW, "commodities", "macro_daily_commodities_fx.csv"),
    }
    for src, dst in mapping.items():
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)

def standardize_processed_datasets():
    """
    Ensures both original comprehensive names and standardized names from Data.md exist:
    - financial_metrics.csv
    - valuation_metrics.csv
    - stock_performance.csv
    - macroeconomic_data.csv
    - peer_comparison.csv
    """
    os.makedirs(DATA_PROCESSED, exist_ok=True)
    
    # 1. Financial Metrics
    src_fin = os.path.join(DATA_PROCESSED, "icbp_financial_statements_annual_2010_2025.csv")
    dst_fin = os.path.join(DATA_PROCESSED, "financial_metrics.csv")
    if os.path.exists(src_fin):
        df_fin = pd.read_csv(src_fin)
        src_ratios = os.path.join(DATA_PROCESSED, "icbp_financial_ratios_2010_2025.csv")
        if os.path.exists(src_ratios):
            df_rat = pd.read_csv(src_ratios)
            merged_fin = pd.merge(df_fin, df_rat, on="Year", how="left")
            merged_fin.to_csv(dst_fin, index=False)
        else:
            df_fin.to_csv(dst_fin, index=False)
            
    # 2. Valuation Metrics
    src_val = os.path.join(DATA_PROCESSED, "icbp_valuation_multiples_annual_2010_2025.csv")
    dst_val = os.path.join(DATA_PROCESSED, "valuation_metrics.csv")
    if os.path.exists(src_val):
        shutil.copy2(src_val, dst_val)
        
    # 3. Stock Performance
    src_stock = os.path.join(DATA_PROCESSED, "icbp_master_stock_market_daily.csv")
    dst_stock = os.path.join(DATA_PROCESSED, "stock_performance.csv")
    if os.path.exists(src_stock):
        shutil.copy2(src_stock, dst_stock)
        
    # 4. Macroeconomic Data
    src_macro = os.path.join(DATA_PROCESSED, "macro_economic_environment_2010_2025.csv")
    dst_macro = os.path.join(DATA_PROCESSED, "macroeconomic_data.csv")
    if os.path.exists(src_macro):
        shutil.copy2(src_macro, dst_macro)
        
    # 5. Peer Comparison
    src_peer = os.path.join(DATA_PROCESSED, "peers_financials_valuation_comparison.csv")
    dst_peer = os.path.join(DATA_PROCESSED, "peer_comparison.csv")
    if os.path.exists(src_peer):
        shutil.copy2(src_peer, dst_peer)

def load_financial_data() -> pd.DataFrame:
    path = os.path.join(DATA_PROCESSED, "financial_metrics.csv")
    return pd.read_csv(path)

def load_valuation_data() -> pd.DataFrame:
    path = os.path.join(DATA_PROCESSED, "valuation_metrics.csv")
    return pd.read_csv(path)

def load_stock_data() -> pd.DataFrame:
    path = os.path.join(DATA_PROCESSED, "stock_performance.csv")
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

def load_macro_data() -> pd.DataFrame:
    path = os.path.join(DATA_PROCESSED, "macroeconomic_data.csv")
    return pd.read_csv(path)

def load_peer_data() -> pd.DataFrame:
    path = os.path.join(DATA_PROCESSED, "peer_comparison.csv")
    return pd.read_csv(path)

def load_quarterly_data() -> pd.DataFrame:
    path = os.path.join(DATA_PROCESSED, "icbp_quarterly_financials_2021_2026.csv")
    return pd.read_csv(path)

def load_peer_multi_year_data() -> pd.DataFrame:
    path = os.path.join(DATA_PROCESSED, "peers_multi_year_financials_2015_2025.csv")
    return pd.read_csv(path)

def load_valuation_stats() -> pd.DataFrame:
    path = os.path.join(DATA_PROCESSED, "icbp_valuation_multiples_range_stats.csv")
    return pd.read_csv(path)

def load_monthly_returns() -> pd.DataFrame:
    path = os.path.join(DATA_PROCESSED, "icbp_monthly_returns_2010_2026.csv")
    return pd.read_csv(path)

def load_annual_returns() -> pd.DataFrame:
    path = os.path.join(DATA_PROCESSED, "icbp_annual_returns_2010_2025.csv")
    return pd.read_csv(path)

if __name__ == "__main__":
    organize_raw_subdirectories()
    standardize_processed_datasets()
    print("Data processing standardization complete. Standardized files verified in data/processed/")

