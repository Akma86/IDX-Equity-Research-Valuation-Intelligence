"""
scripts/download_all_raw_financial_statements.py
Downloads and standardizes all raw financial statements and annual reports for ICBP
from early IPO (2010 Prospectus & 2011 Audited Statement) through 2025 Annual Report and 2026 interim statements.
Saves all reports into: data/raw/financial_statements/
"""

import os
import shutil
import requests
import urllib3
import fitz
import json
import pandas as pd

urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

RAW_FS_DIR = os.path.join("data", "raw", "financial_statements")
os.makedirs(RAW_FS_DIR, exist_ok=True)
os.makedirs(os.path.join(RAW_FS_DIR, "annual_reports"), exist_ok=True)
os.makedirs(os.path.join(RAW_FS_DIR, "interim_quarterly"), exist_ok=True)

# 1. Target URLs for Annual Reports and Audited Statements (2010 - 2025)
annual_targets = {
    2010: {
        "title": "ICBP Prospektus Penawaran Umum Perdana Saham (IPO 2010)",
        "url": "https://www.indofoodcbp.com/uploads/document/ICBP_Prospektus%20RingkasPenawaran%20Umum_IPO.pdf",
        "filename": "ICBP_2010_IPO_Prospectus.pdf"
    },
    2011: {
        "title": "ICBP Audited Financial Statements Full Notes FY2011 & FY2010",
        "url": "https://www.indofoodcbp.com/uploads/statement/Financial%20Statement_Full%20Notes_4Q11%20Billingual%20ICBP.pdf",
        "filename": "ICBP_2011_Financial_Statement_Full_Notes.pdf"
    },
    2012: {
        "title": "ICBP Annual Report 2012",
        "url": "https://www.indofoodcbp.com/uploads/annual/ar-2012.pdf",
        "filename": "ICBP_2012_Annual_Report.pdf",
        "local_src": "downloads/ar_2012.pdf"
    },
    2013: {
        "title": "ICBP Annual Report 2013",
        "url": None,
        "filename": "ICBP_2013_Annual_Report.pdf",
        "local_src": "downloads/ar_2013.pdf"
    },
    2014: {
        "title": "ICBP Annual Report 2014",
        "url": "https://www.indofoodcbp.com/uploads/annual/ICBP_2014_website.pdf",
        "filename": "ICBP_2014_Annual_Report.pdf"
    },
    2015: {
        "title": "ICBP Annual Report 2015",
        "url": "https://www.indofoodcbp.com/uploads/annual/ICBP_AR%202015_web%20update.pdf",
        "filename": "ICBP_2015_Annual_Report.pdf",
        "local_src": "downloads/ar_2015.pdf"
    },
    2016: {
        "title": "ICBP Annual Report 2016",
        "url": "https://www.indofoodcbp.com/uploads/annual/ICBP%20AR2016_vFinal_lo.pdf",
        "filename": "ICBP_2016_Annual_Report.pdf",
        "local_src": "downloads/ar_2016.pdf"
    },
    2017: {
        "title": "ICBP Annual Report 2017",
        "url": "https://www.indofoodcbp.com/uploads/annual/ICBP_Annual%20Report_2017.pdf",
        "filename": "ICBP_2017_Annual_Report.pdf",
        "local_src": "downloads/ar_2017.pdf"
    },
    2018: {
        "title": "ICBP Annual Report 2018",
        "url": "https://www.indofoodcbp.com/uploads/annual/AR%20ICBP%202018_website%2020190430.pdf",
        "filename": "ICBP_2018_Annual_Report.pdf"
    },
    2019: {
        "title": "ICBP Annual Report 2019",
        "url": "https://www.indofoodcbp.com/uploads/annual/ICBP%20-%20AR%202019.pdf",
        "filename": "ICBP_2019_Annual_Report.pdf",
        "local_src": "downloads/ar_2019.pdf"
    },
    2020: {
        "title": "ICBP Annual Report 2020",
        "url": "https://www.indofoodcbp.com/uploads/annual/ICBP%20-%20AR%202020%20Preview_web%20version.pdf",
        "filename": "ICBP_2020_Annual_Report.pdf",
        "local_src": "downloads/ar_2020.pdf"
    },
    2021: {
        "title": "ICBP Annual Report 2021",
        "url": "https://www.indofoodcbp.com/uploads/annual/icbp_2021ar_web%20version.pdf",
        "filename": "ICBP_2021_Annual_Report.pdf",
        "local_src": "downloads/ar_2021.pdf"
    },
    2022: {
        "title": "ICBP Annual Report 2022",
        "url": "https://www.indofoodcbp.com/uploads/annual/ICBP_AR_2022.pdf",
        "filename": "ICBP_2022_Annual_Report.pdf",
        "local_src": "downloads/ar_2022.pdf"
    },
    2023: {
        "title": "ICBP Annual Report 2023",
        "url": "https://www.indofoodcbp.com/uploads/annual/AR%20ICBP_2023_web.pdf",
        "filename": "ICBP_2023_Annual_Report.pdf",
        "local_src": "downloads/ar_2023.pdf"
    },
    2024: {
        "title": "ICBP Annual Report 2024",
        "url": "https://www.indofoodcbp.com/uploads/annual/AR%20ICBP%2024_final.pdf",
        "filename": "ICBP_2024_Annual_Report.pdf",
        "local_src": "downloads/ar_2024.pdf"
    },
    2025: {
        "title": "ICBP Annual Report 2025",
        "url": "https://www.indofoodcbp.com/uploads/annual/ICBP_2025AR_final.pdf",
        "filename": "ICBP_2025_Annual_Report.pdf",
        "local_src": "downloads/ar_2025.pdf"
    }
}

