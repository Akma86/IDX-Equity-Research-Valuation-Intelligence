# Direktori Kode & Pemodelan Finansial ICBP
**PT Indofood CBP Sukses Makmur Tbk (IDX: ICBP)**
*Repositori terpusat untuk seluruh skrip komputasi, modul library, dan notebook analitis.*

---

## 1. Struktur Folder Kode

```text
code/
│
├── scripts/                          # Skrip otomatisasi Python mandiri (.py)
│   ├── download_all_raw_financial_statements.py  # Unduh 22 laporan resmi (2010-2026)
│   ├── extract_all_revenue_thesis_data.py        # Ekstraksi catatan segmen dari PDF
│   ├── build_master_segment_timeseries.py        # Rekonsiliasi data segmen 2010-2026
│   ├── generate_all_valuation_and_forecast_thesis.py # Proyeksi 2026E-2030E & Valuasi DCF
│   ├── 01_scrape_financial_statements.py         # Pipeline data laporan keuangan audited
│   ├── 02_scrape_stock_market_data.py            # Pipeline data harga saham harian OHLCV
│   ├── 03_scrape_valuation_multiples.py          # Kalkulasi kelipatan valuasi 15 tahun
│   ├── 04_scrape_peer_data.py                    # Analisis perbandingan peers FMCG
│   ├── 05_scrape_macro_commodities.py            # Pipeline makro, inflasi, valas, komoditas
│   ├── 06_compile_company_industry_info.py       # Profil profil bisnis & aksi korporasi
│   ├── 07_generate_master_excel_workbook.py      # Pembangun Excel Master 15-Sheet
│   └── build_notebooks.py                        # Pembangun Jupyter Notebooks
│
├── src/                              # Modul pustaka Python reusable
│   ├── data_processing.py            # Pembersihan data dan rekayasa fitur
│   ├── financial_metrics.py          # Rasio finansial, ROIC, margin, solvabilitas
│   ├── valuation.py                  # Mesin DCF, WACC CAPM, dan matriks sensitivitas
│   └── visualization.py              # Generator 11 grafik visualisasi standar publikasi
│
└── notebooks/                        # Jupyter Notebooks interaktif (.ipynb)
    ├── 01_data_collection.ipynb      # Pengumpulan & validasi data
    ├── 02_financial_analysis.ipynb   # Analisis kinerja keuangan historis
    ├── 03_stock_performance.ipynb    # Analisis teknikal & imbal hasil saham
    ├── 04_peer_comparison.ipynb      # Komparasi peers (MYOR, UNVR, INDF, CMRY)
    ├── 05_macro_analysis.ipynb       # Korelasi makro, valas, dan komoditas
    ├── 06_valuation_analysis.ipynb   # Pemodelan valuasi DCF & sensitivitas
    └── 07_investment_thesis.ipynb    # Sintesis tesis investasi & rekomendasi saham
```

---

## 2. Cara Menjalankan Kode Pemrosesan

Untuk menjalankan seluruh pipeline pemrosesan dari awal hingga menghasilkan seluruh data dan laporan:

```bash
# 1. Jalankan pengunduhan laporan keuangan resmi
python code/scripts/download_all_raw_financial_statements.py

# 2. Jalankan kompilasi data laporan keuangan & rasio
python code/scripts/01_scrape_financial_statements.py

# 3. Jalankan pengolahan data pasar saham & teknikal
python code/scripts/02_scrape_stock_market_data.py

# 4. Jalankan komputasi kelipatan valuasi historis
python code/scripts/03_scrape_valuation_multiples.py

# 5. Jalankan analisis perbandingan peers
python code/scripts/04_scrape_peer_data.py

# 6. Jalankan analisis makroekonomi & komoditas
python code/scripts/05_scrape_macro_commodities.py

# 7. Jalankan model proyeksi 5 tahun & valuasi DCF 3 skenario
python code/scripts/generate_all_valuation_and_forecast_thesis.py

# 8. Hasilkan Master Excel Workbook 15-Sheet
python code/scripts/07_generate_master_excel_workbook.py
```

