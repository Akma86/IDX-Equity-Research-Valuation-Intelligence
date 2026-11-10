"""
src/valuation.py
Discounted Cash Flow (DCF) valuation model, WACC calculation, 3-scenario forecasting
(Bear, Base, Bull), and 2D sensitivity matrix as specified in Data.md Section 3.
"""

import numpy as np
import pandas as pd

class DCFValuationModel:
    def __init__(
        self,
        base_revenue: float = 74850.9,     # FY2025 Revenue in IDR Billion
        net_debt: float = 17969.9,         # Total Debt - Cash as of FY2025 (IDR Billion)
        shares_outstanding: float = 11661.908, # Million shares
        current_price: float = 5575.0,     # Current market price in IDR
        forecast_years: int = 5,
        tax_rate: float = 0.22,            # Indonesia Corporate Income Tax Rate
    ):
        self.base_revenue = base_revenue
        self.net_debt = net_debt
        self.shares_outstanding = shares_outstanding
        self.current_price = current_price
        self.forecast_years = forecast_years
        self.tax_rate = tax_rate

    def calculate_wacc(
        self,
        risk_free_rate: float,
        equity_risk_premium: float,
        beta: float,
        cost_of_debt_pre_tax: float,
        target_equity_weight: float = 0.70,
        target_debt_weight: float = 0.30,
    ) -> dict:
        """Calculates WACC via CAPM."""
        cost_of_equity = risk_free_rate + beta * equity_risk_premium
        cost_of_debt_after_tax = cost_of_debt_pre_tax * (1.0 - self.tax_rate)
        wacc = (target_equity_weight * cost_of_equity) + (target_debt_weight * cost_of_debt_after_tax)
        return {
            "Cost_of_Equity_%": round(cost_of_equity * 100, 2),
            "Cost_of_Debt_After_Tax_%": round(cost_of_debt_after_tax * 100, 2),
            "WACC_%": round(wacc * 100, 2),
            "WACC_decimal": wacc,
            "Cost_of_Equity_decimal": cost_of_equity
        }

    def run_dcf_forecast(
        self,
        rev_growth_rates: list,       # Length 5 (e.g. [0.06, 0.06, 0.05, 0.05, 0.04])
        ebit_margins: list,           # Length 5 (e.g. [0.21, 0.21, 0.21, 0.20, 0.20])
        dna_pct_rev: float,           # e.g. 0.025
        capex_pct_rev: float,         # e.g. 0.035
        nwc_pct_change_rev: float,    # e.g. 0.08
        wacc: float,
        terminal_growth: float
    ) -> dict:
        """
        Projects Free Cash Flow to Firm (FCFF) for 5 forecast years, discounts them,
        and computes Terminal Value, Enterprise Value, and Intrinsic Value Per Share.
        """
        forecasts = []
        prior_rev = self.base_revenue
        discount_factors = []
        pv_fcffs = []
        
        for i in range(self.forecast_years):
            g = rev_growth_rates[i]
            rev = prior_rev * (1.0 + g)
            ebit_margin = ebit_margins[i]
            ebit = rev * ebit_margin
            nopat = ebit * (1.0 - self.tax_rate)
            dna = rev * dna_pct_rev
            capex = rev * capex_pct_rev
            delta_rev = rev - prior_rev
            delta_nwc = delta_rev * nwc_pct_change_rev
            
            # Free Cash Flow to Firm (FCFF)
            fcff = nopat + dna - capex - delta_nwc
            
            # Discount Factor
            t = i + 1
            df = 1.0 / ((1.0 + wacc) ** t)
            pv_fcff = fcff * df
            
            discount_factors.append(df)
            pv_fcffs.append(pv_fcff)
            
            forecasts.append({
                "Year": f"Year +{t}",
                "Revenue_Growth_%": round(g * 100, 2),
                "Revenue": round(rev, 1),
                "EBIT": round(ebit, 1),
                "NOPAT": round(nopat, 1),
                "D&A": round(dna, 1),
                "Capex": round(capex, 1),
                "Delta_NWC": round(delta_nwc, 1),
                "FCFF": round(fcff, 1),
                "Discount_Factor": round(df, 4),
                "PV_FCFF": round(pv_fcff, 1)
            })
            prior_rev = rev
            
        sum_pv_fcff = sum(pv_fcffs)
        
        # Terminal Value via Gordon Growth Model on Year 5 FCFF
        terminal_fcff = forecasts[-1]["FCFF"] * (1.0 + terminal_growth)
        terminal_value = terminal_fcff / (wacc - terminal_growth)
        pv_terminal_value = terminal_value * discount_factors[-1]
        
        enterprise_value = sum_pv_fcff + pv_terminal_value
        equity_value = enterprise_value - self.net_debt
        intrinsic_value_per_share = (equity_value * 1000.0) / self.shares_outstanding # in IDR
        
        upside_downside = ((intrinsic_value_per_share / self.current_price) - 1.0) * 100.0
        margin_of_safety = max(0.0, 1.0 - (self.current_price / intrinsic_value_per_share)) * 100.0 if intrinsic_value_per_share > 0 else 0.0
        
        return {
            "Forecast_Table": pd.DataFrame(forecasts),
            "Sum_PV_FCFF": round(sum_pv_fcff, 1),
            "Terminal_Value": round(terminal_value, 1),
            "PV_Terminal_Value": round(pv_terminal_value, 1),
            "PV_Terminal_Value_%": round((pv_terminal_value / enterprise_value) * 100, 1),
            "Enterprise_Value": round(enterprise_value, 1),
            "Net_Debt": round(self.net_debt, 1),
            "Equity_Value": round(equity_value, 1),
            "Intrinsic_Value_Per_Share": round(intrinsic_value_per_share, 0),
            "Current_Market_Price": round(self.current_price, 0),
            "Upside_Downside_%": round(upside_downside, 2),
            "Margin_of_Safety_%": round(margin_of_safety, 2),
            "WACC_%": round(wacc * 100, 2),
            "Terminal_Growth_%": round(terminal_growth * 100, 2)
        }

    def run_all_scenarios(self) -> dict:
        """
        Executes Bear, Base, and Bull scenarios as mapped in Data.md Section 3.2.
        """
        # Common macroeconomic baseline:
        # Indonesia 10Y Govt Bond SUN Yield ~ 6.50%
        # Equity Risk Premium ~ 5.0% - 5.5%
        # Beta ~ 0.58
        
        # 1. Bear Case
        wacc_bear = self.calculate_wacc(
            risk_free_rate=0.070, equity_risk_premium=0.060, beta=0.65, cost_of_debt_pre_tax=0.065
        )["WACC_decimal"]
        bear_res = self.run_dcf_forecast(
            rev_growth_rates=[0.04, 0.04, 0.035, 0.03, 0.03],
            ebit_margins=[0.19, 0.19, 0.185, 0.18, 0.18],
            dna_pct_rev=0.024, capex_pct_rev=0.035, nwc_pct_change_rev=0.09,
            wacc=wacc_bear, terminal_growth=0.025
        )
        
        # 2. Base Case
        wacc_base = self.calculate_wacc(
            risk_free_rate=0.065, equity_risk_premium=0.052, beta=0.58, cost_of_debt_pre_tax=0.055
        )["WACC_decimal"]
        base_res = self.run_dcf_forecast(
            rev_growth_rates=[0.065, 0.065, 0.060, 0.055, 0.050],
            ebit_margins=[0.215, 0.215, 0.210, 0.210, 0.205],
            dna_pct_rev=0.025, capex_pct_rev=0.032, nwc_pct_change_rev=0.08,
            wacc=wacc_base, terminal_growth=0.035
        )
        
        # 3. Bull Case
        wacc_bull = self.calculate_wacc(
            risk_free_rate=0.060, equity_risk_premium=0.048, beta=0.52, cost_of_debt_pre_tax=0.048
        )["WACC_decimal"]
        bull_res = self.run_dcf_forecast(
            rev_growth_rates=[0.085, 0.085, 0.080, 0.075, 0.070],
            ebit_margins=[0.230, 0.230, 0.225, 0.225, 0.220],
            dna_pct_rev=0.026, capex_pct_rev=0.030, nwc_pct_change_rev=0.07,
            wacc=wacc_bull, terminal_growth=0.042
        )
        
        summary_table = pd.DataFrame([
            {
                "Scenario": "Bear Case",
                "Avg_Rev_Growth_%": "3.5%",
                "Avg_EBIT_Margin_%": "18.5%",
                "WACC_%": f"{bear_res['WACC_%']}%",
                "Terminal_Growth_%": f"{bear_res['Terminal_Growth_%']}%",
                "Enterprise_Value_IDR_B": f"Rp {bear_res['Enterprise_Value']:,.1f}",
                "Equity_Value_IDR_B": f"Rp {bear_res['Equity_Value']:,.1f}",
                "Intrinsic_Value_per_Share": f"Rp {bear_res['Intrinsic_Value_Per_Share']:,.0f}",
                "Current_Price": f"Rp {bear_res['Current_Market_Price']:,.0f}",
                "Upside_Downside_%": f"{bear_res['Upside_Downside_%']:+.1f}%",
                "Margin_of_Safety_%": f"{bear_res['Margin_of_Safety_%']:.1f}%"
            },
            {
                "Scenario": "Base Case",
                "Avg_Rev_Growth_%": "5.9%",
                "Avg_EBIT_Margin_%": "21.1%",
                "WACC_%": f"{base_res['WACC_%']}%",
                "Terminal_Growth_%": f"{base_res['Terminal_Growth_%']}%",
                "Enterprise_Value_IDR_B": f"Rp {base_res['Enterprise_Value']:,.1f}",
                "Equity_Value_IDR_B": f"Rp {base_res['Equity_Value']:,.1f}",
                "Intrinsic_Value_per_Share": f"Rp {base_res['Intrinsic_Value_Per_Share']:,.0f}",
                "Current_Price": f"Rp {base_res['Current_Market_Price']:,.0f}",
                "Upside_Downside_%": f"{base_res['Upside_Downside_%']:+.1f}%",
                "Margin_of_Safety_%": f"{base_res['Margin_of_Safety_%']:.1f}%"
            },
            {
                "Scenario": "Bull Case",
                "Avg_Rev_Growth_%": "7.9%",
                "Avg_EBIT_Margin_%": "22.6%",
                "WACC_%": f"{bull_res['WACC_%']}%",
                "Terminal_Growth_%": f"{bull_res['Terminal_Growth_%']}%",
                "Enterprise_Value_IDR_B": f"Rp {bull_res['Enterprise_Value']:,.1f}",
                "Equity_Value_IDR_B": f"Rp {bull_res['Equity_Value']:,.1f}",
                "Intrinsic_Value_per_Share": f"Rp {bull_res['Intrinsic_Value_Per_Share']:,.0f}",
                "Current_Price": f"Rp {bull_res['Current_Market_Price']:,.0f}",
                "Upside_Downside_%": f"{bull_res['Upside_Downside_%']:+.1f}%",
                "Margin_of_Safety_%": f"{bull_res['Margin_of_Safety_%']:.1f}%"
            }
        ])
        
        return {
            "Bear": bear_res,
            "Base": base_res,
            "Bull": bull_res,
            "Summary": summary_table
        }

    def generate_sensitivity_table(
        self,
        base_forecast_args: dict,
        wacc_range: list = [0.070, 0.075, 0.080, 0.085, 0.090, 0.095],
        growth_range: list = [0.025, 0.030, 0.035, 0.040, 0.045]
    ) -> pd.DataFrame:
        """
        Generates 2D Sensitivity Matrix: WACC vs Terminal Growth Rate.
        Values are Intrinsic Value Per Share (IDR).
        """
        matrix = []
        for w in wacc_range:
            row = {"WACC_%": f"{w*100:.1f}%"}
            for g in growth_range:
                if w > g:
                    res = self.run_dcf_forecast(
                        rev_growth_rates=base_forecast_args["rev_growth_rates"],
                        ebit_margins=base_forecast_args["ebit_margins"],
                        dna_pct_rev=base_forecast_args["dna_pct_rev"],
                        capex_pct_rev=base_forecast_args["capex_pct_rev"],
                        nwc_pct_change_rev=base_forecast_args["nwc_pct_change_rev"],
                        wacc=w,
                        terminal_growth=g
                    )
                    row[f"g = {g*100:.1f}%"] = res["Intrinsic_Value_Per_Share"]
                else:
                    row[f"g = {g*100:.1f}%"] = np.nan
            matrix.append(row)
        return pd.DataFrame(matrix)

if __name__ == "__main__":
    model = DCFValuationModel()
    scenarios = model.run_all_scenarios()
    print("=== ICBP DCF INTRINSIC VALUATION SUMMARY (3 SCENARIOS) ===")
    print(scenarios["Summary"].to_string(index=False))
    
    base_args = {
        "rev_growth_rates": [0.065, 0.065, 0.060, 0.055, 0.050],
        "ebit_margins": [0.215, 0.215, 0.210, 0.210, 0.205],
        "dna_pct_rev": 0.025, "capex_pct_rev": 0.032, "nwc_pct_change_rev": 0.08
    }
    sens_df = model.generate_sensitivity_table(base_args)
    print("\n=== SENSITIVITY ANALYSIS: WACC vs TERMINAL GROWTH RATE (Target Price Rp) ===")
    print(sens_df.to_string(index=False))

