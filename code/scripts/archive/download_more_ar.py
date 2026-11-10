import requests
import urllib3
urllib3.disable_warnings()
import os

additional_reports = {
    "2010": "https://www.indofoodcbp.com/uploads/annual/ar-2010.pdf", # let's check
    "2013": "https://www.indofoodcbp.com/uploads/annual/ICBP_AR_2013.pdf", # let's check
    "2016": "https://www.indofoodcbp.com/uploads/annual/ICBP%20AR2016_vFinal_lo.pdf",
    "2017": "https://www.indofoodcbp.com/uploads/annual/ICBP_Annual%20Report_2017.pdf",
    "2020": "https://www.indofoodcbp.com/uploads/annual/ICBP%20-%20AR%202020%20Preview_web%20version.pdf",
    "2021": "https://www.indofoodcbp.com/uploads/annual/icbp_2021ar_web%20version.pdf",
    "2022": "https://www.indofoodcbp.com/uploads/annual/ICBP_AR_2022.pdf",
    "2023": "https://www.indofoodcbp.com/uploads/annual/AR%20ICBP_2023_web.pdf"
}

for yr, url in additional_reports.items():
    dest = f"downloads/ar_{yr}.pdf"
    if not os.path.exists(dest):
        try:
            r = requests.get(url, verify=False, timeout=25)
            if r.status_code == 200:
                with open(dest, "wb") as f:
                    f.write(r.content)
                print(f"{yr}: Saved ({len(r.content)} bytes)")
            else:
                print(f"{yr}: HTTP {r.status_code}")
        except Exception as e:
            print(f"{yr}: Error {e}")
    else:
        print(f"{yr}: Already exists")
