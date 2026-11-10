"""
extract_segments_all_years.py
Parse exact segment figures (Sales, Intersegment, EBIT) and geographic sales from all reports.
"""

import fitz
import re
import json

def get_text_pages(pdf_path, pages):
    doc = fitz.open(pdf_path)
    res = {}
    for p in pages:
        if p <= len(doc):
            res[p] = doc[p-1].get_text()
    return res

# Let's inspect pages from 2016 AR, 2018 AR, 2020 AR, 2022 AR, 2024 AR, 2025 AR, 2026 1H
reports = {
    "2016": ("data/raw/financial_statements/annual_reports/ICBP_2016_Annual_Report.pdf", [270, 271, 272, 273]),
    "2018": ("data/raw/financial_statements/annual_reports/ICBP_2018_Annual_Report.pdf", [314, 315, 316, 317]),
    "2020": ("data/raw/financial_statements/annual_reports/ICBP_2020_Annual_Report.pdf", [343, 344, 345, 346]),
    "2022": ("data/raw/financial_statements/annual_reports/ICBP_2022_Annual_Report.pdf", [318, 319, 320, 321, 322]),
    "2024": ("data/raw/financial_statements/annual_reports/ICBP_2024_Annual_Report.pdf", [289, 290, 291, 292, 293]),
    "2025": ("data/raw/financial_statements/annual_reports/ICBP_2025_Annual_Report.pdf", [271, 272, 273, 274]),
    "2026_1H": ("data/raw/financial_statements/interim_quarterly/ICBP_2026_1H_Interim_Financial_Statement.pdf", [91, 92, 93, 94])
}

all_res = {}
for yr, (path, pgs) in reports.items():
    all_res[yr] = get_text_pages(path, pgs)

with open("data/raw/extracted_segment_notes/segment_pages_2016_2026.json", "w", encoding="utf-8") as f:
    json.dump(all_res, f, indent=2, ensure_ascii=False)
print("Saved segment pages 2016-2026 successfully.")

