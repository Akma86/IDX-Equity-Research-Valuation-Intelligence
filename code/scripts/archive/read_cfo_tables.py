import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

pages_to_check = [
    ("downloads/ar_2012.pdf", 147), # 0-indexed for 148
    ("downloads/ar_2015.pdf", 184), # 0-indexed for 185
    ("downloads/ar_2019.pdf", 222), # 0-indexed for 223
    ("downloads/ar_2025.pdf", 185)  # 0-indexed for 186
]

for path, pno in pages_to_check:
    doc = fitz.open(path)
    print(f"\n==================== {path} Page {pno+1} ====================")
    txt = doc[pno].get_text()
    for l in txt.split('\n')[:50]:
        if l.strip():
            print("  ", l.strip())
    doc.close()
