import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

for fn in ["ar_2019.pdf", "ar_2024.pdf", "ar_2025.pdf"]:
    path = f"downloads/{fn}"
    doc = fitz.open(path)
    print(f"\n============================== {fn} ==============================")
    # Page 8 (index 7) or 7 (index 6) or 9 (index 8)
    for p in [6, 7, 8]:
        txt = doc[p].get_text()
        if "net sales" in txt.lower() or "penjualan neto" in txt.lower():
            print(f"--- {fn} Page {p+1} ---")
            print(txt[:3000])
    doc.close()
