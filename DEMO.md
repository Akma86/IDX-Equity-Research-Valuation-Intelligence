# Interactive Demo Walkthrough & Valuation Intelligence Guide

This guide provides a structured walkthrough of the **IDX Equity Research & Valuation Intelligence Suite** for **PT Indofood CBP Sukses Makmur Tbk (IDX: ICBP)**. Use this document to reproduce analysis, navigate the interactive Streamlit dashboard, or record a video demonstration for your professional portfolio.

---

## ⚡ Option 1: 5-Second Headless CLI Demo

You can execute a complete institutional summary directly in your terminal without opening a browser:

```bash
python code/scripts/run_demo_cli.py
```

### CLI Demo Output Preview:
```text
================================================================================
  IDX EQUITY RESEARCH & VALUATION INTELLIGENCE SUITE: PT INDOFOOD CBP (ICBP)  
================================================================================
  Institutional Coverage & Dynamic Valuation Model (Audited 2010 - 2026)      
--------------------------------------------------------------------------------

[1] 15-YEAR COMPOUNDING TRAJECTORY (IPO 2010 -> FY2025):
  * Revenue:           IDR 17,960.1 B  -->  IDR 74,850.9 B  (CAGR: +9.98%)
  * Operating EBIT:    IDR 2,542.3 B   -->  IDR 16,655.5 B  (CAGR: +13.35%)
  * Net Income:        IDR 1,704.0 B   -->  IDR 9,224.9 B   (CAGR: +11.92%)
  * Operating Cash:    IDR 2,252.0 B   -->  IDR 12,104.4 B  (CAGR: +11.86%)
  * Balance Sheet:     IDR 13,361.3 B  -->  IDR 135,544.4 B (10.1x Expansion)

[2] PINEHILL GLOBAL M&A TRANSFORMATION:
  * Acquisition: $3.0 Billion acquisition in Aug 2020 (8 Middle East & Africa plants)
  * Addressable Population: >885 Million consumers across MENA & Sub-Saharan Africa
  * Overseas Revenue Share: Surged from 10.8% (2019) to 32.1% (1H 2026)
  * Foreign Non-Current Assets: IDR 55.7 Trillion (65.0% of total non-current assets)

[3] INTRINSIC VALUATION & FOOTBALL FIELD SUMMARY:
                Scenario  WACC     g Target Price  Upside Safety
  Bear Case (Stagnation) 8.80% 2.50%   IDR 12,659 +119.2%  54.4%
Base Case (Target Price) 8.10% 3.50%   IDR 24,582 +325.7%  76.5%
   Bull Case (Expansion) 7.40% 4.20%   IDR 40,673 +604.3%  85.8%

[4] CROSS-SECTIONAL PEER BENCHMARKING (IDX FMCG):
 Ticker               Company_Name  Operating_Margin_%  ROIC_%  P_E_Trailing_x  EV_EBITDA_x  Dividend_Yield_%
ICBP.JK Indofood CBP Sukses Makmur               23.91   21.42            8.63         5.71              4.47
MYOR.JK               Mayora Indah                8.81   14.07            8.56         4.92              4.58
UNVR.JK         Unilever Indonesia               16.94  162.25           15.69         9.96             16.40
INDF.JK     Indofood Sukses Makmur               19.96   21.70            5.53         4.15              4.39
CMRY.JK     Cisarua Mountain Dairy               17.89   29.64           15.98        12.25              4.93

================================================================================
  RECOMMENDATION: CONVICTION BUY | TARGET PRICE: IDR 24,582 (+325.7% UPSIDE)
================================================================================
```

---

## 🖥️ Option 2: Full Interactive Streamlit Dashboard Walkthrough

### 1. Launch the Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

### 2. Guided 8-Tab Exploration Script

#### 📊 Tab 1: Executive Overview & Thesis
- **Visuals:** 4 Top KPI metric cards (Current Price IDR 5,775, DCF Fair Value IDR 24,582, Implied Upside +325.7%, Trailing P/E 7.91x).
- **Key Takeaway:** Notice the 4 Investment Thesis Pillars detailing ICBP's moat, Pinehill compounding engine, valuation disconnect, and de-leveraging cash conversion.
- **Interaction:** Review the 15-year historical compounding chart comparing Revenue, EBIT, and CFO from IPO to FY2025.

