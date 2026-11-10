import requests
import urllib3
urllib3.disable_warnings()
import os
import fitz
import re

os.makedirs("downloads", exist_ok=True)

reports = {
    "2012": "https://www.indofoodcbp.com/uploads/annual/ar-2012.pdf",
    "2015": "https://www.indofoodcbp.com/uploads/annual/ICBP_AR%202015_web%20update.pdf",
    "2019": "https://www.indofoodcbp.com/uploads/annual/ICBP%20-%20AR%202019.pdf",
    "2024": "https://www.indofoodcbp.com/uploads/annual/AR%20ICBP%2024_final.pdf",
    "2025": "https://www.indofoodcbp.com/uploads/annual/ICBP_2025AR_final.pdf"
}

for yr, url in reports.items():
    dest = f"downloads/ar_{yr}.pdf"
    if not os.path.exists(dest):
        print(f"Downloading {yr} from {url}...")
        try:
            r = requests.get(url, verify=False, timeout=30)
            if r.status_code == 200:
                with open(dest, "wb") as f:
                    f.write(r.content)
                print(f"Saved {dest} ({len(r.content)} bytes)")
            else:
                print(f"Failed {yr}: HTTP {r.status_code}")
        except Exception as e:
            print(f"Error {yr}: {e}")
    else:
        print(f"Already exists: {dest}")

print("Download phase complete.")
