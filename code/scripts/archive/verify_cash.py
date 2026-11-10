import fitz
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

reports = [
    (2012, "downloads/ar_2012.pdf"),
    (2013, "downloads/ar_2013.pdf"),
    (2015, "downloads/ar_2015.pdf"),
    (2016, "downloads/ar_2016.pdf"),
    (2017, "downloads/ar_2017.pdf"),
    (2019, "downloads/ar_2019.pdf"),
    (2020, "downloads/ar_2020.pdf"),
    (2021, "downloads/ar_2021.pdf"),
    (2022, "downloads/ar_2022.pdf"),
    (2024, "downloads/ar_2024.pdf"),
    (2025, "downloads/ar_2025.pdf"),
]

for yr, path in reports:
    doc = fitz.open(path)
    # Search for balance sheet
    for pno in range(len(doc)-1, 0, -1):
        txt = doc[pno].get_text()
        if ("laporan posisi keuangan" in txt.lower() or "statement of financial position" in txt.lower() or "neraca konsolidasian" in txt.lower()) and ("aset lancar" in txt.lower() or "current assets" in txt.lower()):
            if "kas dan setara kas" in txt.lower() or "cash and cash equivalents" in txt.lower():
                lines = [l.strip() for l in txt.split('\n') if l.strip()]
                for idx, l in enumerate(lines):
                    if "kas dan setara kas" in l.lower() or "cash and cash equivalents" in l.lower():
                        print(f"[{yr} BS p.{pno+1}]")
                        for off in range(-1, 6):
                            if 0 <= idx + off < len(lines):
                                print("   ", lines[idx+off])
                        break
                break
    doc.close()
