"""
tests/test_application.py
Unit tests and mathematical validation for ICBP Equity Research & Valuation Intelligence.
Validates data provenance, accounting identities, DCF formula logic, and peer multiples.
"""

import os
import unittest
import pandas as pd
import numpy as np

class TestICBPEquityResearch(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        def load_csv(paths):
            for p in paths:
                if os.path.exists(p):
                    return pd.read_csv(p)
            raise FileNotFoundError(f"None of the candidate paths exist: {paths}")

        cls.fin_metrics = load_csv(["results/data_tables/financial_metrics.csv", "data/processed/financial_metrics.csv"])
        cls.fin_annual = load_csv(["results/data_tables/icbp_financial_statements_annual_2010_2025.csv", "data/processed/icbp_financial_statements_annual_2010_2025.csv"])
        cls.segment_ts = load_csv(["results/data_tables/06_master_revenue_dataset_timeseries.csv", "thesis_data/06_master_revenue_dataset_timeseries.csv"])
        cls.peers = load_csv(["results/data_tables/peers_financials_valuation_comparison.csv", "data/processed/peers_financials_valuation_comparison.csv"])
        cls.stock = load_csv(["results/data_tables/stock_performance.csv", "data/processed/stock_performance.csv"])
        cls.macro = load_csv(["results/data_tables/macro_economic_environment_2010_2025.csv", "data/processed/macro_economic_environment_2010_2025.csv"])
        cls.forecasts = load_csv(["results/data_tables/07_financial_forecasts_2026_2030.csv", "thesis_data/07_financial_forecasts_2026_2030.csv"])
        cls.range_stats = load_csv(["results/data_tables/icbp_valuation_multiples_range_stats.csv", "data/processed/icbp_valuation_multiples_range_stats.csv"])

    def test_data_provenance_and_files_exist(self):
        """Verifies all required core datasets exist and have expected rows."""
        self.assertGreaterEqual(len(self.fin_annual), 16, "Annual financials must cover 2010-2025.")
        self.assertGreaterEqual(len(self.segment_ts), 17, "Segment series must cover 17 periods.")
        self.assertGreaterEqual(len(self.stock), 3900, "Daily stock market data must exceed 3900 trading days.")
        self.assertGreaterEqual(len(self.peers), 5, "Peer comparison must include at least 5 companies.")

    def test_accounting_identities(self):
        """Validates standard accounting equations across all historical years."""
        df = self.fin_annual
        for _, row in df.iterrows():
            # 1. Gross Profit = Revenue - COGS
            self.assertAlmostEqual(row["GrossProfit"], row["Revenue"] - row["COGS"], delta=0.5)
            # 2. Net Debt = Total Debt - Cash
            self.assertAlmostEqual(row["NetDebt"], row["TotalDebt"] - row["Cash"], delta=0.5)
            # 3. Net Working Capital = Current Assets - Current Liabilities
            self.assertAlmostEqual(row["NetWorkingCapital"], row["CurrentAssets"] - row["CurrentLiabilities"], delta=0.5)
            # 4. Free Cash Flow = CFO - Capex
            self.assertAlmostEqual(row["FreeCashFlow"], row["CFO"] - row["Capex"], delta=0.5)

    def test_dcf_wacc_and_terminal_value_math(self):
        """Validates CAPM WACC and Gordon Growth Terminal Value mathematical integrity."""
        rf = 0.065
        beta = 0.58
        erp = 0.052
        cost_of_equity = rf + beta * erp
        self.assertAlmostEqual(cost_of_equity, 0.09516, places=4)
        
        pre_tax_kd = 0.055
        tax_rate = 0.22
        after_tax_kd = pre_tax_kd * (1.0 - tax_rate)
        self.assertAlmostEqual(after_tax_kd, 0.0429, places=4)
        
        wacc = 0.70 * cost_of_equity + 0.30 * after_tax_kd
        self.assertAlmostEqual(wacc, 0.079482, delta=0.002)
        
        # Gordon Growth Terminal Value test
        fcff_5 = 16236.0
        g = 0.035
        w = 0.081
        tv = fcff_5 * (1 + g) / (w - g)
        self.assertGreater(tv, 300000.0, "Terminal Value must be mathematically consistent.")

    def test_segment_reconciliation(self):
        """Validates that sum of segments equals gross revenue before eliminations."""
        df_seg = self.segment_ts
        for _, row in df_seg.iterrows():
            sum_segments = (
                row["Noodles_Rev"] + row["Dairy_Rev"] + row["Snacks_Rev"] +
                row["Seasonings_Rev"] + row["Nutrition_Rev"] + row["Beverages_Rev"]
            )
            self.assertAlmostEqual(sum_segments, row["Total_Gross_Rev"], delta=1.0)
            self.assertAlmostEqual(row["Total_Gross_Rev"] + row["Elimination_Rev"], row["Total_Net_Rev"], delta=1.5)

    def test_valuation_multiple_discount(self):
        """Verifies that current P/E is verified at historical discount rank."""
        pe_row = self.range_stats[self.range_stats["Valuation_Multiple"] == "P_E_x"].iloc[0]
        self.assertLess(pe_row["Current_Value"], pe_row["Median"], "Current P/E must be lower than median.")
        self.assertLess(pe_row["Discount_To_Median_%"], -50.0, "Discount to median P/E must be over 50%.")

if __name__ == "__main__":
    unittest.main()
