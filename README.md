# IDX Equity Research & Valuation Intelligence: PT Indofood CBP Sukses Makmur Tbk (ICBP)

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly Charts](https://img.shields.io/badge/Plotly-5.22.0-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Market: IDX](https://img.shields.io/badge/IDX-ICBP.JK-1E3A8A.svg)](https://www.idx.co.id/)
[![Rating: BUY](https://img.shields.io/badge/Recommendation-CONVICTION%20BUY-10B981.svg)]()

> **Institutional-grade Equity Research, Financial Modeling, and Interactive Streamlit Valuation Suite for PT Indofood CBP Sukses Makmur Tbk (IDX: ICBP)**, covering 15+ years of audited financial disclosures (2010–2026), segment decomposition, Pinehill M&A global expansion, peer benchmarking, and a dynamic two-stage DCF valuation model.

---

## 📌 GitHub Repository Metadata & Description

- **Repository Name:** `IDX-Equity-Research-Valuation-Intelligence`
- **Short Description / Tagline:**  
  *Institutional Equity Research, Financial Modeling & Interactive Streamlit Dashboard for PT Indofood CBP Sukses Makmur Tbk (IDX: ICBP) — Audited Financials (2010–2026), Pinehill Global Footprint, Peer Benchmarking, and DCF Valuation.*
- **Suggested GitHub Topics / Tags:**  
  `equity-research` `dcf-valuation` `financial-modeling` `streamlit-dashboard` `indofood` `icbp` `indonesia-stock-exchange` `idx` `fmcg` `fundamental-analysis` `quantitative-finance` `python`

---

## 🎯 Executive Summary & Valuation Snapshot

| Valuation Metric | Current Market Level | 15-Year Historical Median | Target Fair Value (DCF Base) | Implied Upside |
|---|:---:|:---:|:---:|:---:|
| **Stock Price** | **IDR 5,775** | - | **IDR 24,582** | **+325.7%** |
| **Trailing P/E** | **7.91x** | **23.15x** | 18.0x – 22.0x | -65.8% Discount |
| **Forward P/E** | **6.76x** | 21.0x | 16.0x – 18.0x | -67.8% Discount |
| **EV / EBITDA** | **4.64x** | **12.32x** | 10.0x – 12.0x | -62.3% Discount |
| **P / BV** | **1.18x** | **3.42x** | 2.5x – 3.0x | -65.5% Discount |
| **Free Cash Flow Yield** | **11.35%** | **4.80%** | - | All-Time High |
| **Dividend Yield** | **4.75%** | **1.92%** | - | DPR 35% – 50% |

### Core Investment Thesis Pillars
1. **Unassailable Market Moat:** ICBP controls **>70% of Indonesia's instant noodle market** through the iconic *Indomie* brand, backed by the Salim Group's unmatched national distribution highway (PT Indomarco Adi Prima / IAP) reaching **>500,000 retail warungs** across 17,000 islands.
2. **Pinehill Global Engine:** The $3.0B acquisition of Pinehill Company Limited expanded direct manufacturing into 8 emerging economies across the Middle East & Africa (>885M consumers). International sales surged from **10.8% in 2019 to 32.1% in 1H 2026 (+20.7% YoY growth)**.
3. **Decadal Valuation Disconnect:** ICBP trades at **7.91x P/E (0th percentile rank since its 2010 IPO)**. The market has excessively penalized ICBP for non-cash foreign exchange translation paper losses on its USD 2.75B fixed-rate global bonds, creating an asymmetric risk/reward opportunity.
4. **Self-Funding Balance Sheet Deleveraging:** ICBP generates **>IDR 12 Trillion in annual operating cash flow (FCF conversion >100%)**, capable of completely retiring its entire net debt within **under 2 years**.

---

## 🖥️ Interactive Streamlit Dashboard Overview

The repository features an institutional-grade, full-screen **Streamlit Web Application** (`app.py`) providing interactive financial intelligence:

```bash
# Launch the interactive Streamlit application
streamlit run app.py
```

### Dashboard Capabilities
- **Executive Overview & Thesis:** Real-time KPI metric cards, investment pillar breakdown, and multi-year compounding trajectory.
- **Financial Statements & Ratios Explorer:** 15-year interactive charts across profitability margins, return on capital (ROIC/ROE), leverage ratios, and cash flows.
- **Segment & Pinehill Global Footprint:** Dynamic visualization of 6 operating divisions (Noodles, Dairy, Snacks, Seasonings, Nutrition, Beverages) and geographic revenue mix.
- **Interactive DCF Valuation Calculator:** Real-time dynamic scenario sliders for **WACC (6.5% - 11.0%)**, **Terminal Growth (1.5% - 5.0%)**, **Revenue CAGR (3.0% - 14.0%)**, and **EBIT Margin (16.0% - 26.0%)** with an interactive 2D sensitivity heatmap.
- **Peer Valuation & Benchmarking:** Cross-sectional scatter plots and valuation multiples comparing ICBP against **MYOR**, **UNVR**, **INDF**, and **CMRY**.
- **Stock Performance & Momentum:** Price action charts with 20/50/200-day SMAs, 14-day RSI (bullish divergence), MACD, rolling volatility, and drawdown curves.
- **Macro & Input Cost Sensitivity:** Multi-variable regression of inflation, USD/IDR, wheat, CPO, and interest-rate cycles on ICBP's margins.
- **Full Research Initiation Report:** Complete Wall Street-style initiation note rendered inside the application.

---

## 📂 Repository Architecture (Code vs. Results Segregation)

To ensure institutional clarity, all **code logic** is cleanly decoupled from **research deliverables and outputs**:

```text
IDX Equity Research & Valuation Intelligence/
│
├── app.py                                   # Streamlit Interactive Dashboard
├── requirements.txt                         # Production Python dependencies
├── .gitignore                               # Git ignore configuration
├── README.md                                # Project documentation
│
├── code/                                    # ◄── ALL SOURCE CODE & ENGINES
│   ├── scripts/                             # Automation pipelines (Scrapers, DCF, Multiples, Excel)
│   │   ├── 01_scrape_financial_statements.py
│   │   ├── 02_scrape_stock_market_data.py
│   │   ├── 03_scrape_valuation_multiples.py
│   │   ├── 04_scrape_peer_data.py
│   │   ├── 05_scrape_macro_commodities.py
│   │   ├── 06_compile_company_industry_info.py
│   │   ├── 07_generate_master_excel_workbook.py
│   │   ├── build_master_segment_timeseries.py
│   │   ├── download_all_raw_financial_statements.py
│   │   ├── extract_all_revenue_thesis_data.py
│   │   └── generate_all_valuation_and_forecast_thesis.py
│   ├── src/                                 # Reusable core modules
│   │   ├── valuation.py                     # DCF engine & sensitivity matrix
│   │   ├── financial_metrics.py             # Ratio computation & accounting checks
│   │   ├── data_processing.py               # Feature engineering & cleansing
│   │   └── visualization.py                 # Plotly & Matplotlib generators
│   ├── notebooks/                           # 7 Interactive Jupyter Notebooks
│   └── README.md                            # Code execution manual
│
├── results/                                 # ◄── ALL DELIVERABLES & THESIS OUTPUTS
│   ├── thesis_dossiers/                     # 11 Modular Markdown (.md) research dossiers
│   │   ├── 00_THESIS_DATA_GUIDE.md
│   │   ├── 01_REVENUE_ORIGIN_AND_EXECUTIVE_SUMMARY.md
│   │   ├── 02_SEGMENT_REVENUE_AND_PROFITABILITY_2010_2026.md
│   │   ├── 03_GEOGRAPHIC_REVENUE_AND_PINEHILL_GLOBAL_FOOTPRINT.md
│   │   ├── 04_DISTRIBUTION_NETWORK_AND_CUSTOMER_CONCENTRATION.md
│   │   ├── 05_REVENUE_DRIVERS_PRICING_POWER_AND_THESIS_CATALYSTS.md
│   │   ├── 07_FINANCIAL_FORECASTS_AND_FCF_MODEL.md
│   │   ├── 08_DCF_VALUATION_SCENARIOS_AND_SENSITIVITY.md
│   │   ├── 09_PEER_VALUATION_BENCHMARKING.md
│   │   ├── 10_STOCK_TRENDS_MOMENTUM_AND_VOLATILITY.md
│   │   └── 11_MACRO_FX_COMMODITY_AND_RATE_EXPOSURES.md
│   ├── data_tables/                         # 21 Structured CSV datasets
│   ├── figures/                             # 11 High-resolution PNG charts
│   ├── master_excel/                        # ICBP_Equity_Research_Master_Dataset.xlsx (15 Sheets)
│   ├── reports/                             # Equity Research Initiation Report (PDF/MD)
│   └── README.md                            # Results navigation guide
│
├── data/                                    # Underlying raw & processed storage
│   ├── raw/financial_statements/            # 22 Official downloaded Annual Reports & Statements
│   ├── processed/                           # Normalized analytical datasets
│   └── exports/                             # Excel Master Workbook
│
└── tests/                                   # Unit tests & validation suite
    └── test_application.py                  # Accounting & valuation verification
```

---

## 🔒 Git Directory Tracking & `.gitkeep` Convention

In Git, **empty directories are not tracked by default**. To preserve the essential folder structure across fresh repository clones, empty or transient directories include a `.gitkeep` placeholder file:

- `scratch/.gitkeep`: Preserves the scratch script workspace while ignoring temporary dump files.
- `data/raw/macroeconomic/.gitkeep`: Preserves raw macro directory structure.
- `data/raw/commodities/.gitkeep`: Preserves raw commodity cache structure.
- `data/raw/competitors/.gitkeep`: Preserves raw competitor OHLCV storage.
- `data/raw/stock_market/.gitkeep`: Preserves daily price storage.
- `downloads/.gitkeep`: Preserves the official PDF download directory.
- `reports/figures/.gitkeep`: Preserves the figure export directory.

---

## 🚀 Quickstart: Installation & Execution Guide

### 1. Environment Setup
Clone the repository and install the production dependencies:

```bash
# Clone the repository
git clone https://github.com/<your-username>/IDX-Equity-Research-Valuation-Intelligence.git
cd IDX-Equity-Research-Valuation-Intelligence

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Run the Interactive Streamlit Dashboard
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser to explore the dashboard.

### 3. Run Automated Validation & Unit Tests
```bash
python tests/test_application.py
```
*Validates data provenance, accounting identities, WACC CAPM math, and segment reconciliations.*

### 4. Reproduce the Data Scraping & Valuation Pipeline
```bash
# 1. Download official reports
python code/scripts/download_all_raw_financial_statements.py

# 2. Extract segment notes from audited reports
python code/scripts/extract_all_revenue_thesis_data.py

# 3. Build multi-year segment timeseries
python code/scripts/build_master_segment_timeseries.py

# 4. Generate 2026E-2030E DCF forecast models
python code/scripts/generate_all_valuation_and_forecast_thesis.py

# 5. Build Master Excel Workbook (15 Sheets)
python code/scripts/07_generate_master_excel_workbook.py
```

---

## 📊 Summary of DCF Valuation Scenarios

$$PV(\text{Enterprise Value}) = \sum_{t=1}^{5} \frac{\text{FCFF}_t}{(1 + \text{WACC})^t} + \frac{\text{FCFF}_5 \times (1 + g)}{(\text{WACC} - g) \times (1 + \text{WACC})^5}$$

| Parameter | Bear Case (Stagnation) | Base Case (Target Price) | Bull Case (Expansion) |
|---|:---:|:---:|:---:|
| **5-Yr Revenue CAGR** | +4.0% | **+7.5%** | +9.7% |
| **Operating (EBIT) Margin** | 18.4% | **21.8%** | 23.1% |
| **WACC (Discount Rate)** | 8.80% | **8.10%** | 7.40% |
| **Terminal Growth Rate ($g$)** | 2.50% | **3.50%** | 4.20% |
| **Enterprise Value (IDR B)** | Rp 166,175.7 | **Rp 304,558.6** | Rp 474,562.2 |
| **Net Debt (FY2025)** | -Rp 17,969.9 | **-Rp 17,969.9** | -Rp 17,969.9 |
| **Equity Value (IDR B)** | Rp 148,205.8 | **Rp 286,588.7** | Rp 456,592.3 |
| **Intrinsic Value Per Share** | **IDR 12,659** | **IDR 24,582** | **IDR 40,673** |
| **Current Market Price** | IDR 5,775 | IDR 5,775 | IDR 5,775 |
| **Implied Upside (%)** | **+119.2%** | **+325.7%** | **+604.3%** |
| **Margin of Safety (%)** | **54.4%** | **76.5%** | **85.8%** |

---

## ⚖️ Peer Valuation Benchmarking (IDX FMCG)

| Ticker | Company Name | Market Cap (IDR T) | Operating Margin (%) | ROIC (%) | Trailing P/E (x) | Forward P/E (x) | P/BV (x) | EV/EBITDA (x) | Dividend Yield (%) |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **ICBP.JK** | **Indofood CBP** | **71.43** | **23.91%** | **21.42%** | **8.63x** | **6.76x** | **1.29x** | **5.71x** | **4.47%** |
| **MYOR.JK** | Mayora Indah | 29.08 | 8.81% | 14.07% | 8.56x | 8.23x | 1.54x | 4.92x | 4.58% |
| **UNVR.JK** | Unilever Indonesia | 55.26 | 16.94% | 162.25% | 15.69x | 13.70x | 13.14x | 9.96x | 16.40% |
| **INDF.JK** | Indofood (Parent) | 59.05 | 19.96% | 21.70% | 5.53x | 5.17x | 0.74x | 4.15x | 4.39% |
| **CMRY.JK** | Cisarua Mountain Dairy | 34.36 | 17.89% | 29.64% | 15.98x | 19.42x | 4.97x | 12.25x | 4.93% |

---

## 📜 License & Disclaimers

- **License:** Released under the [MIT License](LICENSE).
- **Disclaimer:** *This repository and all associated research models, dossiers, and forecasts are created strictly for portfolio demonstration, educational, and equity research analysis purposes. They do not constitute personalized financial advice or a direct solicitation to buy or sell securities. Investors should conduct independent due diligence before making investment decisions.*
