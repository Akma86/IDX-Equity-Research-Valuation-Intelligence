import fitz
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# Search for "kas neto yang diperoleh dari aktivitas operasi" or "arus kas neto yang diperoleh dari aktivitas operasi"
# and "kas dan setara kas pada akhir tahun" in all downloaded reports
reports = {
    2012: "downloads/ar_2012.pdf",
    2015: "downloads/ar_2015.pdf",
    2016: "downloads/ar_2016.pdf",
    2017: "downloads/ar_2017.pdf",
    2019: "downloads/ar_2019.pdf",
    2020: "downloads/ar_2020.pdf",
    2021: "downloads/ar_2021.pdf",
    2022: "downloads/ar_2022.pdf",
    2023: "downloads/ar_2023.pdf",
    2024: "downloads/ar_2024.pdf",
    2025: "downloads/ar_2025.pdf"
}

results = {}

for yr, path in reports.items():
    doc = fitz.open(path)
    # Search backwards from end of document (financial statements are at the end)
    for pno in range(len(doc)-1, max(0, len(doc)-120), -1):
        txt = doc[pno].get_text()
        if "laporan arus kas" in txt.lower() or "statement of cash flows" in txt.lower():
            if "aktivitas operasi" in txt.lower() and ("penerimaan kas dari pelanggan" in txt.lower() or "cash received from customers" in txt.lower()):
                # this is the first page of statement of cash flows
                print(f"[{yr}] Cash Flow page found at p.{pno+1}")
                # let's look at lines on this page and next page
                combined_txt = txt + "\n" + doc[min(len(doc)-1, pno+1)].get_text()
                lines = [l.strip() for l in combined_txt.split('\n') if l.strip()]
                for idx, line in enumerate(lines):
                    if any(k in line.lower() for k in ["kas neto yang diperoleh dari aktivitas operasi", "kas neto yang diperoleh dari", "net cash provided by operating activities", "net cash flows provided by operating"]):
                        print(f"  [{yr}] CFO Line: {line}")
                        # print nearby lines to catch numbers
                        for offset in range(-3, 8):
                            if 0 <= idx + offset < len(lines):
                                print(f"      {lines[idx+offset]}")
                        break
                break
    doc.close()
