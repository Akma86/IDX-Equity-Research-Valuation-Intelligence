import fitz
import sys
import pandas as pd
import re

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect the exact lines of Financial Highlights in ar_2012 (page 5), ar_2015 (page 8), ar_2019 (page 8), ar_2024 (page 8), ar_2025 (page 8)
docs = {
    "2012": ("downloads/ar_2012.pdf", 4),
    "2015": ("downloads/ar_2015.pdf", 7),
    "2019": ("downloads/ar_2019.pdf", 7),
    "2024": ("downloads/ar_2024.pdf", 7),
    "2025": ("downloads/ar_2025.pdf", 7),
}

for yr, (path, pno) in docs.items():
    doc = fitz.open(path)
    txt = doc[pno].get_text()
    print(f"==================== {yr} (p.{pno+1}) ====================")
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    print(f"Total lines: {len(lines)}")
    # Print the lines containing numbers or keywords
    for l in lines[:40]:
        print("  ", l)
    doc.close()
