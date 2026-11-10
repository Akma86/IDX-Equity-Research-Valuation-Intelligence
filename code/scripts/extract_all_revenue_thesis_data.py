"""
extract_all_revenue_thesis_data.py
Systematically extracts revenue breakdown from all official ICBP annual reports & financial statements
from IPO (2010) through 2026 (including 9M26/1H26).
Dumps structured segment data, geographic data, and customer concentration data.
"""

import os
import fitz
import re
import json
import pandas as pd

def extract_text_range(pdf_path, start_page, end_page):
    doc = fitz.open(pdf_path)
    text = ""
    for p in range(start_page - 1, min(end_page, len(doc))):
        text += f"\n--- Page {p+1} ---\n" + doc[p].get_text()
    return text

def run_extraction():
    reports_map = {
        "2011_FS": ("data/raw/financial_statements/annual_reports/ICBP_2011_Financial_Statement_Full_Notes.pdf", 95, 105),
        "2012_AR": ("data/raw/financial_statements/annual_reports/ICBP_2012_Annual_Report.pdf", 225, 235),
        "2013_AR": ("data/raw/financial_statements/annual_reports/ICBP_2013_Annual_Report.pdf", 235, 245),
        "2014_AR": ("data/raw/financial_statements/annual_reports/ICBP_2014_Annual_Report.pdf", 255, 265),
        "2015_AR": ("data/raw/financial_statements/annual_reports/ICBP_2015_Annual_Report.pdf", 270, 280),
        "2016_AR": ("data/raw/financial_statements/annual_reports/ICBP_2016_Annual_Report.pdf", 268, 276),
        "2017_AR": ("data/raw/financial_statements/annual_reports/ICBP_2017_Annual_Report.pdf", 274, 282),
        "2018_AR": ("data/raw/financial_statements/annual_reports/ICBP_2018_Annual_Report.pdf", 312, 320),
        "2019_AR": ("data/raw/financial_statements/annual_reports/ICBP_2019_Annual_Report.pdf", 319, 327),
        "2020_AR": ("data/raw/financial_statements/annual_reports/ICBP_2020_Annual_Report.pdf", 341, 350),
        "2021_AR": ("data/raw/financial_statements/annual_reports/ICBP_2021_Annual_Report.pdf", 291, 300),
        "2022_AR": ("data/raw/financial_statements/annual_reports/ICBP_2022_Annual_Report.pdf", 316, 326),
        "2024_AR": ("data/raw/financial_statements/annual_reports/ICBP_2024_Annual_Report.pdf", 287, 296),
        "2025_AR": ("data/raw/financial_statements/annual_reports/ICBP_2025_Annual_Report.pdf", 269, 278),
        "2026_1H": ("data/raw/financial_statements/interim_quarterly/ICBP_2026_1H_Interim_Financial_Statement.pdf", 89, 96)
    }
    
    extracted_texts = {}
    for key, (path, start_p, end_p) in reports_map.items():
        if os.path.exists(path):
            print(f"Extracting {key} from {path} (pages {start_p}-{end_p})...")
            extracted_texts[key] = extract_text_range(path, start_p, end_p)
            
    os.makedirs("data/raw/extracted_segment_notes", exist_ok=True)
    with open("data/raw/extracted_segment_notes/segment_notes_dump.json", "w", encoding="utf-8") as f:
        json.dump(extracted_texts, f, indent=2, ensure_ascii=False)
    print("Extracted segment text dumped to data/raw/extracted_segment_notes/segment_notes_dump.json")

if __name__ == "__main__":
    run_extraction()

