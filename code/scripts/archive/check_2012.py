import fitz
import sys

# Set stdout encoding to utf-8 to avoid charmap errors
sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open("downloads/ar_2012.pdf")
print("Total pages in ar_2012.pdf:", len(doc))
for pno in range(2, 12):
    txt = doc[pno].get_text()
    if any(k in txt.lower() for k in ["ikhtisar", "penjualan", "highlights", "neraca", "rugi"]):
        print(f"\n--- ar_2012 Page {pno+1} ---")
        for line in [l.strip() for l in txt.split('\n') if l.strip()][:30]:
            print("  ", line)
doc.close()
