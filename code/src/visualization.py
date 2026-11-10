"""
src/visualization.py
Generates high-resolution institutional-grade research figures and charts
saved to reports/figures/ for GitHub portfolio presentation and research reports.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np

# Set institutional styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES_DIR = os.path.join(BASE_DIR, "reports", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

NAVY = "#1B365D"
BLUE = "#206095"
LIGHT_BLUE = "#4192D9"
TEAL = "#008080"
AMBER = "#D97706"
CRIMSON = "#B91C1C"
GRAY = "#64748B"

def plot_all_figures():
    print("Generating institutional research figures in reports/figures/...")
    
    # Load processed data
    fin_df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "financial_metrics.csv"))
    val_df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "valuation_metrics.csv"))
    stock_df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "stock_performance.csv"))
    stock_df["Date"] = pd.to_datetime(stock_df["Date"])
    peer_df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "peer_comparison.csv"))
    macro_df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "macroeconomic_data.csv"))
    seg_df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "icbp_segments_geography_breakdown.csv"))

    # -------------------------------------------------------------
    # Figure 1: Long-Horizon Revenue & Profitability (2010 - 2025)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    x = fin_df["Year"]
    ax.plot(x, fin_df["Revenue"] / 1000.0, marker='o', linewidth=2.5, color=NAVY, label="Net Revenue (IDR Trillion)")
    ax.plot(x, fin_df["GrossProfit"] / 1000.0, marker='s', linewidth=2, color=BLUE, label="Gross Profit (IDR Trillion)")
    ax.plot(x, fin_df["EBIT"] / 1000.0, marker='^', linewidth=2, color=TEAL, label="Operating Profit / EBIT (IDR Trillion)")
    ax.plot(x, fin_df["NetIncome"] / 1000.0, marker='d', linewidth=2, color=AMBER, label="Net Income (IDR Trillion)")
    
    ax.axvline(x=2020, color=CRIMSON, linestyle="--", alpha=0.7, label="Pinehill M&A Consolidation (2020)")
    ax.set_title("ICBP 15-Year Financial Trajectory (FY2010 - FY2025)\nRevenue CAGR: 9.98% | Net Profit CAGR: 11.92%", fontsize=13, fontweight='bold', pad=12, color=NAVY)
    ax.set_ylabel("IDR Trillion", fontsize=11, fontweight='bold')
    ax.set_xlabel("Fiscal Year", fontsize=11)
    ax.set_xticks(x)
    ax.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0", loc="upper left")
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "01_financial_trajectory_growth.png"))
    plt.close()

    # -------------------------------------------------------------
    # Figure 2: Margin Evolution & Pricing Power
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, (fin_df["GrossProfit"] / fin_df["Revenue"]) * 100, marker='o', linewidth=2.5, color=NAVY, label="Gross Profit Margin (%)")
    ax.plot(x, (fin_df["EBIT"] / fin_df["Revenue"]) * 100, marker='s', linewidth=2.2, color=TEAL, label="EBIT Margin (%)")
    ax.plot(x, (fin_df["NetIncome"] / fin_df["Revenue"]) * 100, marker='^', linewidth=2.0, color=AMBER, label="Net Profit Margin (%)")
    
    ax.set_title("ICBP Profitability Margins & Pricing Power Resilience (2010 - 2025)", fontsize=13, fontweight='bold', pad=12, color=NAVY)
    ax.set_ylabel("Margin (%)", fontsize=11, fontweight='bold')
    ax.set_xlabel("Fiscal Year", fontsize=11)
    ax.set_xticks(x)
    ax.set_ylim(5, 42)
    ax.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0", loc="center left")
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "02_margin_stability_evolution.png"))
    plt.close()

    # -------------------------------------------------------------
    # Figure 3: Operating Cash Flow vs Capex vs FCF
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    bar_width = 0.38
    r1 = np.arange(len(x))
    r2 = [val + bar_width for val in r1]
    
    ax.bar(r1, fin_df["CFO"] / 1000.0, width=bar_width, color=NAVY, label="Operating Cash Flow (CFO)", alpha=0.9)
    ax.bar(r2, fin_df["Capex"] / 1000.0, width=bar_width, color=AMBER, label="Capital Expenditure (Capex)", alpha=0.9)
    ax.plot(r1 + bar_width/2, fin_df["FreeCashFlow"] / 1000.0, color=TEAL, marker='o', linewidth=2.5, label="Free Cash Flow (CFO - Capex)")
    
    ax.set_title("ICBP Cash Flow Generation & Capital Allocation (IDR Trillion)", fontsize=13, fontweight='bold', pad=12, color=NAVY)
    ax.set_ylabel("IDR Trillion", fontsize=11, fontweight='bold')
    ax.set_xticks(r1 + bar_width / 2)
    ax.set_xticklabels(x)
    ax.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0", loc="upper left")
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "03_cfo_fcf_capex_generation.png"))
    plt.close()

    # -------------------------------------------------------------
    # Figure 4: Stock Price Performance vs IHSG Benchmark
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    ax1.plot(stock_df["Date"], stock_df["ICBP_Base100"], color=NAVY, linewidth=2, label="ICBP.JK (Base 100 = IPO)")
    ax1.plot(stock_df["Date"], stock_df["IHSG_Base100"], color=GRAY, linewidth=1.5, linestyle="--", label="IHSG / IDX Benchmark (Base 100)")
    ax1.set_title("ICBP vs IHSG Benchmark: Performance Since IPO (Oct 2010 - Oct 2026)", fontsize=13, fontweight='bold', pad=10, color=NAVY)
    ax1.set_ylabel("Normalized Index (Base 100)", fontsize=10, fontweight='bold')
    ax1.legend(loc="upper left", frameon=True, facecolor="white")
    
    # Lower subplot: 1-Year Rolling Beta
    ax2.plot(stock_df["Date"], stock_df["ICBP_Beta_1Y"], color=TEAL, linewidth=1.2, label="1Y Rolling Beta vs IHSG")
    ax2.axhline(y=1.0, color=CRIMSON, linestyle=":", alpha=0.7)
    ax2.axhline(y=0.58, color=TEAL, linestyle="--", alpha=0.7, label="Latest Beta: 0.58")
    ax2.set_ylabel("Beta", fontsize=10, fontweight='bold')
    ax2.set_ylim(0.0, 1.5)
    ax2.legend(loc="upper right", frameon=True, facecolor="white")
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "04_stock_performance_vs_ihsg.png"))
    plt.close()

    # -------------------------------------------------------------
    # Figure 5: Historical Valuation Multiples (P/E and EV/EBITDA)
    # -------------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    
    l1 = ax1.plot(val_df["Year"], val_df["P_E_x"], color=NAVY, marker='o', linewidth=2.2, label="P/E Multiple (x)")
    l2 = ax2.plot(val_df["Year"], val_df["EV_EBITDA_x"], color=AMBER, marker='s', linewidth=2.2, linestyle="--", label="EV/EBITDA (x)")
    
    # 15-year median PE
    med_pe = val_df["P_E_x"].median()
    ax1.axhline(y=med_pe, color=NAVY, linestyle=":", alpha=0.6, label=f"15Y Median P/E: {med_pe:.1f}x")
    
    lines = l1 + l2
    labels = [l.get_label() for l in lines] + [f"15Y Median P/E ({med_pe:.1f}x)"]
    ax1.legend(lines, labels, loc="upper right", frameon=True, facecolor="white")
    
    ax1.set_title("ICBP Historical Valuation Multiples: Trading at Decadal Trough (2010 - 2025)", fontsize=13, fontweight='bold', pad=12, color=NAVY)
    ax1.set_xlabel("Fiscal Year", fontsize=11)
    ax1.set_ylabel("Price-to-Earnings (x)", fontsize=11, fontweight='bold', color=NAVY)
    ax2.set_ylabel("EV / EBITDA (x)", fontsize=11, fontweight='bold', color=AMBER)
    ax1.set_xticks(val_df["Year"])
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "05_valuation_multiples_history.png"))
    plt.close()

    # -------------------------------------------------------------
    # Figure 6: Peer Comparison Relative Valuation Bar Chart
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    
    # Bar Chart 1: P/E Trailing
    colors = [NAVY if t == "ICBP.JK" else GRAY for t in peer_df["Ticker"]]
    ax1.barh(peer_df["Ticker"], peer_df["P_E_Trailing_x"], color=colors, height=0.55)
    for i, v in enumerate(peer_df["P_E_Trailing_x"]):
        ax1.text(v + 0.3, i, f"{v:.1f}x", va='center', fontweight='bold', fontsize=9)
    ax1.set_title("Trailing P/E Multiple (x)", fontsize=11, fontweight='bold', color=NAVY)
    ax1.set_xlim(0, 18)
    
    # Bar Chart 2: Operating Margin vs ROE
    bar_h = 0.35
    y_ind = np.arange(len(peer_df))
    ax2.barh(y_ind - bar_h/2, peer_df["Operating_Margin_%"], height=bar_h, color=TEAL, label="Operating Margin (%)")
    ax2.barh(y_ind + bar_h/2, peer_df["ROE_%"], height=bar_h, color=AMBER, label="ROE (%)")
    ax2.set_yticks(y_ind)
    ax2.set_yticklabels(peer_df["Ticker"])
    ax2.set_title("Operating Margin & ROE (%)", fontsize=11, fontweight='bold', color=NAVY)
    ax2.legend(frameon=True, facecolor="white", loc="lower right")
    ax2.set_xlim(0, 45)
    
    plt.suptitle("Peer Relative Valuation & Operating Efficiency Comparison", fontsize=13, fontweight='bold', y=1.02, color=NAVY)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "06_peer_comparison_matrix.png"))
    plt.close()

    # -------------------------------------------------------------
    # Figure 7: Wheat Commodity Spike vs Gross Margin Sensitivity
    # -------------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    
    l1 = ax1.plot(macro_df["Year"], macro_df["Avg_Wheat_USd_bu"], color=CRIMSON, marker='o', linewidth=2.2, label="Wheat Futures (USd/bu)")
    gross_margin_series = (fin_df["GrossProfit"] / fin_df["Revenue"]) * 100.0
    l2 = ax2.plot(macro_df["Year"], gross_margin_series, color=NAVY, marker='s', linewidth=2.5, label="ICBP Gross Margin (%)")
    
    ax1.set_title("Raw Material Commodity Sensitivity: Wheat Spikes vs ICBP Gross Margin", fontsize=13, fontweight='bold', pad=12, color=NAVY)
    ax1.set_xlabel("Fiscal Year", fontsize=11)
    ax1.set_ylabel("Wheat Futures Price (USd/bushel)", fontsize=11, fontweight='bold', color=CRIMSON)
    ax2.set_ylabel("ICBP Gross Margin (%)", fontsize=11, fontweight='bold', color=NAVY)
    ax1.set_xticks(macro_df["Year"])
    
    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="lower left", frameon=True, facecolor="white")
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "07_macro_commodity_correlation.png"))
    plt.close()

    # -------------------------------------------------------------
    # Figure 8: DCF Football Field Valuation Chart
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 4.5))
    scenarios = ["Current Price", "Bear Case", "Base Case", "Bull Case"]
    values = [5575.0, 11674.0, 23368.0, 43464.0]
    bar_colors = [GRAY, AMBER, NAVY, TEAL]
    
    bars = ax.barh(scenarios, values, color=bar_colors, height=0.55)
    for b in bars:
        w = b.get_width()
        ax.text(w + 500, b.get_y() + b.get_height()/2, f"Rp {w:,.0f}", va='center', fontweight='bold', fontsize=10)
        
    ax.axvline(x=5575.0, color=CRIMSON, linestyle="--", linewidth=1.5, alpha=0.8, label="Current Market Price (Rp 5,575)")
    ax.set_title("ICBP DCF Intrinsic Value Range vs Market Price (Football Field)", fontsize=13, fontweight='bold', pad=12, color=NAVY)
    ax.set_xlabel("Intrinsic Value per Share (IDR)", fontsize=11, fontweight='bold')
    ax.set_xlim(0, 52000)
    ax.legend(frameon=True, facecolor="white", loc="lower right")
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "08_dcf_valuation_football_field.png"))
    plt.close()

    # -------------------------------------------------------------
    # Figure 9: Business Segment Revenue Breakdown
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    
    # Division Pie
    div_labels = ["Noodles", "Dairy", "Snacks", "Seasonings", "Nutrition", "Beverages"]
    div_rev_2024 = [53870.1, 9661.8, 4539.5, 4301.1, 1357.7, 1674.3]
    colors_pie = [NAVY, BLUE, LIGHT_BLUE, TEAL, AMBER, GRAY]
    ax1.pie(div_rev_2024, labels=div_labels, autopct='%1.1f%%', startangle=140, colors=colors_pie, explode=(0.05, 0, 0, 0, 0, 0))
    ax1.set_title("Revenue by Product Segment (FY2024)", fontsize=11, fontweight='bold', color=NAVY)
    
    # Geographic expansion stack
    years = seg_df["Year"]
    dom = seg_df["Domestic_Sales_IDR_B"] / 1000.0
    intl = seg_df["Overseas_Sales_IDR_B"] / 1000.0
    ax2.bar(years, dom, label="Domestic Indonesia", color=NAVY, width=0.6)
    ax2.bar(years, intl, bottom=dom, label="Overseas (Pinehill Markets)", color=AMBER, width=0.6)
    ax2.set_title("Geographic Sales Expansion (IDR Trillion)", fontsize=11, fontweight='bold', color=NAVY)
    ax2.set_ylabel("IDR Trillion", fontsize=10, fontweight='bold')
    ax2.legend(frameon=True, facecolor="white", loc="upper left")
    
    plt.suptitle("ICBP Segment Dominance & International Pinehill Footprint", fontsize=13, fontweight='bold', y=1.02, color=NAVY)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "09_segment_geographic_breakdown.png"))
    plt.close()

    # -------------------------------------------------------------
    # Figure 10: Technical Indicators (Price, RSI, Drawdown)
    # -------------------------------------------------------------
    fig, (tax1, tax2, tax3) = plt.subplots(3, 1, figsize=(11, 8), sharex=True, gridspec_kw={'height_ratios': [2.5, 1.2, 1.2]})
    
    # 1. Price + MAs
    tax1.plot(stock_df["Date"], stock_df["ICBP_Close"], label="ICBP Close (IDR)", color=NAVY, linewidth=1.5)
    tax1.plot(stock_df["Date"], stock_df["ICBP_SMA_50"], label="50-Day SMA", color=AMBER, linewidth=1.2, linestyle="--")
    tax1.plot(stock_df["Date"], stock_df["ICBP_SMA_200"], label="200-Day SMA", color=TEAL, linewidth=1.2, linestyle=":")
    tax1.set_title("ICBP Technical Structure: Multi-Year Moving Averages, RSI & Drawdown", fontsize=13, fontweight='bold', pad=10, color=NAVY)
    tax1.set_ylabel("Price (IDR)", fontsize=10, fontweight='bold')
    tax1.legend(frameon=True, loc="upper left", facecolor="white")
    
    # 2. RSI 14
    if "ICBP_RSI_14" in stock_df.columns:
        tax2.plot(stock_df["Date"], stock_df["ICBP_RSI_14"], color=BLUE, linewidth=1.2)
        tax2.axhline(70, color=CRIMSON, linestyle="--", alpha=0.7, label="Overbought (70)")
        tax2.axhline(30, color=TEAL, linestyle="--", alpha=0.7, label="Oversold (30)")
        tax2.fill_between(stock_df["Date"], 30, 70, color=GRAY, alpha=0.1)
        tax2.set_ylabel("14D RSI", fontsize=10, fontweight='bold')
        tax2.set_ylim(10, 90)
        tax2.legend(frameon=True, loc="upper right", facecolor="white")
        
    # 3. Drawdown %
    if "ICBP_Drawdown_%" in stock_df.columns:
        tax3.plot(stock_df["Date"], stock_df["ICBP_Drawdown_%"], color=CRIMSON, linewidth=1.2, label="Drawdown from Peak (%)")
        tax3.fill_between(stock_df["Date"], stock_df["ICBP_Drawdown_%"], 0, color=CRIMSON, alpha=0.2)
        tax3.set_ylabel("Drawdown (%)", fontsize=10, fontweight='bold')
        tax3.set_xlabel("Date", fontsize=10)
        tax3.legend(frameon=True, loc="lower left", facecolor="white")
        
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "10_technical_rsi_drawdown.png"))
    plt.close()

    # -------------------------------------------------------------
    # Figure 11: Historical Valuation Multiples Percentile Range
    # -------------------------------------------------------------
    range_path = os.path.join(BASE_DIR, "data", "processed", "icbp_valuation_multiples_range_stats.csv")
    if os.path.exists(range_path):
        vr_df = pd.read_csv(range_path)
        fig, vax = plt.subplots(figsize=(10, 5))
        
        # Plot P/E, P/BV, EV/EBITDA, EV/Sales discounts
        v_sub = vr_df[vr_df["Valuation_Multiple"].isin(["P_E_x", "P_BV_x", "EV_EBITDA_x", "EV_EBIT_x", "EV_Sales_x", "P_FCF_x"])]
        mult_names = v_sub["Valuation_Multiple"].str.replace("_x", "").values
        discounts = v_sub["Discount_To_Median_%"].values
        
        bars = vax.bar(mult_names, discounts, color=CRIMSON, width=0.55, alpha=0.85)
        for b in bars:
            h = b.get_height()
            vax.text(b.get_x() + b.get_width()/2, h - 5, f"{h:.1f}%", ha='center', va='top', color='white', fontweight='bold', fontsize=10)
            
        vax.axhline(0, color=NAVY, linewidth=1.2)
        vax.set_title("ICBP Current Valuation Multiple Discount vs 16-Year Historical Median\nTrading at Unprecedented 50% - 67% Discounts across Multiples", fontsize=12, fontweight='bold', pad=12, color=NAVY)
        vax.set_ylabel("Discount to Historical Median (%)", fontsize=10, fontweight='bold')
        vax.set_ylim(-80, 10)
        plt.tight_layout()
        fig.savefig(os.path.join(FIGURES_DIR, "11_valuation_discount_to_historical_median.png"))
        plt.close()

    print(f"All 11 institutional research figures successfully generated in: {FIGURES_DIR}")

if __name__ == "__main__":
    plot_all_figures()
