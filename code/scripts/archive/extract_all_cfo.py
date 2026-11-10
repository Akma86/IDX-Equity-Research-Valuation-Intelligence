import fitz
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

files = ["ar_2012.pdf", "ar_2015.pdf", "ar_2019.pdf", "ar_2025.pdf"]

for fn in files:
    doc = fitz.open(f"downloads/{fn}")
    print(f"\n==================== {fn} ====================")
    for p in range(len(doc)):
        txt = doc[p].get_text()
        if "statement of cash flows" in txt.lower() or "laporan arus kas" in txt.lower():
            # Check if this is MD&A or audited report
            if any(k in txt.lower() for k in ["arus kas neto yang diperoleh dari aktivitas operasi", "net cash flow provided by operating activities", "aktivitas operasi"]):
                print(f"--- {fn} Page {p+1} ---")
                for line in txt.split('\n'):
                    l = line.strip()
                    if any(k in l.lower() for k in ["operasi", "operating", "kas dan setara kas", "cash and cash equivalents", "investasi", "investing", "pendanaan", "financing"]):
                        print("  ", l)
    doc.close()