# 2. Key Interim / Quarterly Financial Statements
quarterly_targets = {
    "9M26": {
        "title": "ICBP Interim Consolidated Financial Statements 9M26 (30 Sep 2026)",
        "url": "https://www.indofoodcbp.com/uploads/statement/Icbp_billingual_30_Sep_26.pdf",
        "filename": "ICBP_2026_9M_Interim_Financial_Statement.pdf",
        "local_src": "downloads/icbp_9M26_summary.pdf"
    },
    "1H26": {
        "title": "ICBP Interim Consolidated Financial Statements 1H26 (30 Jun 2026)",
        "url": "https://www.indofoodcbp.com/uploads/statement/ICBP_billingual_30_Jun_26.pdf",
        "filename": "ICBP_2026_1H_Interim_Financial_Statement.pdf"
    },
    "1Q26": {
        "title": "ICBP Interim Consolidated Financial Statements 1Q26 (31 Mar 2026)",
        "url": "https://www.indofoodcbp.com/uploads/statement/ICBP_billingual_31_Mar_26.pdf",
        "filename": "ICBP_2026_1Q_Interim_Financial_Statement.pdf"
    },
    "9M25": {
        "title": "ICBP Interim Consolidated Financial Statements 9M25 (30 Sep 2025)",
        "url": "https://www.indofoodcbp.com/uploads/statement/Icbp_billingual_30_Sep_25.pdf",
        "filename": "ICBP_2025_9M_Interim_Financial_Statement.pdf"
    },
    "1H25": {
        "title": "ICBP Interim Consolidated Financial Statements 1H25 (30 Jun 2025)",
        "url": "https://www.indofoodcbp.com/uploads/statement/ICBP_billingual_30Jun25.pdf",
        "filename": "ICBP_2025_1H_Interim_Financial_Statement.pdf"
    },
    "1Q25": {
        "title": "ICBP Interim Consolidated Financial Statements 1Q25 (31 Mar 2025)",
        "url": "https://www.indofoodcbp.com/uploads/statement/Icbp_billingual_31_Mar_25.pdf",
        "filename": "ICBP_2025_1Q_Interim_Financial_Statement.pdf"
    }
}

manifest = []

def download_or_copy(item, folder_path, period_label, category):
    dst = os.path.join(folder_path, item["filename"])
    local_src = item.get("local_src")
    url = item.get("url")
    
    # Check if local exists and can be copied
    if local_src and os.path.exists(local_src):
        if not os.path.exists(dst):
            shutil.copy2(local_src, dst)
            print(f"[COPIED] {item['filename']} from local cache ({os.path.getsize(dst)/1e6:.2f} MB)")
        else:
            print(f"[EXISTS] {item['filename']} ({os.path.getsize(dst)/1e6:.2f} MB)")
    elif url:
        if not os.path.exists(dst):
            print(f"[DOWNLOADING] {item['filename']} from {url}...")
            try:
                r = requests.get(url, headers=headers, verify=False, timeout=60)
                if r.status_code == 200:
                    with open(dst, "wb") as f:
                        f.write(r.content)
                    print(f"  -> Saved {item['filename']} ({len(r.content)/1e6:.2f} MB)")
                else:
                    print(f"  -> Failed: HTTP {r.status_code}")
            except Exception as e:
                print(f"  -> Error: {e}")
        else:
            print(f"[EXISTS] {item['filename']} ({os.path.getsize(dst)/1e6:.2f} MB)")
    
    if os.path.exists(dst):
        try:
            doc = fitz.open(dst)
            page_count = len(doc)
            file_size_mb = round(os.path.getsize(dst) / (1024 * 1024), 2)
            manifest.append({
                "Period": period_label,
                "Category": category,
                "Title": item["title"],
                "Filename": item["filename"],
                "Relative_Path": os.path.relpath(dst).replace("\\", "/"),
                "File_Size_MB": file_size_mb,
                "Page_Count": page_count,
                "Source_URL": url if url else "Local Cache / IPO Filing"
            })
        except Exception as e:
            print(f"Error inspecting {dst}: {e}")

print("==========================================================")
print("PROCESSING ANNUAL REPORTS & IPO PROSPECTUS (2010 - 2025)...")
print("==========================================================")
ann_dir = os.path.join(RAW_FS_DIR, "annual_reports")
for yr in sorted(annual_targets.keys()):
    download_or_copy(annual_targets[yr], ann_dir, str(yr), "Annual / Audited")

print("\n==========================================================")
print("PROCESSING INTERIM & QUARTERLY STATEMENTS (2025 - 2026)...")
print("==========================================================")
q_dir = os.path.join(RAW_FS_DIR, "interim_quarterly")
for q_lbl, q_info in quarterly_targets.items():
    download_or_copy(q_info, q_dir, q_lbl, "Quarterly / Interim")

# Save manifest catalog
manifest_df = pd.DataFrame(manifest)
manifest_json_path = os.path.join(RAW_FS_DIR, "financial_reports_catalog.json")
manifest_csv_path = os.path.join(RAW_FS_DIR, "financial_reports_catalog.csv")

with open(manifest_json_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

manifest_df.to_csv(manifest_csv_path, index=False)

print("\n==========================================================")
print("ALL RAW FINANCIAL REPORTS CATALOG SUMMARY:")
print("==========================================================")
print(manifest_df[["Period", "Category", "Filename", "File_Size_MB", "Page_Count"]].to_string(index=False))
print(f"\nManifest catalog saved to:\n - {manifest_csv_path}\n - {manifest_json_path}")
print(f"Total Reports Stored: {len(manifest_df)} official documents.")
print(f"Total Size: {manifest_df['File_Size_MB'].sum():.2f} MB across {manifest_df['Page_Count'].sum()} pages.")

