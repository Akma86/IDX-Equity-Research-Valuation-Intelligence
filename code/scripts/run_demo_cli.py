"""
code/scripts/run_demo_cli.py
Interactive CLI Demo & Valuation Intelligence Engine for PT Indofood CBP Sukses Makmur Tbk (ICBP)
Quick verification and terminal walkthrough of core valuation models, Pinehill metrics, and investment thesis.
"""

import sys
import os
import pandas as pd
import numpy as np

def run_cli_demo():
    print("=" * 80)
    print("  IDX EQUITY RESEARCH & VALUATION INTELLIGENCE SUITE: PT INDOFOOD CBP (ICBP)  ")
    print("=" * 80)
    print("  Institutional Coverage & Dynamic Valuation Model (Audited 2010 - 2026)      ")
    print("-" * 80)

    # 1. Load Datasets
    data_path = "results/data_tables/icbp_financial_statements_annual_2010_2025.csv"
    if not os.path.exists(data_path):
        data_path = "data/processed/icbp_financial_statements_annual_2010_2025.csv"
        
    df_annual = pd.read_csv(data_path)
    latest = df_annual.iloc[-1]
    ipo = df_annual.iloc[0]

    print("\n[1] 15-YEAR COMPOUNDING TRAJECTORY (IPO 2010 -> FY2025):")
    print(f"  * Revenue:           IDR {ipo['Revenue']:,.1f} B  -->  IDR {latest['Revenue']:,.1f} B  (CAGR: +9.98%)")
    print(f"  * Operating EBIT:    IDR {ipo['EBIT']:,.1f} B   -->  IDR {latest['EBIT']:,.1f} B  (CAGR: +13.35%)")
    print(f"  * Net Income:        IDR {ipo['NetIncome']:,.1f} B   -->  IDR {latest['NetIncome']:,.1f} B   (CAGR: +11.92%)")
    print(f"  * Operating Cash:    IDR {ipo['CFO']:,.1f} B   -->  IDR {latest['CFO']:,.1f} B  (CAGR: +11.86%)")
    print(f"  * Balance Sheet:     IDR {ipo['TotalAssets']:,.1f} B  -->  IDR {latest['TotalAssets']:,.1f} B (10.1x Expansion)")

    # 2. Pinehill Global Footprint
    print("\n[2] PINEHILL GLOBAL M&A TRANSFORMATION:")
    print("  * Acquisition: $3.0 Billion acquisition in Aug 2020 (8 Middle East & Africa plants)")
    print("  * Addressable Population: >885 Million consumers across MENA & Sub-Saharan Africa")
    print("  * Overseas Revenue Share: Surged from 10.8% (2019) to 32.1% (1H 2026)")
    print("  * Foreign Non-Current Assets: IDR 55.7 Trillion (65.0% of total non-current assets)")

    # 3. DCF Scenarios Summary
    print("\n[3] INTRINSIC VALUATION & FOOTBALL FIELD SUMMARY:")
    scenarios = [
        {"Scenario": "Bear Case (Stagnation)", "WACC": "8.80%", "g": "2.50%", "Target Price": "IDR 12,659", "Upside": "+119.2%", "Safety": "54.4%"},
        {"Scenario": "Base Case (Target Price)", "WACC": "8.10%", "g": "3.50%", "Target Price": "IDR 24,582", "Upside": "+325.7%", "Safety": "76.5%"},
        {"Scenario": "Bull Case (Expansion)",   "WACC": "7.40%", "g": "4.20%", "Target Price": "IDR 40,673", "Upside": "+604.3%", "Safety": "85.8%"},
    ]
    df_scen = pd.DataFrame(scenarios)
    print(df_scen.to_string(index=False))

    # 4. Peer Valuation Disconnect
    print("\n[4] CROSS-SECTIONAL PEER BENCHMARKING (IDX FMCG):")
    peers_path = "results/data_tables/peers_financials_valuation_comparison.csv"
    if not os.path.exists(peers_path):
        peers_path = "data/processed/peers_financials_valuation_comparison.csv"
    df_peers = pd.read_csv(peers_path)
    cols = ["Ticker", "Company_Name", "Operating_Margin_%", "ROIC_%", "P_E_Trailing_x", "EV_EBITDA_x", "Dividend_Yield_%"]
    print(df_peers[cols].to_string(index=False))

    print("\n" + "=" * 80)
    print("  RECOMMENDATION: CONVICTION BUY | TARGET PRICE: IDR 24,582 (+325.7% UPSIDE)")
    print("  LAUNCH STREAMLIT APP: streamlit run app.py")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    run_cli_demo()
