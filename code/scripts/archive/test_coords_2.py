import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

from test_coords import extract_rows_by_coords

for yr, path, pno in [("2019", "downloads/ar_2019.pdf", 7), ("2020", "downloads/ar_2020.pdf", 7), ("2024", "downloads/ar_2024.pdf", 7)]:
    print(f"\n==================== {yr} Lines with Coordinates ====================")
    rows = extract_rows_by_coords(path, pno)
    for r in rows:
        if any(c.isdigit() for c in r) and any(k in r.lower() for k in ["sales", "penjualan", "gross", "ebit", "income", "asset", "ekuitas", "equity", "debt", "share", "saham"]):
            print("  ", r)
