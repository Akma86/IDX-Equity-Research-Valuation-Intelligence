import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

docs = {
    "2012": ("downloads/ar_2012.pdf", 4),
    "2015": ("downloads/ar_2015.pdf", 7),
    "2019": ("downloads/ar_2019.pdf", 7),
    "2024": ("downloads/ar_2024.pdf", 7),
    "2025": ("downloads/ar_2025.pdf", 7),
}

for yr, (path, pno) in docs.items():
    with pdfplumber.open(path) as pdf:
        p = pdf.pages[pno]
        tables = p.extract_tables()
        print(f"\n==================== {yr} Tables ({len(tables)}) ====================")
        for i, t in enumerate(tables):
            print(f"Table {i} rows: {len(t)}")
            for row in t[:6]:
                print("  ", [str(cell).replace('\n', ' ') for cell in row if cell])