#### 📈 Tab 2: Financial Statements & Trajectory
- **Visuals:** Revenue vs EBIT growth chart, Margin evolution (Gross, Operating, Net margins), Return on Invested Capital (ROIC vs ROE), and Cash Conversion (CFO vs Capex vs FCF).
- **Insight:** Observe how operating margin expanded from ~14% in 2010 to 22.3% in 2025 despite commodity shocks, proving formidable brand pricing power.

#### 🌍 Tab 3: Segment & Pinehill Global Footprint
- **Visuals:** Gross revenue breakdown by operating division (Noodles, Dairy, Snacks, Seasonings, Nutrition, Beverages) and geographic market shares.
- **Insight:** Check the overseas revenue metric surging from 10.8% in 2019 to 32.1% in 1H 2026, with foreign non-current assets reaching IDR 55.7 Trillion (65.0% of total).

#### 🧮 Tab 4: Interactive DCF Valuation Engine
- **Sliders:**
  - **WACC (%):** Drag from 8.10% down to 7.40% or up to 9.50%.
  - **Terminal Growth Rate (%):** Adjust from 1.5% to 5.0%.
  - **Revenue CAGR (%):** Adjust 5-year growth rates.
  - **Operating EBIT Margin (%):** Adjust margin sustainability.
- **Dynamic Output:** Fair value recalculates instantly in real-time, accompanied by a dynamic 2D Sensitivity Heatmap matrix ($WACC \times g$).

#### ⚖️ Tab 5: Peer Benchmarking & Multiples
- **Visuals:** Cross-sectional scatter plot of Operating Margin vs Trailing P/E across ICBP, Mayora (MYOR), Unilever (UNVR), Indofood Parent (INDF), and Cimory (CMRY).
- **Insight:** ICBP delivers the highest operating margin in its core category (23.91%), yet trades at 8.63x trailing P/E (lower than UNVR at 15.69x and CMRY at 15.98x).

#### 📉 Tab 6: Stock Performance & Technicals
- **Visuals:** Interactive Plotly Candlestick / Line chart with 20/50/200-day Simple Moving Averages, 14-day RSI, MACD histogram, and historical drawdowns.
- **Insight:** Identifies the oversold territory (RSI < 35) and historical support levels.

#### 🌐 Tab 7: Macro & Input Cost Sensitivity
- **Visuals:** Sensitivity bar chart analyzing impact of Bank Indonesia interest rate hikes, USD/IDR currency depreciation, wheat commodity spikes, and CPO prices.
- **Insight:** Natural dollar operational hedge provided by Pinehill's export and overseas revenues.

#### 📑 Tab 8: Equity Research Initiation Report
- **Visuals:** Institutional initiation note rendered directly inside the dashboard with tables and executive exhibits.

---

## 🎥 Recording a Video / GIF Demo for Portfolio Showcase

If creating a video or GIF demonstration for GitHub, LinkedIn, or personal portfolio:

1. **Recommended Free Tools:**
   - [Loom](https://www.loom.com/) (Browser / Desktop video with voiceover)
   - [ScreenToGif](https://www.screentogif.com/) (Windows animated GIF creator)
   - [OBS Studio](https://obsproject.com/) (High-definition screen capture)
2. **Recommended 60-Second Video Script:**
   - **00:00 - 00:15:** Introduce ICBP, the 15-year IPO track record, and the current 7.91x P/E valuation anomaly.
   - **00:15 - 00:35:** Switch to Tab 4 (Interactive DCF Valuation), adjust the WACC slider and terminal growth slider, and show the target price sensitivity matrix.
   - **00:35 - 00:45:** Switch to Tab 3 (Pinehill footprint) and Tab 5 (Peer benchmarking) highlighting ICBP's superior margins vs Mayora and Unilever.
   - **00:45 - 01:00:** Conclude with the Conviction BUY thesis and terminal test suite pass.

