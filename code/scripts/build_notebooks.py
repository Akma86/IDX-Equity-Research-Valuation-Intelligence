"""
scripts/build_notebooks.py
Generates the 7 professional Jupyter Notebooks specified in Data.md section 5,
fully updated with all audited financial metrics, quarterly interim progression,
technical indicators (RSI, MACD, Drawdown), peer multi-year history, and macro/commodity indicators.
"""

import os
import nbformat as nbf

NOTEBOOKS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notebooks")
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)

def create_notebook(filename, title, description, code_cells):
    nb = nbf.v4.new_notebook()
    nb.cells = []
    
    # Title & Metadata cell
    header_md = f"""# {title}
**Project:** IDX Equity Research & Valuation Intelligence  
**Target Entity:** PT Indofood CBP Sukses Makmur Tbk (IDX: ICBP)  
**Description:** {description}
"""
    nb.cells.append(nbf.v4.new_markdown_cell(header_md))
    
    # Add cells
    for item in code_cells:
        if item["type"] == "md":
            nb.cells.append(nbf.v4.new_markdown_cell(item["content"]))
        elif item["type"] == "code":
            nb.cells.append(nbf.v4.new_code_cell(item["content"]))
            
    filepath = os.path.join(NOTEBOOKS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Generated: {filepath}")

def build_all_notebooks():
    # -------------------------------------------------------------------------
    # Notebook 1: Data Collection & Integrity
    # -------------------------------------------------------------------------
    create_notebook(
        "01_data_collection.ipynb",
        "01. Data Collection & Integrity Verification",
        "Pipeline for auditing, loading, and verifying all six raw and processed data groups spanning from IPO (2010) through 2025/2026, including 9M26 interim data.",
        [
            {"type": "md", "content": "## 1. Setup & Environment Verification"},
            {"type": "code", "content": """import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.abspath('../src'))
from data_processing import (
    load_financial_data,
    load_valuation_data,
    load_stock_data,
    load_macro_data,
    load_peer_data,
    load_quarterly_data,
    load_peer_multi_year_data,
    load_valuation_stats
)

print("Environment & Modules successfully imported!")"""},
            {"type": "md", "content": "## 2. Load & Inspect Financial Statements Data (2010 - 2025)"},
            {"type": "code", "content": """df_fin = load_financial_data()
print(f"Financial Statements Shape: {df_fin.shape}")
df_fin[['Year', 'Revenue', 'GrossProfit', 'EBIT', 'NetIncome', 'Cash', 'TotalDebt', 'TotalAssets', 'TotalEquity', 'CurrentAssets', 'CurrentLiabilities', 'CFO', 'Capex', 'CFI', 'CFF']].tail(10)"""},
            {"type": "md", "content": "## 3. Load & Inspect Quarterly / Interim Progression (2021 - 2026, incl 9M26)"},
            {"type": "code", "content": """df_q = load_quarterly_data()
print(f"Quarterly records: {len(df_q)} periods")
display(df_q.tail(7))"""},
            {"type": "md", "content": "## 4. Load & Inspect Daily Stock Market Series (3,950+ Days & Technical Indicators)"},
            {"type": "code", "content": """df_stock = load_stock_data()
print(f"Daily Stock Records: {len(df_stock)} from {df_stock['Date'].min().strftime('%Y-%m-%d')} to {df_stock['Date'].max().strftime('%Y-%m-%d')}")
display(df_stock[['Date', 'ICBP_Close', 'ICBP_AdjClose', 'ICBP_Volume', 'ICBP_SMA_50', 'ICBP_SMA_200', 'ICBP_RSI_14', 'ICBP_MACD_Line', 'ICBP_Drawdown_%']].tail(5))"""},
            {"type": "md", "content": "## 5. Load & Inspect Macroeconomic, CPO, Coal, and Peer Datasets"},
            {"type": "code", "content": """df_macro = load_macro_data()
df_peer = load_peer_data()
df_peer_multi = load_peer_multi_year_data()

print("--- Macroeconomic Indicators (Recent Years) ---")
display(df_macro[['Year', 'BI_Rate_%', 'Inflation_YoY_%', 'GDP_Growth_YoY_%', 'Consumer_Confidence_Index_IKK', 'Avg_USD_IDR', 'Avg_Wheat_USd_bu', 'Avg_CPO_USD_MT', 'Avg_Coal_USD_MT']].tail(5))

print("--- Peer Comparison Snapshot ---")
display(df_peer[['Ticker', 'Company_Name', 'Market_Cap_IDR_Trillion', 'Revenue_Growth_YoY_%', 'Operating_Margin_%', 'ROE_%', 'ROIC_%', 'P_E_Trailing_x', 'EV_EBITDA_x']])"""}
        ]
    )

    # -------------------------------------------------------------------------
    # Notebook 2: Financial Analysis
    # -------------------------------------------------------------------------
    create_notebook(
        "02_financial_analysis.ipynb",
        "02. Financial Statement & Profitability Analysis",
        "Detailed examination of revenue trends, gross and operating margins, capital efficiency, DuPont decomposition, and cash conversion.",
        [
            {"type": "md", "content": "## 1. Import Modules and Compute Derived Financial Metrics"},
            {"type": "code", "content": """import sys, os
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath('../src'))
from data_processing import load_financial_data, load_quarterly_data
from financial_metrics import calculate_derived_financial_metrics, get_growth_cagrs

df = load_financial_data()
metrics = calculate_derived_financial_metrics(df)
cagrs = get_growth_cagrs(df)

display(cagrs)"""},
            {"type": "md", "content": "## 2. Profitability Margins & Historical Evolution"},
            {"type": "code", "content": """margin_cols = ['Year', 'Revenue', 'Gross_Margin_%', 'EBIT_Margin_%', 'EBITDA_Margin_%', 'Net_Margin_%']
metrics[margin_cols].tail(10)"""},
            {"type": "md", "content": "## 3. Return on Capital & DuPont Analysis (3-Way)"},
            {"type": "code", "content": """dupont_cols = ['Year', 'Net_Margin_%', 'Asset_Turnover_x', 'Equity_Multiplier_x', 'DuPont_ROE_%', 'ROIC_%', 'ROA_%']
metrics[dupont_cols].tail(10)"""},
            {"type": "md", "content": "## 4. Liquidity & Solvency Structure (Current Ratio & Leverage)"},
            {"type": "code", "content": """solv_cols = ['Year', 'CurrentAssets', 'CurrentLiabilities', 'Current_Ratio_x', 'NetWorkingCapital', 'Debt_to_Equity_x', 'Net_Debt_to_EBITDA_x']
metrics[solv_cols].tail(10)"""},
            {"type": "md", "content": "## 5. Cash Generation & Free Cash Flow Quality"},
            {"type": "code", "content": """fcf_cols = ['Year', 'CFO', 'Capex', 'FreeCashFlow', 'FCF_Margin_%', 'CFO_to_NetIncome_x', 'FCF_Conversion_%']
metrics[fcf_cols].tail(10)"""}
        ]
    )

    # -------------------------------------------------------------------------
    # Notebook 3: Stock Performance
    # -------------------------------------------------------------------------
    create_notebook(
        "03_stock_performance.ipynb",
        "03. Stock Market & Relative Performance Analysis",
        "Historical return analysis, benchmark comparison vs IHSG, volatility, RSI, MACD, drawdowns, and rolling systematic risk (beta).",
        [
            {"type": "md", "content": "## 1. Load Daily Stock Performance Data"},
            {"type": "code", "content": """import sys, os
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath('../src'))
from data_processing import load_stock_data, load_monthly_returns, load_annual_returns

stock_df = load_stock_data()
stock_df.set_index('Date', inplace=True)
stock_df[['ICBP_Close', 'IHSG_Close', 'ICBP_Cum_Return_%', 'IHSG_Cum_Return_%', 'ICBP_SMA_50', 'ICBP_SMA_200', 'ICBP_RSI_14', 'ICBP_Beta_1Y', 'ICBP_Drawdown_%']].tail(10)"""},
            {"type": "md", "content": "## 2. Technical Profile: RSI, MACD & 52-Week Range"},
            {"type": "code", "content": """latest = stock_df.iloc[-1]
print(f"Latest ICBP Close: Rp {latest['ICBP_Close']:,.0f}")
print(f"14-Day RSI: {latest['ICBP_RSI_14']:.2f}")
print(f"MACD Line: {latest['ICBP_MACD_Line']:.2f} | Signal: {latest['ICBP_MACD_Signal']:.2f}")
print(f"52-Week Range: Rp {latest['ICBP_52W_Low']:,.0f} - Rp {latest['ICBP_52W_High']:,.0f}")
print(f"Drawdown from Peak: {latest['ICBP_Drawdown_%']:.2f}% (Max Historical: {latest['ICBP_Max_Drawdown_%']:.2f}%)")"""},
            {"type": "md", "content": "## 3. Annual & Monthly Return Aggregation"},
            {"type": "code", "content": """ann_df = load_annual_returns()
display(ann_df.tail(10))"""}
        ]
    )

    # -------------------------------------------------------------------------
    # Notebook 4: Peer Comparison
    # -------------------------------------------------------------------------
    create_notebook(
        "04_peer_comparison.ipynb",
        "04. Peer Benchmark & Relative Valuation",
        "Multi-company comparative analysis against Indonesian FMCG leaders: MYOR, UNVR, INDF, and CMRY across cross-sectional snapshot and multi-year history.",
        [
            {"type": "md", "content": "## 1. Load Peer Comparison Snapshot"},
            {"type": "code", "content": """import sys, os
import pandas as pd

sys.path.append(os.path.abspath('../src'))
from data_processing import load_peer_data, load_peer_multi_year_data

peers = load_peer_data()
display(peers[['Ticker', 'Company_Name', 'Market_Cap_IDR_Trillion', 'Revenue_Growth_YoY_%', 'Operating_Margin_%', 'ROE_%', 'ROIC_%', 'P_E_Trailing_x', 'P_BV_x', 'EV_EBITDA_x', 'Dividend_Yield_%']])"""},
            {"type": "md", "content": "## 2. Multi-Year Longitudinal Peer Financial Evolution (2015 - 2025)"},
            {"type": "code", "content": """peers_multi = load_peer_multi_year_data()
display(peers_multi.tail(15))"""}
        ]
    )

    # -------------------------------------------------------------------------
    # Notebook 5: Macro Analysis
    # -------------------------------------------------------------------------
    create_notebook(
        "05_macro_analysis.ipynb",
        "05. Macroeconomic Dynamics & Commodity Sensitivity",
        "Analysis of Bank Indonesia interest rate cycles, inflation, Consumer Confidence Index (IKK), USD/IDR exchange rates, and input commodity prices (Wheat, CPO, Oil, Coal).",
        [
            {"type": "md", "content": "## 1. Load Macroeconomic & Commodity Environment Data"},
            {"type": "code", "content": """import sys, os
import pandas as pd

sys.path.append(os.path.abspath('../src'))
from data_processing import load_macro_data, load_financial_data

macro_df = load_macro_data()
fin_df = load_financial_data()
merged = pd.merge(macro_df, fin_df[['Year', 'GrossProfit', 'Revenue', 'EBIT']], on='Year')
merged['Gross_Margin_%'] = (merged['GrossProfit'] / merged['Revenue']) * 100.0
display(merged[['Year', 'BI_Rate_%', 'Inflation_YoY_%', 'GDP_Growth_YoY_%', 'Consumer_Confidence_Index_IKK', 'Avg_USD_IDR', 'Avg_Wheat_USd_bu', 'Avg_CPO_USD_MT', 'Avg_Coal_USD_MT', 'Gross_Margin_%']])"""},
            {"type": "md", "content": "## 2. Input Cost Sensitivity: Correlation with Margins"},
            {"type": "code", "content": """corr = merged[['Gross_Margin_%', 'Avg_Wheat_USd_bu', 'Avg_CPO_USD_MT', 'Avg_Crude_Oil_USD_bbl', 'Avg_Coal_USD_MT', 'Avg_USD_IDR', 'Inflation_YoY_%']].corr()
print("--- Correlation Matrix with ICBP Gross Margin ---")
display(corr[['Gross_Margin_%']])"""}
        ]
    )

    # -------------------------------------------------------------------------
    # Notebook 6: Valuation Analysis (DCF & Historical Multiples)
    # -------------------------------------------------------------------------
    create_notebook(
        "06_valuation_analysis.ipynb",
        "06. Intrinsic DCF Modeling & Historical Valuation Multiples",
        "Comprehensive Discounted Cash Flow (DCF) model across Bear, Base, and Bull scenarios with historical multiples percentile trading range.",
        [
            {"type": "md", "content": "## 1. Historical Valuation Multiples Trading Range"},
            {"type": "code", "content": """import sys, os
import pandas as pd

sys.path.append(os.path.abspath('../src'))
from data_processing import load_valuation_data, load_valuation_stats
from valuation import DCFValuationModel

val_df = load_valuation_data()
stats_df = load_valuation_stats()

print("=== 16-Year Valuation Multiples Statistical Range Summary ===")
display(stats_df)"""},
            {"type": "md", "content": "## 2. DCF Valuation Model Execution (3 Scenarios)"},
            {"type": "code", "content": """dcf = DCFValuationModel()
results = dcf.run_all_scenarios()

print("=== DCF SCENARIOS SUMMARY TABLE ===")
display(results['Summary'])"""},
            {"type": "md", "content": "## 3. Base Case 5-Year Free Cash Flow to Firm (FCFF) Projections"},
            {"type": "code", "content": """display(results['Base']['Forecast_Table'])"""},
            {"type": "md", "content": "## 4. Valuation Sensitivity Analysis (WACC vs Terminal Growth Rate)"},
            {"type": "code", "content": """base_args = {
    "rev_growth_rates": [0.065, 0.065, 0.060, 0.055, 0.050],
    "ebit_margins": [0.215, 0.215, 0.210, 0.210, 0.205],
    "dna_pct_rev": 0.025, "capex_pct_rev": 0.032, "nwc_pct_change_rev": 0.08
}
sens_matrix = dcf.generate_sensitivity_table(base_args)
print("=== Intrinsic Value per Share (IDR) across WACC & Terminal Growth Rates ===")
display(sens_matrix)"""}
        ]
    )

    # -------------------------------------------------------------------------
    # Notebook 7: Investment Thesis
    # -------------------------------------------------------------------------
    create_notebook(
        "07_investment_thesis.ipynb",
        "07. Investment Thesis, Catalysts & Strategic Risks",
        "Synthesis of fundamental findings, economic moat analysis, catalysts, risks, and institutional investment recommendation.",
        [
            {"type": "md", "content": "## 1. Investment Rating & Valuation Summary"},
            {"type": "code", "content": """import sys, os, json
import pandas as pd

sys.path.append(os.path.abspath('../src'))
from valuation import DCFValuationModel

dcf = DCFValuationModel()
results = dcf.run_all_scenarios()
display(results['Summary'])"""},
            {"type": "md", "content": "## 2. Core Thesis, Economic Moat & Catalysts"},
            {"type": "code", "content": """with open('../data/processed/icbp_corporate_profile_intel.json', 'r', encoding='utf-8') as f:
    intel = json.load(f)

print("Key Investment Catalysts:")
for c in intel["Strategic_Catalysts"]:
    print(f"- {c}")

print("\nKey Risks & Mitigants:")
for r in intel["Key_Risks"]:
    print(f"- {r}")"""}
        ]
    )

if __name__ == "__main__":
    build_all_notebooks()
