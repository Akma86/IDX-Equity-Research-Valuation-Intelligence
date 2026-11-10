import fitz

files = ["ar_2012.pdf", "ar_2015.pdf", "ar_2019.pdf", "ar_2024.pdf", "ar_2025.pdf"]

for fn in files:
    path = f"downloads/{fn}"
    doc = fitz.open(path)
    print(f"\n==================== {fn} (Total pages: {len(doc)}) ====================")
    found = []
    for pno in range(min(40, len(doc))):
        txt = doc[pno].get_text()
        if "financial highlights" in txt.lower() or "ikhtisar keuangan" in txt.lower() or "ikhtisar kinerja" in txt.lower():
            found.append(pno)
    print(f"Matched pages: {found}")
    for pno in found[:2]:
        print(f"--- Page {pno+1} preview ---")
        lines = [l.strip() for l in doc[pno].get_text().split('\n') if l.strip()]
        for l in lines[:25]:
            print("  ", l)
    doc.close()
