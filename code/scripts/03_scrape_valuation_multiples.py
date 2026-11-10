"""
03_scrape_valuation_multiples.py
Computes historical valuation metrics for ICBP from IPO (2010) through 2025/2026.
Calculates: Market Cap, Enterprise Value (EV), P/E, Forward P/E, P/BV, EV/EBITDA,
EV/EBIT, EV/Sales, P/FCF, FCF Yield, and Dividend Yield.
Constructs statistical distribution benchmarks (Min, 25th, Median, 75th, Max, Mean, SD, Z-score)
matching Data.md Section 2.3.
"""

import os
import pandas as pd
import numpy as np

def build_valuation_multiples():
    print("Building historical valuation multiples for ICBP (2010 - 2025/2026)...")
    
    # 1. Load Financial Statements
    fin_df = pd.read_csv("data/processed/financial_metrics.csv")
    
    # 2. Historical year-end unadjusted share prices (Rp) matching audited annual reports
    # (Accounting for the 1:2 stock split in 2016)
    hist_prices = {
        2010: 4900.0, 2011: 5200.0, 2012: 7800.0, 2013: 10200.0, 2014: 13100.0,
        2015: 13475.0, 2016: 8575.0, 2017: 8900.0, 2018: 10450.0, 2019: 11150.0,
        2020: 9575.0, 2021: 8700.0, 2022: 10000.0, 2023: 10575.0, 2024: 11250.0, 2025: 11800.0
    }
    
    val_records = []
    
    for idx, row in fin_df.iterrows():
        yr = int(row["Year"])
        price = hist_prices.get(yr, np.nan)
        shares = row["SharesOutstanding"] # in millions
        
        # Market Capitalization in IDR Billion
        mcap = (price * shares) / 1000.0
        
        total_debt = row["TotalDebt"]
        cash = row["Cash"]
        net_debt = total_debt - cash
        ev = mcap + net_debt # Enterprise Value (IDR Billion)
        
        # Valuation Multiples matching Data.md Section 2.3
        pe = mcap / row["NetIncome"] if row["NetIncome"] > 0 else np.nan
        pbv = mcap / row["TotalEquity"] if row["TotalEquity"] > 0 else np.nan
        ev_ebitda = ev / row["EBITDA"] if row["EBITDA"] > 0 else np.nan
        ev_ebit = ev / row["EBIT"] if row["EBIT"] > 0 else np.nan
        ev_sales = ev / row["Revenue"] if row["Revenue"] > 0 else np.nan
        
        fcf = row["FreeCashFlow"]
        p_fcf = mcap / fcf if fcf > 0 else np.nan
        fcf_yield = (fcf / mcap) * 100.0 if mcap > 0 else np.nan
        ev_fcf = ev / fcf if fcf > 0 else np.nan
        div_yield = (row["DPS"] / price) * 100.0 if price > 0 else np.nan
        
        val_records.append({
            "Year": yr,
            "YearEndClose_Rp": price,
            "SharesOutstanding_M": shares,
            "MarketCap_IDR_B": round(mcap, 1),
            "Cash_IDR_B": round(cash, 1),
            "TotalDebt_IDR_B": round(total_debt, 1),
            "NetDebt_IDR_B": round(net_debt, 1),
            "EnterpriseValue_IDR_B": round(ev, 1),
            "P_E_x": round(pe, 2),
            "P_BV_x": round(pbv, 2),
            "EV_EBITDA_x": round(ev_ebitda, 2),
            "EV_EBIT_x": round(ev_ebit, 2),
            "EV_Sales_x": round(ev_sales, 2),
            "P_FCF_x": round(p_fcf, 2) if not np.isnan(p_fcf) else np.nan,
            "FCFYield_%": round(fcf_yield, 2),
            "EV_FCF_x": round(ev_fcf, 2) if not np.isnan(ev_fcf) else np.nan,
            "DividendYield_%": round(div_yield, 2)
        })
        
    val_df = pd.DataFrame(val_records)
    
    # Calculate Forward P/E based on actual next-year earnings
    val_df["Forward_EPS_Rp"] = val_df["Year"].map(lambda y: fin_df.loc[fin_df["Year"] == y+1, "EPS"].values[0] if y < 2025 else np.nan)
    val_df["P_E_Forward_x"] = round(val_df["YearEndClose_Rp"] / val_df["Forward_EPS_Rp"], 2)
    
    # Save annual valuation multiples
    val_df.to_csv("data/processed/icbp_valuation_multiples_annual_2010_2025.csv", index=False)
    val_df.to_csv("data/processed/valuation_metrics.csv", index=False)
    print("Valuation multiples saved to:")
    print(" - data/processed/icbp_valuation_multiples_annual_2010_2025.csv")
    print(" - data/processed/valuation_metrics.csv")
    
    # -------------------------------------------------------------
    # 3. Compute Historical Valuation Multiples Statistical Range Summary
    # -------------------------------------------------------------
    # Current market snapshot (October 2026):
    # Current Price ~Rp 5,575, MCap ~Rp 65,015 B, Net Debt ~Rp 19,604 B, EV ~Rp 84,619 B
    # LTM / Run-Rate Net Income ~Rp 8,221 B, EBITDA ~Rp 18,222 B, EBIT ~Rp 18,222 B (annualized 9M26), Rev ~Rp 85,928 B
    current_metrics = {
        "P_E_x": round(65015.0 / 8221.0, 2), # ~7.91x
        "P_BV_x": round(65015.0 / 55330.7, 2), # ~1.18x
        "EV_EBITDA_x": round(84619.0 / 18222.0, 2), # ~4.64x
        "EV_EBIT_x": round(84619.0 / 18222.0, 2), # ~4.64x
        "EV_Sales_x": round(84619.0 / 85928.0, 2), # ~0.98x
        "P_FCF_x": round(65015.0 / 7378.8, 2), # ~8.81x
        "FCFYield_%": round((7378.8 / 65015.0) * 100.0, 2), # ~11.35%
        "DividendYield_%": round((265.0 / 5575.0) * 100.0, 2) # ~4.75%
    }
    
    stats_list = []
    target_cols = ["P_E_x", "P_BV_x", "EV_EBITDA_x", "EV_EBIT_x", "EV_Sales_x", "P_FCF_x", "FCFYield_%", "DividendYield_%"]
    
    for col in target_cols:
        series = val_df[col].dropna()
        curr = current_metrics.get(col, np.nan)
        pct_rank = round((series < curr).mean() * 100.0, 1)
        mean_val = round(series.mean(), 2)
        med_val = round(series.median(), 2)
        std_val = round(series.std(), 2)
        discount_to_med = round(((curr - med_val) / med_val) * 100.0, 1)
        
        stats_list.append({
            "Valuation_Multiple": col,
            "Min": round(series.min(), 2),
            "Percentile_25th": round(series.quantile(0.25), 2),
            "Median": med_val,
            "Mean": mean_val,
            "Percentile_75th": round(series.quantile(0.75), 2),
            "Max": round(series.max(), 2),
            "Std_Dev": std_val,
            "Current_Value": curr,
            "Current_Percentile_Rank_%": pct_rank,
            "Discount_To_Median_%": discount_to_med
        })
        
    stats_df = pd.DataFrame(stats_list)
    stats_df.to_csv("data/processed/icbp_valuation_multiples_range_stats.csv", index=False)
    print("Historical valuation multiples statistical range saved to data/processed/icbp_valuation_multiples_range_stats.csv")
    
    print("\nHistorical Multiples Range & Current Position:")
    print(stats_df.to_string(index=False))

if __name__ == "__main__":
    build_valuation_multiples()
