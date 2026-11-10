import fitz
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

pages = [
    ("downloads/ar_2012.pdf", [147, 148]),
    ("downloads/ar_2015.pdf", [184, 185]),
    ("downloads/ar_2019.pdf", [222, 223]),
    ("downloads/ar_2025.pdf", [185, 186])
]

for path, pnos in pages:
    doc = fitz.open(path)
    print(f"\n==================== {path} ====================")
    for pno in pnos:
        txt = doc[pno].get_text()
        for block in txt.split('\n\n'):
            if any(k in block.lower() for k in ["arus kas neto yang diperoleh dari aktivitas operasi", "net cash flows provided by operating activities", "net cash provided by operating activities", "kas dan setara kas pada akhir tahun", "cash and cash equivalents at end of year"]):
                print(f"--- Page {pno+1} Match ---")
                print(block.strip())
    doc.close()
