# Panduan Data Tesis: Direktori Lengkap Riset Ekuitas ICBP
**PT Indofood CBP Sukses Makmur Tbk (IDX: ICBP)**
*Dokumen ini merupakan indeks dan panduan navigasi bagi seluruh data analitis, proyeksi keuangan, valuasi DCF, benchmarking peer, teknikal kuantitatif, dan analisis eksposur makroekonomi yang diekstrak langsung dari Laporan Keuangan Audited dan Laporan Tahunan (Annual Report) ICBP periode IPO (2010) hingga 2026 YTD.*

---

## 1. Tujuan Direktori `thesis_data/`

Folder ini dibentuk khusus sebagai **pusat data primer (*thesis data vault*)** untuk menyusun **Investment Thesis & Equity Research Report** emiten ICBP secara komprehensif dan berstandar institusi riset pasar modal.

Semua angka historis, margin segmen, distribusi geografis, dan model valuasi di dalam folder ini telah direkonsiliasi dan bersumber langsung dari:
1. **Catatan atas Laporan Keuangan Konsolidasian: Informasi Segmen Operasi** (*Note on Segment Information* - Catatan 30/31).
2. **Catatan atas Laporan Keuangan Konsolidasian: Penjualan Neto** (*Note on Net Sales* - Catatan 24/25).
3. **Catatan atas Transaksi dengan Pihak Berelasi** (*Note on Related Parties* - Catatan 31/32).
4. **Prospektus Penawaran Umum Perdana Saham (IPO 2010)** dan 21 berkas PDF resmi BEI & Investor Relations ICBP.

---

## 2. Peta Dokumen & Navigasi Lengkap

Folder ini tersusun secara modular ke dalam 11 berkas dokumen:

```text
thesis_data/
│
├── 00_THESIS_DATA_GUIDE.md
│   └── (File ini) Indeks direktori, panduan metodologi, dan pemetaan data tesis.
│
├── 01_REVENUE_ORIGIN_AND_EXECUTIVE_SUMMARY.md
│   └── Eksekutif summary "Dari Mana Saja Uang ICBP Berasal": Segmen, Geografis, dan Kanal Penjualan.
│
├── 02_SEGMENT_REVENUE_AND_PROFITABILITY_2010_2026.md
│   └── Analisis mendalam 6 divisi operasi: Noodles, Dairy, Snacks, Seasonings, Nutrition, Beverages (Sales, EBIT, Margin 2010-2026).
│
├── 03_GEOGRAPHIC_REVENUE_AND_PINEHILL_GLOBAL_FOOTPRINT.md
│   └── Analisis pasar domestik vs internasional, akuisisi Pinehill ($3,0 Miliar), dan jejak pabrik di 8 negara (MEA).
│
├── 04_DISTRIBUTION_NETWORK_AND_CUSTOMER_CONCENTRATION.md
│   └── Analisis "Salim Distribution Moat": Peran PT Indomarco Adi Prima (IAP), Indomaret, General Trade, dan Pihak Berelasi.
│
├── 05_REVENUE_DRIVERS_PRICING_POWER_AND_THESIS_CATALYSTS.md
│   └── Bahan tesis investasi: Pricing power, premiumisasi, sensitivitas komoditas (gandum/CPO), risiko valuta asing, dan katalis DCF.
│
├── 06_master_revenue_dataset_timeseries.csv
│   └── Dataset mentah & terstruktur (CSV) 17 periode (2010–2026 1H) untuk memudahkan visualisasi dan pemodelan finansial.
│
├── 07_FINANCIAL_FORECASTS_AND_FCF_MODEL.md
│   └── Model proyeksi 5 tahun (2026E–2030E): Laporan Laba Rugi terperinci, NOPAT, Capex, NWC, dan Free Cash Flow to Firm (FCFF).
│
├── 08_DCF_VALUATION_SCENARIOS_AND_SENSITIVITY.md
│   └── Model Valuasi DCF 3 Skenario (Bear, Base, Bull), struktur WACC CAPM, dan matriks sensitivitas 2 arah (WACC vs Terminal Growth).
│
├── 09_PEER_VALUATION_BENCHMARKING.md
│   └── Komparasi valuasi & kualitas finansial peer: ICBP vs MYOR, UNVR, INDF, CMRY (P/E, EV/EBITDA, ROIC, Margin Usaha).
│
├── 10_STOCK_TRENDS_MOMENTUM_AND_VOLATILITY.md
│   └── Analisis kuantitatif & teknikal saham: Imbal hasil multi-tahun vs IHSG, SMA 20/50/200, RSI 14, MACD, volatilitas, dan drawdown.
│
└── 11_MACRO_FX_COMMODITY_AND_RATE_EXPOSURES.md
    └── Telaah risiko makroekonomi: Inflasi & elastisitas giffen, utang obligasi USD $2,75B, devaluasi mata uang MEA, gandum, CPO, dan BI-Rate.
```

