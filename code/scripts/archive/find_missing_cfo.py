import fitz
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

years_needed = [2010, 2013, 2016, 2017, 2020, 2021, 2022]

for fn in ["ar_2012.pdf", "ar_2015.pdf", "ar_2019.pdf", "ar_2024.pdf"]:
    doc = fitz.open(f"downloads/{fn}")
    print(f"\n--- Searching in {fn} ---")
    for pno in range(len(doc)):
        txt = doc[pno].get_text()
        # Look for cash flow from operating activities or kas dari aktivitas operasi
        if "aktivitas operasi" in txt.lower() and ("arus kas" in txt.lower() or "cash flow" in txt.lower()):
            for y in years_needed:
                if str(y) in txt:
                    lines = [l.strip() for l in txt.split('\n') if l.strip()]
                    for i, l in enumerate(lines):
                        if any(k in l.lower() for k in ["kas neto yang diperoleh", "net cash provided by operating", "arus kas neto yang diperoleh"]):
                            print(f"File {fn} Page {pno+1} for Year context around {y}:")
                            print("  " + " | ".join(lines[max(0, i-2):min(len(lines), i+6)]))
                            break
    doc.close()
