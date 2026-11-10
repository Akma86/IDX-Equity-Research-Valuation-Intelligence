"""
src/financial_metrics.py
Financial analysis, ratios calculation, DuPont decomposition, and capital efficiency metrics
as specified in Data.md section 2.1.
"""

import pandas as pd
import numpy as np

def calculate_derived_financial_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes all derived financial metrics specified in Data.md:
    Growth, Profitability, Return, Capital Structure, Cash Flow, and Quality of Earnings.
    """
    res = df.copy()
    
    # 1. Growth Metrics
    res["Revenue_Growth_%"] = res["Revenue"].pct_change() * 100.0
    res["EBIT_Growth_%"] = res["EBIT"].pct_change() * 100.0
    res["NetIncome_Growth_%"] = res["NetIncome"].pct_change() * 100.0
    res["EPS_Growth_%"] = res["EPS"].pct_change() * 100.0
    
    # 2. Profitability Margins
    res["Gross_Margin_%"] = (res["GrossProfit"] / res["Revenue"]) * 100.0
    res["EBIT_Margin_%"] = (res["EBIT"] / res["Revenue"]) * 100.0
    res["EBITDA_Margin_%"] = (res["EBITDA"] / res["Revenue"]) * 100.0
    res["Net_Margin_%"] = (res["NetIncome"] / res["Revenue"]) * 100.0
    
    # 3. Capital Efficiency & Returns
    # Effective tax rate assumed ~22% for NOPAT
    tax_rate = 0.22
    res["NOPAT"] = res["EBIT"] * (1 - tax_rate)
    # Invested Capital = Total Equity + Total Debt - Cash
    res["Invested_Capital"] = res["TotalEquity"] + res["TotalDebt"] - res["Cash"]
    res["ROIC_%"] = (res["NOPAT"] / res["Invested_Capital"]) * 100.0
    res["ROE_%"] = (res["NetIncome"] / res["TotalEquity"]) * 100.0
    res["ROA_%"] = (res["NetIncome"] / res["TotalAssets"]) * 100.0
    
    # 4. Solvency and Leverage
    res["Debt_to_Equity_x"] = res["TotalDebt"] / res["TotalEquity"]
    res["Net_Debt"] = res["TotalDebt"] - res["Cash"]
    res["Net_Debt_to_EBITDA_x"] = res["Net_Debt"] / res["EBITDA"]
    res["Debt_to_Assets_x"] = res["TotalDebt"] / res["TotalAssets"]
    
    # 5. Cash Flow & Earnings Quality
    if "FreeCashFlow" not in res.columns:
        res["FreeCashFlow"] = res["CFO"] - res["Capex"]
    res["FCF_Margin_%"] = (res["FreeCashFlow"] / res["Revenue"]) * 100.0
    res["CFO_to_NetIncome_x"] = res["CFO"] / res["NetIncome"]
    res["FCF_Conversion_%"] = (res["FreeCashFlow"] / res["NetIncome"]) * 100.0
    res["Capex_to_Revenue_%"] = (res["Capex"] / res["Revenue"]) * 100.0
    if "CurrentAssets" in res.columns and "CurrentLiabilities" in res.columns:
        res["Current_Ratio_x"] = res["CurrentAssets"] / res["CurrentLiabilities"]
        res["Net_Working_Capital"] = res["CurrentAssets"] - res["CurrentLiabilities"]
    
    # 6. DuPont Analysis (3-way)
    # ROE = Net Margin * Asset Turnover * Equity Multiplier
    res["Asset_Turnover_x"] = res["Revenue"] / res["TotalAssets"]
    res["Equity_Multiplier_x"] = res["TotalAssets"] / res["TotalEquity"]
    res["DuPont_ROE_%"] = res["Net_Margin_%"] * res["Asset_Turnover_x"] * res["Equity_Multiplier_x"]
    
    return res

def calculate_cagr(start_val: float, end_val: float, periods: int) -> float:
    """Calculates Compound Annual Growth Rate (CAGR)."""
    if start_val <= 0 or end_val <= 0 or periods <= 0:
        return np.nan
    return ((end_val / start_val) ** (1.0 / periods) - 1.0) * 100.0

def get_growth_cagrs(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates 3Y, 5Y, 10Y, and Since-IPO (15Y) CAGRs for key indicators."""
    latest_yr = df["Year"].max()
    metrics = ["Revenue", "GrossProfit", "EBIT", "EBITDA", "NetIncome", "TotalAssets", "TotalEquity", "CFO"]
    
    periods = {
        "3-Year (2022-2025)": 3,
        "5-Year (2020-2025)": 5,
        "10-Year (2015-2025)": 10,
        "15-Year Since IPO (2010-2025)": 15
    }
    
    records = []
    for label, n_yr in periods.items():
        base_yr = latest_yr - n_yr
        row_now = df[df["Year"] == latest_yr].iloc[0]
        row_base = df[df["Year"] == base_yr]
        if not row_base.empty:
            row_base = row_base.iloc[0]
            rec = {"Period": label}
            for m in metrics:
                rec[f"{m}_CAGR_%"] = round(calculate_cagr(row_base[m], row_now[m], n_yr), 2)
            records.append(rec)
            
    return pd.DataFrame(records)

if __name__ == "__main__":
    from data_processing import load_financial_data
    df = load_financial_data()
    metrics_df = calculate_derived_financial_metrics(df)
    cagr_df = get_growth_cagrs(df)
    print("--- Derived Financial Metrics (Recent 5 Years) ---")
    cols_to_show = ["Year", "Revenue", "Gross_Margin_%", "EBIT_Margin_%", "Net_Margin_%", "ROE_%", "ROIC_%", "Net_Debt_to_EBITDA_x", "CFO_to_NetIncome_x"]
    print(metrics_df[cols_to_show].tail().to_string(index=False))
    print("\n--- Long-Horizon CAGRs ---")
    print(cagr_df.to_string(index=False))

