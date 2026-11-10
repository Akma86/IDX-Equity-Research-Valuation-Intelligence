import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

for yr in [2012, 2020, 2021, 2022, 2023]:
    path = f"downloads/ar_{yr}.pdf"
    doc = fitz.open(path)
    for pno in range(len(doc)):
        txt = doc[pno].get_text()
        if "laporan arus kas" in txt.lower() or "statement of cash flows" in txt.lower():
            if "penerimaan kas dari pelanggan" in txt.lower() or "cash received from customers" in txt.lower():
                print(f"[{yr}] Found on page {pno+1}")
                # print 40 lines
                lines = [l.strip() for l in txt.split('\n') if l.strip()]
                for l in lines[:30]:
                    print("  ", l)
                break
    doc.close()
