"""
app.py - IDX Equity Research & Valuation Intelligence Dashboard
PT Indofood CBP Sukses Makmur Tbk (IDX: ICBP)
An institutional-grade equity research, financial modeling, and DCF valuation application.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="ICBP Equity Research & Valuation Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0F172A;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
    }
    .badge-buy {
        background-color: #10B981;
        color: white;
        padding: 0.25rem 0.6rem;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading with Caching ---
@st.cache_data
def load_all_data():
    candidate_map = {
        "fin_metrics": [
            "results/data_tables/financial_metrics.csv",
            "data/processed/financial_metrics.csv"
        ],
        "fin_annual": [
            "results/data_tables/icbp_financial_statements_annual_2010_2025.csv",
            "data/processed/icbp_financial_statements_annual_2010_2025.csv"
        ],
        "fin_ratios": [
            "results/data_tables/icbp_financial_ratios_2010_2025.csv",
            "data/processed/icbp_financial_ratios_2010_2025.csv"
        ],
        "segments": [
            "results/data_tables/icbp_segments_geography_breakdown.csv",
            "data/processed/icbp_segments_geography_breakdown.csv"
        ],
        "segment_ts": [
            "results/data_tables/06_master_revenue_dataset_timeseries.csv",
            "thesis_data/06_master_revenue_dataset_timeseries.csv",
            "data/processed/06_master_revenue_dataset_timeseries.csv"
        ],
        "peers": [
            "results/data_tables/peers_financials_valuation_comparison.csv",
            "data/processed/peers_financials_valuation_comparison.csv"
        ],
        "stock": [
            "results/data_tables/stock_performance.csv",
            "data/processed/stock_performance.csv"
        ],
        "macro": [
            "results/data_tables/macro_economic_environment_2010_2025.csv",
            "data/processed/macro_economic_environment_2010_2025.csv"
        ],
        "forecasts": [
            "results/data_tables/07_financial_forecasts_2026_2030.csv",
            "thesis_data/07_financial_forecasts_2026_2030.csv"
        ],
        "dcf_sens": [
            "results/data_tables/08_dcf_sensitivity_matrix.csv",
            "thesis_data/08_dcf_sensitivity_matrix.csv"
        ]
    }
    dfs = {}
    for k, candidates in candidate_map.items():
        found_df = None
        for p in candidates:
            if os.path.exists(p):
                found_df = pd.read_csv(p)
                break
        dfs[k] = found_df if found_df is not None else pd.DataFrame()
    return dfs

data = load_all_data()

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/combo-chart--v1.png", width=60)
    st.title("ICBP Research Suite")
    st.caption("**IDX: ICBP.JK** | Consumer Non-Cyclicals")
    st.markdown("---")
    
    st.markdown("### Analyst Recommendation")
    st.markdown("## <span class='badge-buy'>CONVICTION BUY</span>", unsafe_allow_html=True)
    st.metric("12M Target Price", "IDR 24,582", "+325.7% Upside")
    st.caption("Current Price: IDR 5,775 | 52W Range: 5,400 - 8,725")
    st.markdown("---")
    
    nav_choice = st.radio(
        "Navigation",
        [
            "Executive Overview & Thesis",
            "Financial Statements & Trajectory",
            "Segment & Pinehill Global Footprint",
            "Interactive DCF Valuation",
            "Peer Benchmarking & Multiples",
            "Stock Technicals & Momentum",
            "Macro & Input Cost Sensitivity",
            "Equity Research Initiation Report"
        ]
    )
    
    st.markdown("---")
    st.caption("© 2026 Antigravity Research | IDX Equity Research Intelligence")

# ==============================================================================
# TAB 1: EXECUTIVE OVERVIEW & INVESTMENT THESIS
# ==============================================================================
if nav_choice == "Executive Overview & Thesis":
    st.markdown("<div class='main-header'>PT Indofood CBP Sukses Makmur Tbk (IDX: ICBP)</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Global Consumer Staples Powerhouse | Equity Research Initiation & Valuation Intelligence</div>", unsafe_allow_html=True)
    
    # Top KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("<div class='metric-card'><div class='metric-label'>Target Price</div><div class='metric-value'>Rp 24,582</div><small style='color:#10B981;font-weight:600;'>+325.7% Upside</small></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><div class='metric-label'>Current Price</div><div class='metric-value'>Rp 5,775</div><small>Market Cap: Rp 67.3T</small></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><div class='metric-label'>Trailing P/E</div><div class='metric-value'>7.91x</div><small style='color:#10B981;'>-65.8% to 15Y Median</small></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-card'><div class='metric-label'>EV / EBITDA</div><div class='metric-value'>4.64x</div><small style='color:#10B981;'>-62.3% to 15Y Median</small></div>", unsafe_allow_html=True)
    with col5:
        st.markdown("<div class='metric-card'><div class='metric-label'>Dividend Yield</div><div class='metric-value'>4.75%</div><small>DPR: 35% - 50%</small></div>", unsafe_allow_html=True)
    
    st.markdown("### Core Investment Pillars")
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.info("**1. Unassailable Moat**\n\nControls >70% of Indonesia's instant noodle market via *Indomie*. Reaches >500,000 retail warungs across 17,000 islands through Indomarco Adi Prima (IAP).")
    with t2:
        st.info("**2. Pinehill Global Engine**\n\nPinehill Company Ltd ($3.0B acquisition) expanded reach across Middle East & Africa (>885M consumers). International sales grew from 10.8% to 32.1%.")
    with t3:
        st.info("**3. Decadal Valuation Mispricing**\n\nTrading at 7.9x Trailing P/E and 4.6x EV/EBITDA (0th percentile rank). The market penalizes non-cash USD FX paper loss while ignoring resilient operational cash flow.")
    with t4:
        st.info("**4. High-Yield Cash Compounder**\n\nGenerates >IDR 12 Trillion in annual operating cash flow with FCF conversion >100%. Free cash flow will fully eliminate net debt within 2 years.")
        
    st.markdown("### 15-Year Financial Compounding Trajectory (2010 - 2025)")
    if not data["fin_annual"].empty:
        df_fin = data["fin_annual"]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=df_fin["Year"], y=df_fin["Revenue"], name="Revenue (IDR B)", marker_color="#1E3A8A"), secondary_y=False)
        fig.add_trace(go.Bar(x=df_fin["Year"], y=df_fin["GrossProfit"], name="Gross Profit (IDR B)", marker_color="#3B82F6"), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_fin["Year"], y=df_fin["NetIncome"], name="Net Income (IDR B)", line=dict(color="#10B981", width=3)), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_fin["Year"], y=df_fin["EBIT"] / df_fin["Revenue"] * 100, name="Operating Margin (%)", line=dict(color="#F59E0B", width=2.5, dash="dot")), secondary_y=True)
        fig.update_layout(title="Revenue, Profitability, and Margin Expansion (2010 - 2025)", hovermode="x unified", height=450, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        fig.update_yaxes(title_text="IDR Billion", secondary_y=False)
        fig.update_yaxes(title_text="Operating Margin (%)", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# TAB 2: FINANCIAL STATEMENTS & TRAJECTORY
# ==============================================================================
elif nav_choice == "Financial Statements & Trajectory":
    st.markdown("<div class='main-header'>15-Year Historical Financial Performance</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Audited Financial Statements, Margin Trajectory, and Balance Sheet Quality (2010 - 2025 + 9M26)</div>", unsafe_allow_html=True)
    
    if not data["fin_metrics"].empty:
        df_m = data["fin_metrics"]
        
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            metric_view = st.selectbox("Select Ratio Category", ["Profitability Margins (%)", "Returns on Capital (%)", "Solvency & Leverage", "Cash Flow & Capital Discipline"])
        
        if metric_view == "Profitability Margins (%)":
            fig = px.line(
                df_m, x="Year",
                y=["GrossProfitMargin_%", "EBITMargin_%", "EBITDAMargin_%", "NetProfitMargin_%"],
                markers=True,
                title="Historical Margin Evolution (2010 - 2025)",
                labels={"value": "Margin (%)", "variable": "Metric"}
            )
            fig.update_layout(height=420, hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
            
        elif metric_view == "Returns on Capital (%)":
            fig = px.line(
                df_m, x="Year",
                y=["ROIC_%", "ROE_%", "ROA_%"],
                markers=True,
                title="Return on Invested Capital (ROIC), ROE, and ROA",
                labels={"value": "Return (%)", "variable": "Metric"}
            )
            fig.update_layout(height=420, hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
            
        elif metric_view == "Solvency & Leverage":
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(x=df_m["Year"], y=df_m["TotalDebt"], name="Total Debt (IDR B)", marker_color="#EF4444"), secondary_y=False)
            fig.add_trace(go.Bar(x=df_m["Year"], y=df_m["Cash"], name="Cash & Equivalents (IDR B)", marker_color="#10B981"), secondary_y=False)
            fig.add_trace(go.Scatter(x=df_m["Year"], y=df_m["NetDebtToEBITDA_x"], name="Net Debt to EBITDA (x)", line=dict(color="#1E3A8A", width=3)), secondary_y=True)
            fig.update_layout(title="Debt Profile and Deleveraging Trajectory (Pinehill Absorption)", hovermode="x unified", height=420)
            st.plotly_chart(fig, use_container_width=True)
            
        elif metric_view == "Cash Flow & Capital Discipline":
            fig = px.bar(
                df_m, x="Year",
                y=["CFO", "Capex", "FreeCashFlow"],
                barmode="group",
                title="Operating Cash Flow (CFO), Capex, and Free Cash Flow Generation",
                labels={"value": "IDR Billion", "variable": "Cash Flow Item"}
            )
            fig.update_layout(height=420, hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
            
        st.markdown("### Audited Historical Financial Table (IDR Billion)")
        st.dataframe(df_m.set_index("Year").round(2), use_container_width=True)

# ==============================================================================
# TAB 3: SEGMENT & PINEHILL GLOBAL FOOTPRINT
# ==============================================================================
elif nav_choice == "Segment & Pinehill Global Footprint":
    st.markdown("<div class='main-header'>Operating Segments & Global Footprint</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Decomposition of 6 Business Units and the Pinehill International Transformation</div>", unsafe_allow_html=True)
    
    if not data["segment_ts"].empty:
        df_seg = data["segment_ts"]
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Segment Revenue Composition (2010 - 2026)")
            fig_seg = px.area(
                df_seg, x="Year",
                y=["Noodles_Rev", "Dairy_Rev", "Snacks_Rev", "Seasonings_Rev", "Nutrition_Rev", "Beverages_Rev"],
                title="Gross Revenue Breakdown by Division (IDR Billion)",
                labels={"value": "IDR Billion", "variable": "Division"}
            )
            fig_seg.update_layout(height=400, hovermode="x unified")
            st.plotly_chart(fig_seg, use_container_width=True)
            
        with c2:
            st.markdown("#### Geographic Transformation: Domestic vs Global")
            fig_geo = px.bar(
                df_seg, x="Year",
                y=["Domestic_Rev", "Overseas_Rev"],
                title="Domestic (Indonesia) vs International (Pinehill / Global) Sales",
                barmode="stack",
                labels={"value": "IDR Billion", "variable": "Geographic Region"}
            )
            fig_geo.update_layout(height=400, hovermode="x unified")
            st.plotly_chart(fig_geo, use_container_width=True)
            
        st.markdown("#### Division Operating Profitability (EBIT Margin %)")
        fig_m = px.line(
            df_seg, x="Year",
            y=["Noodles_Margin_%", "Dairy_Margin_%", "Snacks_Margin_%", "Seasonings_Margin_%", "Nutrition_Margin_%", "Beverages_Margin_%"],
            markers=True,
            title="EBIT Margin Trajectory by Division (%)"
        )
        fig_m.update_layout(height=400, hovermode="x unified")
        st.plotly_chart(fig_m, use_container_width=True)
        
        st.info("""
        **Strategic Takeaway on Segment Economics:**
        * **Noodles (Mi Instan)**: Generates **71.9% of gross revenue** and **86.9% of total operating profit** with stable 24%–26% EBIT margins.
        * **Pinehill Impact**: International sales surged from **10.8% in 2019** to **32.1% in 1H 2026**. Non-current productive assets in foreign markets represent **65.0% of total non-current assets** (IDR 55.7 Trillion).
        * **Turnaround Story**: Beverages turned from -20% operating loss in 2016 to solid 12%–15% EBIT profitability.
        """)

# ==============================================================================
# TAB 4: INTERACTIVE DCF VALUATION & SCENARIOS
# ==============================================================================
elif nav_choice == "Interactive DCF Valuation":
    st.markdown("<div class='main-header'>Interactive Discounted Cash Flow (DCF) Model</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Dynamic Two-Stage FCFF Valuation with Real-Time Scenario Sliders</div>", unsafe_allow_html=True)
    
    # Preset scenarios
    preset = st.radio("Select Pre-Configured Scenario:", ["Base Case (Consensus / Target)", "Bear Case (Downside Stagnation)", "Bull Case (Pinehill Acceleration)"], horizontal=True)
    
    if preset == "Base Case (Consensus / Target)":
        def_wacc, def_g, def_rev_g, def_ebit_m = 8.10, 3.50, 7.50, 21.80
    elif preset == "Bear Case (Downside Stagnation)":
        def_wacc, def_g, def_rev_g, def_ebit_m = 8.80, 2.50, 4.00, 18.40
    else:
        def_wacc, def_g, def_rev_g, def_ebit_m = 7.40, 4.20, 9.70, 23.10
        
    st.markdown("#### Valuation Parameters")
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        wacc_input = st.slider("WACC / Discount Rate (%)", 6.5, 11.0, float(def_wacc), 0.1)
    with sc2:
        terminal_g_input = st.slider("Terminal Growth Rate g (%)", 1.5, 5.0, float(def_g), 0.1)
    with sc3:
        rev_cagr_input = st.slider("5-Yr Revenue CAGR (%)", 3.0, 14.0, float(def_rev_g), 0.1)
    with sc4:
        ebit_margin_input = st.slider("Average EBIT Margin (%)", 16.0, 26.0, float(def_ebit_m), 0.1)
        
    # Real-Time DCF Computation
    shares = 11661.908  # M shares
    current_px = 5775.0
    net_debt = 17969.9
    tax_rate = 0.22
    dna_pct = 0.026
    capex_pct = 0.038
    nwc_pct = 0.08
    
    wacc_dec = wacc_input / 100.0
    tg_dec = terminal_g_input / 100.0
    
    # 5-Year Forecast
    prior_rev = 74850.9
    fcff_list = []
    pv_fcff_list = []
    df_forecast = []
    
    for t in range(1, 6):
        r = prior_rev * (1.0 + (rev_cagr_input / 100.0))
        eb = r * (ebit_margin_input / 100.0)
        nopat = eb * (1.0 - tax_rate)
        dna = r * dna_pct
        capex = r * capex_pct
        dnwc = (r - prior_rev) * nwc_pct
        fcff = nopat + dna - capex - dnwc
        df = 1.0 / ((1.0 + wacc_dec) ** t)
        pv = fcff * df
        
        fcff_list.append(fcff)
        pv_fcff_list.append(pv)
        df_forecast.append({
            "Year": f"Year +{t}",
            "Revenue": round(r, 1),
            "EBIT": round(eb, 1),
            "NOPAT": round(nopat, 1),
            "D&A": round(dna, 1),
            "Capex": round(capex, 1),
            "Delta_NWC": round(dnwc, 1),
            "FCFF": round(fcff, 1),
            "PV_FCFF": round(pv, 1)
        })
        prior_rev = r
        
    sum_pv_fcff = sum(pv_fcff_list)
    term_fcff = fcff_list[-1] * (1.0 + tg_dec)
    
    if wacc_dec > tg_dec:
        tv = term_fcff / (wacc_dec - tg_dec)
        pv_tv = tv / ((1.0 + wacc_dec) ** 5)
        ev = sum_pv_fcff + pv_tv
        eq_val = ev - net_debt
        target_px = (eq_val * 1000.0) / shares
        upside = ((target_px / current_px) - 1.0) * 100.0
    else:
        target_px, upside, ev, eq_val, pv_tv = 0, 0, 0, 0, 0

    st.markdown("---")
    res_c1, res_c2, res_c3, res_c4 = st.columns(4)
    with res_c1:
        st.metric("Intrinsic Target Price", f"IDR {target_px:,.0f}", f"{upside:+.1f}% vs Current")
    with res_c2:
        st.metric("Enterprise Value (EV)", f"IDR {ev:,.1f} B", f"TV: {pv_tv/ev*100:.1f}% of EV")
    with res_c3:
        st.metric("Equity Value", f"IDR {eq_val:,.1f} B", f"Net Debt: IDR {net_debt:,.1f} B")
    with res_c4:
        st.metric("5-Year Cumulative FCFF", f"IDR {sum(fcff_list):,.1f} B", "High Cash Generation")
        
    st.markdown("#### Projected 5-Year Free Cash Flow Waterfall (IDR Billion)")
    st.dataframe(pd.DataFrame(df_forecast).set_index("Year"), use_container_width=True)
    
    # Sensitivity Heatmap
    st.markdown("#### 2-Way Valuation Sensitivity Heatmap: WACC vs Terminal Growth ($g$)")
    if not data["dcf_sens"].empty:
        df_hm = data["dcf_sens"].set_index("WACC_%")
        fig_hm = px.imshow(
            df_hm,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Viridis",
            labels=dict(x="Terminal Growth Rate (g)", y="WACC (%)", color="Target Price (Rp)"),
            title="Target Price Matrix Across WACC & Terminal Growth Combinations"
        )
        st.plotly_chart(fig_hm, use_container_width=True)

# ==============================================================================
# TAB 5: PEER VALUATION & BENCHMARKING
# ==============================================================================
elif nav_choice == "Peer Benchmarking & Multiples":
    st.markdown("<div class='main-header'>Peer Benchmarking & Multiples Comparison</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Comparative Financial Quality: ICBP vs MYOR, UNVR, INDF, CMRY</div>", unsafe_allow_html=True)
    
    if not data["peers"].empty:
        df_p = data["peers"]
        
        p1, p2 = st.columns(2)
        with p1:
            fig_pe = px.bar(
                df_p, x="Ticker", y=["P_E_Trailing_x", "P_E_Forward_x"],
                barmode="group", title="Trailing vs Forward P/E Comparison (x)",
                labels={"value": "P/E Multiple (x)", "variable": "Multiple"}
            )
            fig_pe.update_layout(height=400)
            st.plotly_chart(fig_pe, use_container_width=True)
            
        with p2:
            fig_opm = px.scatter(
                df_p, x="Operating_Margin_%", y="P_E_Forward_x",
                size="Market_Cap_IDR_Trillion", text="Ticker",
                color="Ticker",
                title="Valuation Disconnect: Forward P/E vs Operating Margin (%)",
                labels={"Operating_Margin_%": "Operating Margin (%)", "P_E_Forward_x": "Forward P/E Multiple"}
            )
            fig_opm.update_traces(textposition="top center")
            fig_opm.update_layout(height=400)
            st.plotly_chart(fig_opm, use_container_width=True)
            
        st.markdown("### Comparative Peer Matrix")
        st.dataframe(df_p.set_index("Ticker"), use_container_width=True)

# ==============================================================================
# TAB 6: STOCK PERFORMANCE & TECHNICALS
# ==============================================================================
elif nav_choice == "Stock Technicals & Momentum":
    st.markdown("<div class='main-header'>Stock Performance, Volatility & Technicals</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Price Action, Moving Averages, RSI 14, MACD, and Drawdown Profile</div>", unsafe_allow_html=True)
    
    if not data["stock"].empty:
        df_stk = data["stock"].tail(500)
        
        # Price and Moving Averages
        fig_px = go.Figure()
        fig_px.add_trace(go.Scatter(x=df_stk["Date"], y=df_stk["ICBP_Close"], name="Close Price", line=dict(color="#1E3A8A", width=2)))
        fig_px.add_trace(go.Scatter(x=df_stk["Date"], y=df_stk["ICBP_SMA_20"], name="SMA 20", line=dict(color="#F59E0B", width=1.5)))
        fig_px.add_trace(go.Scatter(x=df_stk["Date"], y=df_stk["ICBP_SMA_50"], name="SMA 50", line=dict(color="#10B981", width=1.5)))
        fig_px.add_trace(go.Scatter(x=df_stk["Date"], y=df_stk["ICBP_SMA_200"], name="SMA 200", line=dict(color="#EF4444", width=2)))
        fig_px.update_layout(title="ICBP Price Action with 20/50/200-Day Moving Averages", hovermode="x unified", height=450)
        st.plotly_chart(fig_px, use_container_width=True)
        
        # Momentum Oscillators
        tc1, tc2 = st.columns(2)
        with tc1:
            fig_rsi = px.line(df_stk, x="Date", y="ICBP_RSI_14", title="14-Day RSI (Relative Strength Index)")
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
            fig_rsi.update_layout(height=350)
            st.plotly_chart(fig_rsi, use_container_width=True)
            
        with tc2:
            fig_dd = px.area(df_stk, x="Date", y="ICBP_Drawdown_%", title="Historical Drawdown Profile (%)", color_discrete_sequence=["#EF4444"])
            fig_dd.update_layout(height=350)
            st.plotly_chart(fig_dd, use_container_width=True)

# ==============================================================================
# TAB 7: MACRO & INPUT COST SENSITIVITY
# ==============================================================================
elif nav_choice == "Macro & Input Cost Sensitivity":
    st.markdown("<div class='main-header'>Macroeconomic & Commodity Exposure</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>External Environment: Inflation, USD/IDR FX, Wheat, CPO, and Interest Rates</div>", unsafe_allow_html=True)
    
    if not data["macro"].empty:
        df_mc = data["macro"]
        
        mc1, mc2 = st.columns(2)
        with mc1:
            fig_cpi = make_subplots(specs=[[{"secondary_y": True}]])
            fig_cpi.add_trace(go.Scatter(x=df_mc["Year"], y=df_mc["Inflation_YoY_%"], name="Headline Inflation (%)", line=dict(color="#EF4444", width=2.5)), secondary_y=False)
            fig_cpi.add_trace(go.Scatter(x=df_mc["Year"], y=df_mc["BI_Rate_%"], name="BI Rate (%)", line=dict(color="#1E3A8A", width=2.5, dash="dash")), secondary_y=False)
            fig_cpi.add_trace(go.Scatter(x=df_mc["Year"], y=df_mc["Avg_USD_IDR"], name="USD/IDR", line=dict(color="#10B981", width=2)), secondary_y=True)
            fig_cpi.update_layout(title="Inflation, BI-Rate, and USD/IDR Exchange Rate", height=400, hovermode="x unified")
            st.plotly_chart(fig_cpi, use_container_width=True)
            
        with mc2:
            fig_cmd = make_subplots(specs=[[{"secondary_y": True}]])
            fig_cmd.add_trace(go.Scatter(x=df_mc["Year"], y=df_mc["Avg_Wheat_USd_bu"], name="Wheat (USc/bu)", line=dict(color="#F59E0B", width=2.5)), secondary_y=False)
            fig_cmd.add_trace(go.Scatter(x=df_mc["Year"], y=df_mc["Avg_CPO_USD_MT"], name="CPO (USD/MT)", line=dict(color="#10B981", width=2.5)), secondary_y=True)
            fig_cmd.update_layout(title="Raw Material Costs: Wheat & Crude Palm Oil (CPO)", height=400, hovermode="x unified")
            st.plotly_chart(fig_cmd, use_container_width=True)
            
        st.info("""
        **Key Macro Insights:**
        * **Wheat & CPO Input Hedge**: Bogasari (INDF parent) and SIMP (Salim Ivomas) guarantee 100% physical procurement integrity with 3-4 months inventory lag.
        * **USD 2.75B Bond Structure**: All global bonds have fixed coupons (3.399% to 5.415%) with principal due in 2031, 2032, and 2051. Short-term IDR depreciation produces only non-cash paper losses without impacting operating cash flow.
        """)

# ==============================================================================
# TAB 8: EQUITY RESEARCH INITIATION REPORT
# ==============================================================================
elif nav_choice == "Equity Research Initiation Report":
    st.markdown("<div class='main-header'>Institutional Equity Research Report</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Full Initiation of Coverage Dossier & Investment Thesis</div>", unsafe_allow_html=True)
    
    report_candidates = [
        "results/reports/equity_research_report.md",
        "reports/equity_research_report.md"
    ]
    report_path = None
    for p in report_candidates:
        if os.path.exists(p):
            report_path = p
            break
            
    if report_path:
        with open(report_path, "r", encoding="utf-8") as f:
            report_text = f.read()
        # Ensure image paths resolve in Streamlit web app
        report_text = report_text.replace("figures/", "results/figures/").replace("../results/figures/", "results/figures/")
        st.markdown(report_text)
    else:
        st.warning("Equity Research Report file not found in results/reports/equity_research_report.md")
