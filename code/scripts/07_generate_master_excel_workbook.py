"""
07_generate_master_excel_workbook.py
Generates the comprehensive, institutional-grade Excel workbook containing all 6 data groups
with professional formatting, column widths, number styles, and clean headers.
Output: data/exports/ICBP_Equity_Research_Master_Dataset.xlsx
"""

import os
import json
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

def generate_master_excel():
    print("Generating Master Excel Workbook: data/exports/ICBP_Equity_Research_Master_Dataset.xlsx...")
    os.makedirs("data/exports", exist_ok=True)
    
    excel_path = "data/exports/ICBP_Equity_Research_Master_Dataset.xlsx"
    writer = pd.ExcelWriter(excel_path, engine="openpyxl")
    
    # 1. Executive Summary Sheet
    summary_data = [
        ["METRIC / ATTRIBUTE", "VALUE / DESCRIPTION", "NOTES / CONTEXT"],
        ["Company Name", "PT Indofood CBP Sukses Makmur Tbk", "Consumer Branded Products Flagship"],
        ["Stock Ticker", "ICBP.JK (IDX: ICBP)", "Listed on Indonesia Stock Exchange"],
        ["IPO Date", "2010-10-07", "Initial Public Offering (15+ Years Track Record)"],
        ["IPO Offering Price", "Rp 5,395 per share", "Unadjusted pre-split price"],
        ["Par Value / Split History", "1:2 Stock Split executed on 2016-07-27", "Par value halved from Rp 100 to Rp 50"],
        ["Total Shares Outstanding", "11,661,908,000 shares", "Stable share count post-2016 split"],
        ["Parent Entity", "PT Indofood Sukses Makmur Tbk (INDF)", "80.53% Controlling Ownership (Salim Group)"],
        ["Public Free Float", "19.47% (2,270,230,000 shares)", "Widely held by institutional & retail investors"],
        ["Core Business Moat", "Unmatched national distribution (>500k outlets) & iconic Indomie brand equity", "Global instant noodle capacity >37 billion packs/yr"],
        ["Geographic Footprint", "Domestic Indonesia (~69%) + Pinehill Global Markets (~31%)", "Operating plants in Nigeria, Saudi Arabia, Egypt, Turkey, Serbia, Kenya"],
        ["Latest Revenue (2025)", "Rp 74,850.9 Billion (~Rp 74.85 Trillion)", "15-Year Revenue CAGR: 9.98%"],
        ["Interim Revenue (9M26)", "Rp 64,445.7 Billion (+14.5% YoY)", "Run-rate FY26 Revenue estimated at ~Rp 85.9 Trillion"],
        ["Latest Net Profit (2025)", "Rp 9,224.9 Billion (~Rp 9.22 Trillion)", "15-Year Net Income CAGR: 11.92%"],
        ["Interim Net Profit (9M26)", "Rp 6,165.9 Billion (Rp 529 EPS)", "Healthy core profitability despite FX bond volatility"],
        ["Latest Operating Cash Flow (2025)", "Rp 12,104.4 Billion (~Rp 12.10 Trillion)", "Consistently positive CFO throughout corporate history"],
        ["Latest Cash & Equivalents (9M26)", "Rp 30,942.1 Billion (~Rp 30.94 Trillion)", "Robust liquidity reserve against foreign debt liabilities"],
        ["Total Assets (9M26)", "Rp 143,525.3 Billion (~Rp 143.53 Trillion)", "Grew 10.7x from Rp 13.36 Trillion at IPO"],
        ["Total Equity (9M26)", "Rp 77,801.4 Billion (~Rp 77.80 Trillion)", "Grew 8.3x from Rp 9.36 Trillion at IPO"],
        ["Total Dividends Paid (Cumulative)", ">Rp 27.5 Trillion returned to shareholders", "Uninterrupted annual cash dividend payout since IPO (33%-50% DPR)"]
    ]
    summary_df = pd.DataFrame(summary_data[1:], columns=summary_data[0])
    summary_df.to_excel(writer, sheet_name="Executive_Summary", index=False)
    
    # 2. Financial Statements Annual (2010 - 2025)
    fin_df = pd.read_csv("data/processed/icbp_financial_statements_annual_2010_2025.csv")
    fin_df.to_excel(writer, sheet_name="Financial_Statements", index=False)
    
    # 3. Financial Ratios (2010 - 2025)
    ratios_df = pd.read_csv("data/processed/icbp_financial_ratios_2010_2025.csv")
    ratios_df.to_excel(writer, sheet_name="Financial_Ratios", index=False)
    
    # 4. Quarterly & Interim Financials (2021 - 2026, incl 9M26)
    if os.path.exists("data/processed/icbp_quarterly_financials_2021_2026.csv"):
        q_df = pd.read_csv("data/processed/icbp_quarterly_financials_2021_2026.csv")
        q_df.to_excel(writer, sheet_name="Quarterly_Financials", index=False)
        
    # 5. Valuation Multiples Annual (2010 - 2025)
    val_df = pd.read_csv("data/processed/icbp_valuation_multiples_annual_2010_2025.csv")
    val_df.to_excel(writer, sheet_name="Valuation_Multiples", index=False)
    
    # 6. Historical Valuation Multiples Statistical Range
    if os.path.exists("data/processed/icbp_valuation_multiples_range_stats.csv"):
        vrange_df = pd.read_csv("data/processed/icbp_valuation_multiples_range_stats.csv")
        vrange_df.to_excel(writer, sheet_name="Valuation_Range_Stats", index=False)
        
    # 7. Peer Comparison Snapshot
    peers_df = pd.read_csv("data/processed/peers_financials_valuation_comparison.csv")
    peers_df.to_excel(writer, sheet_name="Peer_Comparison", index=False)
    
    # 8. Peer Multi-Year History (2015 - 2025)
    if os.path.exists("data/processed/peers_multi_year_financials_2015_2025.csv"):
        peer_hist_df = pd.read_csv("data/processed/peers_multi_year_financials_2015_2025.csv")
        peer_hist_df.to_excel(writer, sheet_name="Peer_Multi_Year_History", index=False)
        
    # 9. Macro & Commodity Environment Annual (2010 - 2025)
    macro_df = pd.read_csv("data/processed/macro_economic_environment_2010_2025.csv")
    macro_df.to_excel(writer, sheet_name="Macro_Commodities_Annual", index=False)
    
    # 10. Segments & Geography Breakdown
    seg_df = pd.read_csv("data/processed/icbp_segments_geography_breakdown.csv")
    seg_df.to_excel(writer, sheet_name="Segments_Geography", index=False)
    
    # 11. Annual & Monthly Returns
    if os.path.exists("data/processed/icbp_annual_returns_2010_2025.csv"):
        ann_ret_df = pd.read_csv("data/processed/icbp_annual_returns_2010_2025.csv")
        ann_ret_df.to_excel(writer, sheet_name="Annual_Returns", index=False)
        
    if os.path.exists("data/processed/icbp_monthly_returns_2010_2026.csv"):
        m_ret_df = pd.read_csv("data/processed/icbp_monthly_returns_2010_2026.csv")
        m_ret_df.to_excel(writer, sheet_name="Monthly_Returns", index=False)
        
    # 12. Daily Stock Market Series & Technicals (2010 - 2026)
    daily_df = pd.read_csv("data/processed/icbp_master_stock_market_daily.csv")
    daily_df.to_excel(writer, sheet_name="Daily_Stock_Prices", index=False)
    
    # 13. Corporate Actions Timeline
    with open("data/processed/icbp_corporate_profile_intel.json", "r", encoding="utf-8") as f:
        intel = json.load(f)
    corp_df = pd.DataFrame(intel["Corporate_Actions_Timeline"])
    corp_df.to_excel(writer, sheet_name="Corporate_Actions", index=False)
    
    # 14. Raw Financial Reports Catalog & Audit Trail (2010 - 2026)
    catalog_path = "data/raw/financial_statements/financial_reports_catalog.csv"
    if os.path.exists(catalog_path):
        cat_df = pd.read_csv(catalog_path)
        cat_df.to_excel(writer, sheet_name="Source_Reports_Catalog", index=False)
    
    writer.close()
    
    # Professional openpyxl formatting
    wb = openpyxl.load_workbook(excel_path)
    header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    
    for sheetname in wb.sheetnames:
        ws = wb[sheetname]
        ws.views.sheetView[0].showGridLines = True
        
        # Style headers
        for col_idx in range(1, ws.max_column + 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            
        # Set clean column widths based on sample data
        for col_idx in range(1, ws.max_column + 1):
            col_letter = get_column_letter(col_idx)
            max_len = 0
            for row_idx in range(1, min(ws.max_row + 1, 30)):
                val = ws.cell(row=row_idx, column=col_idx).value
                if val is not None:
                    max_len = max(max_len, len(str(val)))
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)
            
    wb.save(excel_path)
    print(f"Master Excel Workbook created with {len(wb.sheetnames)} sheets:")
    for i, s in enumerate(wb.sheetnames):
        print(f"  {i+1}. {s}")

if __name__ == "__main__":
    generate_master_excel()
