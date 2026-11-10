# Direktori Hasil Riset, Laporan Tesis, dan Output Data
**PT Indofood CBP Sukses Makmur Tbk (IDX: ICBP)**
*Repositori terpusat untuk seluruh dokumen analisis tesis, dataset hasil proyeksi, grafik visualisasi, dan laporan riset ekuitas.*

---

## 1. Struktur Folder Hasil (*Results*)

Folder ini murni berisi **seluruh hasil kalkulasi, dokumen laporan analitis untuk penulisan tesis, tabel data, figur grafik, dan berkas Excel**, tanpa bercampur dengan file kode program:

```text
results/
│
├── thesis_dossiers/                  # Dokumen Analitis Markdown (.md) untuk Tesis
│   ├── 00_THESIS_DATA_GUIDE.md                                 # Panduan navigasi seluruh dossier
│   ├── 01_REVENUE_ORIGIN_AND_EXECUTIVE_SUMMARY.md              # Ringkasan asal pendapatan (Segmen, Pasar, Kanal)
│   ├── 02_SEGMENT_REVENUE_AND_PROFITABILITY_2010_2026.md       # Dekomposisi 6 divisi operasi (Sales, EBIT, Margin)
│   ├── 03_GEOGRAPHIC_REVENUE_AND_PINEHILL_GLOBAL_FOOTPRINT.md  # Pasar domestik vs MEA & Pinehill USD 3,0B
│   ├── 04_DISTRIBUTION_NETWORK_AND_CUSTOMER_CONCENTRATION.md   # Moat distribusi IAP & jaringan Indomaret
│   ├── 05_REVENUE_DRIVERS_PRICING_POWER_AND_THESIS_CATALYSTS.md # Pricing power, komoditas, & skenario
│   ├── 07_FINANCIAL_FORECASTS_AND_FCF_MODEL.md                 # Proyeksi 2026E-2030E & Free Cash Flow
│   ├── 08_DCF_VALUATION_SCENARIOS_AND_SENSITIVITY.md           # DCF 3 Skenario & Matriks Sensitivitas
│   ├── 09_PEER_VALUATION_BENCHMARKING.md                       # Perbandingan valuasi peers FMCG
│   ├── 10_STOCK_TRENDS_MOMENTUM_AND_VOLATILITY.md              # Analisis tren harga, SMA, RSI, drawdown
│   └── 11_MACRO_FX_COMMODITY_AND_RATE_EXPOSURES.md             # Analisis inflasi, utang USD, gandum, suku bunga
│
├── data_tables/                      # Tabel Data Hasil (.csv)
│   ├── 06_master_revenue_dataset_timeseries.csv   # Data time-series segmen 17 periode (2010-2026)
│   ├── 07_financial_forecasts_2026_2030.csv       # Tabel proyeksi laba rugi & FCFF 5 tahun
│   ├── 08_dcf_sensitivity_matrix.csv              # Matriks sensitivitas WACC vs Terminal Growth
│   ├── financial_metrics.csv                      # Metrik keuangan lengkap 2010-2025
│   ├── peers_financials_valuation_comparison.csv  # Tabel komparasi lengkap peers FMCG
│   ├── stock_performance.csv                      # Data historis harga, indikator teknikal harian
│   └── macro_economic_environment_2010_2025.csv   # Data historis indikator makro & komoditas
│
├── figures/                          # Grafik Visualisasi Standar Publikasi (.png)
│   ├── 01_financial_trajectory_growth.png         # Trajektori pertumbuhan pendapatan, EBIT, laba bersih
│   ├── 02_margin_stability_evolution.png          # Evolusi stabilitas margin kotor, EBIT, dan bersih
│   ├── 03_cfo_fcf_capex_generation.png            # Arus kas operasi, capex, dan free cash flow
│   ├── 04_stock_performance_vs_ihsg.png           # Kinerja saham ICBP vs benchmark IHSG
│   ├── 05_valuation_multiples_history.png         # Kelipatan P/E, P/BV, EV/EBITDA 15 tahun
│   ├── 06_peer_comparison_matrix.png              # Matriks komparasi peers (P/E vs Margin Usaha)
│   ├── 07_macro_commodity_correlation.png         # Korelasi makroekonomi dan harga komoditas
│   ├── 08_dcf_valuation_football_field.png        # Rentang valuasi DCF Football Field chart
│   ├── 09_segment_geographic_breakdown.png        # Komposisi segmen operasi & geografis Pinehill
│   ├── 10_technical_rsi_drawdown.png              # Analisis momentum RSI 14 dan Maximum Drawdown
│   └── 11_valuation_discount_to_historical_median.png # Diskon valuasi saat ini thd median historis
│
├── master_excel/                     # Model Finansial Komprehensif (.xlsx)
│   └── ICBP_Equity_Research_Master_Dataset.xlsx   # Master Workbook 15-Sheet terintegrasi
│
└── reports/                          # Laporan Riset Ekuitas Konsolidasian (.md)
    ├── equity_research_report.md                  # Institutional Equity Research Initiation Report
    └── ICBP_EQUITY_RESEARCH_DOSSIER.md            # Comprehensive Analyst Research Dossier
```

