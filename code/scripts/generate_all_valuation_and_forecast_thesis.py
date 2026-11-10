"""
generate_all_valuation_and_forecast_thesis.py
Computes and generates all financial forecasts (2026E-2030E), 3-scenario DCF models,
sensitivity grids, peer rankings, technical stats, and macro sensitivity tables.
Outputs structured CSVs for thesis_data.
"""

import pandas as pd
import numpy as np
import os

# 1. Financial Forecasts (2026E - 2030E)
# Base Year: FY2025 (Revenue: Rp 74,850.9 B, EBIT: Rp 16,655.5 B, Net Income: Rp 9,224.9 B)
# 1H26 Actual: Revenue Rp 41,863.4 B (+11.3% YoY), indicating FY26E annualized ~ Rp 82,500 - 83,500 B.

forecast_years = [2026, 2027, 2028, 2029, 2030]

# Base Case Forecast Assumptions
base_rev_growth = [0.105, 0.075, 0.070, 0.065, 0.060]  # FY26 reflects 1H26 momentum (+10.5%), tapering to 6%
base_ebit_margins = [0.222, 0.220, 0.218, 0.215, 0.215]
tax_rate = 0.22
dna_rate = 0.026      # ~2.6% of revenue
capex_rate = 0.038    # ~3.8% of revenue (expansion in Africa + modern domestic lines)
nwc_rate = 0.08       # ~8% of delta revenue

forecast_data = []
prior_rev = 74850.9
cash_balance = 29216.5
total_debt = 47186.4
net_debt_start = 17969.9

for i, yr in enumerate(forecast_years):
    g = base_rev_growth[i]
    rev = prior_rev * (1 + g)
    ebit_margin = base_ebit_margins[i]
    ebit = rev * ebit_margin
    nopat = ebit * (1 - tax_rate)
    dna = rev * dna_rate
    capex = rev * capex_rate
    delta_rev = rev - prior_rev
    delta_nwc = delta_rev * nwc_rate
    
    # Free Cash Flow to Firm (FCFF)
    fcff = nopat + dna - capex - delta_nwc
    
    # Net Interest Expense (USD 2.75B bonds ~ 4.2% avg coupon - interest on cash)
    net_interest = 1650.0  # ~Rp 1,650 B
    ebt = ebit - net_interest
    tax = ebt * tax_rate
    net_income = ebt - tax
    
    # Cash Flow from Operations (CFO = Net Income + D&A - Delta NWC)
    cfo = net_income + dna - delta_nwc
    fcf_equity = cfo - capex
    
    forecast_data.append({
        "Forecast_Year": f"{yr}E",
        "Revenue_IDR_B": round(rev, 1),
        "Revenue_Growth_YoY_%": round(g * 100, 2),
        "Gross_Profit_IDR_B": round(rev * 0.355, 1),
        "Gross_Margin_%": 35.5,
        "EBIT_IDR_B": round(ebit, 1),
        "EBIT_Margin_%": round(ebit_margin * 100, 2),
        "NOPAT_IDR_B": round(nopat, 1),
        "Depreciation_Amortization_IDR_B": round(dna, 1),
        "Capex_IDR_B": round(capex, 1),
        "Change_in_NWC_IDR_B": round(delta_nwc, 1),
        "FCFF_IDR_B": round(fcff, 1),
        "CFO_IDR_B": round(cfo, 1),
        "FCFE_IDR_B": round(fcf_equity, 1),
        "Net_Income_IDR_B": round(net_income, 1),
        "EPS_IDR": round((net_income * 1000) / 11661.908, 0)
    })
    prior_rev = rev

df_forecast = pd.DataFrame(forecast_data)
os.makedirs("thesis_data", exist_ok=True)
df_forecast.to_csv("thesis_data/07_financial_forecasts_2026_2030.csv", index=False)
print("Saved 2026E-2030E Financial Forecasts.")

# 2. DCF Valuation Models (Bear, Base, Bull)
# Common parameters:
shares_out = 11661.908 # Million shares
current_price = 5775.0 # Market price in IDR
net_debt = 17969.9     # Total Debt - Cash (FY2025)