---

## 3. Matriks Pertanyaan Kunci Tesis vs Sumber Data

| Pertanyaan Kunci dalam Investment Thesis | Dokumen Rujukan Utama | Variabel & Temuan Kunci |
|---|---|---|
| **Apa motor utama pendapatan & laba perseroan?** | `01_REVENUE_ORIGIN...` & `02_SEGMENT_REVENUE...` | Mi Instan (71,9% sales, 86,9% EBIT, margin tebal 24%–26%). |
| **Seberapa besar kontribusi pasar global Pinehill?** | `03_GEOGRAPHIC_REVENUE...` | Lonjakan penjualan MEA dari 10% ke 32%; pabrik luar negeri 65% aset tetap. |
| **Seberapa kuat benteng distribusi grup?** | `04_DISTRIBUTION_NETWORK...` | Penjualan via IAP (>60%), Indomaret (>22k gerai), 500k warung, zero default risk. |
| **Bagaimana proyeksi kas bebas 5 tahun ke depan?** | `07_FINANCIAL_FORECASTS...` | FCFF diproyeksikan menghasilkan Rp 72,5 Triliun (2026E–2030E), deleveraging penuh. |
| **Berapa nilai wajar saham ICBP (DCF Target Price)?** | `08_DCF_VALUATION...` | Base Case: **Rp 24.582 / saham (+325,7%)**; Bear Case: **Rp 12.659 (+119,2%)**. |
| **Bagaimana posisi valuasi ICBP dibanding pesaing?** | `09_PEER_VALUATION...` | P/E 8,6x (vs peer 12,1x), terdiskon 65,8% dari median historis (persentil ke-0). |
| **Bagaimana tren teknikal dan lantai harga saham?** | `10_STOCK_TRENDS...` | Lantai support kuat di Rp 5.400–Rp 5.500; RSI & MACD konfirmasi bullish divergence. |
| **Bagaimana dampak utang USD dan devaluasi mata uang?** | `11_MACRO_FX_COMMODITY...` | Beban kurs obligasi USD 2,75B non-kas (jatuh tempo 2031/32/51); pemulihan ASP di MEA. |

---

## 4. Standar Nilai & Konvensi Satuan

- Seluruh angka nominal dalam laporan analitis disajikan dalam **Miliar Rupiah (IDR Billion / Rp Miliar)** kecuali jika secara eksplisit dinyatakan lain (misalnya dalam Dolar AS untuk transaksi Pinehill dan obligasi global).
- Dalam laporan keuangan resmi ICBP, angka disajikan dalam satuan **Jutaan Rupiah (IDR Million)**. Konversi ke Miliar Rupiah dilakukan dengan membagi $1.000$.
- Penjualan Neto Konsolidasian (*Consolidated Net Sales*) dihitung setelah mengeliminasi penjualan antar-segmen (*inter-segment eliminations*).
