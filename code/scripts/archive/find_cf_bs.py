import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = ["ar_2012.pdf", "ar_2015.pdf", "ar_2019.pdf", "ar_2024.pdf", "ar_2025.pdf"]

for fn in files:
    doc = fitz.open(f"downloads/{fn}")
    cf_pages = []
    bs_pages = []
    for pno in range(len(doc)-1, -1, -1):
        txt = doc[pno].get_text().lower()
        if "arus kas neto yang diperoleh dari aktivitas operasi" in txt or "net cash flows provided by operating activities" in txt:
            cf_pages.append(pno)
        if ("kas dan setara kas" in txt or "cash and cash equivalents") and ("aset lancar" in txt or "current assets" in txt) and ("laporan posisi keuangan" in txt or "statements of financial position" in txt):
            bs_pages.append(pno)
    print(f"{fn}: CF pages {cf_pages[:2]}, BS pages {bs_pages[:2]}")
    doc.close()