def calc_dcf(wacc, terminal_g, rev_growths, ebit_margins, dna_pct=0.026, capex_pct=0.038, nwc_pct=0.08):
    rev_prev = 74850.9
    pv_fcff_list = []
    fcff_list = []
    df_list = []
    
    for t, (g, m) in enumerate(zip(rev_growths, ebit_margins), 1):
        r = rev_prev * (1 + g)
        eb = r * m
        np_val = eb * (1 - 0.22)
        d = r * dna_pct
        c = r * capex_pct
        dnwc = (r - rev_prev) * nwc_pct
        f = np_val + d - c - dnwc
        df = 1.0 / ((1 + wacc) ** t)
        pv = f * df
        
        fcff_list.append(f)
        df_list.append(df)
        pv_fcff_list.append(pv)
        rev_prev = r
        
    sum_pv_fcff = sum(pv_fcff_list)
    term_fcff = fcff_list[-1] * (1 + terminal_g)
    tv = term_fcff / (wacc - terminal_g)
    pv_tv = tv * df_list[-1]
    
    ev = sum_pv_fcff + pv_tv
    eq_val = ev - net_debt
    target_price = (eq_val * 1000) / shares_out
    upside = ((target_price / current_price) - 1) * 100
    
    return {
        "WACC": wacc, "Term_g": terminal_g,
        "Sum_PV_FCFF": sum_pv_fcff, "TV": tv, "PV_TV": pv_tv,
        "EV": ev, "Net_Debt": net_debt, "Equity_Value": eq_val,
        "Target_Price_Rp": target_price, "Upside_%": upside
    }

# Scenarios
# Bear Case: High inflation, lower MEA growth, WACC 9.2% (Rf 7.0%, Beta 0.65, ERP 6.0%), g 2.5%
bear_res = calc_dcf(
    wacc=0.088, terminal_g=0.025,
    rev_growths=[0.05, 0.045, 0.040, 0.035, 0.030],
    ebit_margins=[0.195, 0.190, 0.185, 0.180, 0.180]
)

# Base Case: Consensus, Pinehill steady ramp, WACC 8.1% (Rf 6.5%, Beta 0.58, ERP 5.2%), g 3.5%
base_res = calc_dcf(
    wacc=0.081, terminal_g=0.035,
    rev_growths=[0.105, 0.075, 0.070, 0.065, 0.060],
    ebit_margins=[0.222, 0.220, 0.218, 0.215, 0.215]
)

# Bull Case: High Africa penetration, premiumization success, WACC 7.4% (Rf 6.0%, Beta 0.52, ERP 4.8%), g 4.2%
bull_res = calc_dcf(
    wacc=0.074, terminal_g=0.042,
    rev_growths=[0.130, 0.100, 0.090, 0.085, 0.080],
    ebit_margins=[0.235, 0.235, 0.230, 0.230, 0.225]
)

print(f"Bear Target Price: Rp {bear_res['Target_Price_Rp']:,.0f} ({bear_res['Upside_%']:+.1f}%)")
print(f"Base Target Price: Rp {base_res['Target_Price_Rp']:,.0f} ({base_res['Upside_%']:+.1f}%)")
print(f"Bull Target Price: Rp {bull_res['Target_Price_Rp']:,.0f} ({bull_res['Upside_%']:+.1f}%)")

# 3. Sensitivity Grid: WACC vs Terminal Growth Rate
wacc_grid = [0.071, 0.076, 0.081, 0.086, 0.091]
g_grid = [0.025, 0.030, 0.035, 0.040, 0.045]

sens_rows = []
for w in wacc_grid:
    row = {"WACC_%": f"{w*100:.1f}%"}
    for g in g_grid:
        if w > g:
            res = calc_dcf(
                wacc=w, terminal_g=g,
                rev_growths=base_rev_growth, ebit_margins=base_ebit_margins
            )
            row[f"g={g*100:.1f}%"] = round(res["Target_Price_Rp"], 0)
        else:
            row[f"g={g*100:.1f}%"] = np.nan
    sens_rows.append(row)

df_sens = pd.DataFrame(sens_rows)
df_sens.to_csv("thesis_data/08_dcf_sensitivity_matrix.csv", index=False)
print("Saved DCF Sensitivity Matrix.")

