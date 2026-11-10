import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

def extract_rows_by_coords(pdf_path, pno):
    doc = fitz.open(pdf_path)
    page = doc[pno]
    words = page.get_text("words")
    # Group words by approximate y coordinate (within 4 points)
    lines_dict = {}
    for w in words:
        x0, y0, x1, y1, text = w[:5]
        # find matching line key
        matched = False
        for y_key in lines_dict:
            if abs(y_key - y0) < 4:
                lines_dict[y_key].append((x0, text))
                matched = True
                break
        if not matched:
            lines_dict[y0] = [(x0, text)]
    
    sorted_y = sorted(lines_dict.keys())
    extracted_lines = []
    for y in sorted_y:
        # sort words in line by x0
        line_words = sorted(lines_dict[y], key=lambda x: x[0])
        extracted_lines.append(" ".join(w[1] for w in line_words))
    doc.close()
    return extracted_lines

for yr, path, pno in [("2012", "downloads/ar_2012.pdf", 4), ("2015", "downloads/ar_2015.pdf", 7), ("2025", "downloads/ar_2025.pdf", 7)]:
    print(f"\n==================== {yr} Lines with Coordinates ====================")
    rows = extract_rows_by_coords(path, pno)
    for r in rows:
        if any(c.isdigit() for c in r) and any(k in r.lower() for k in ["sales", "penjualan", "gross", "ebit", "income", "asset", "ekuitas", "equity", "debt", "share", "saham"]):
            print("  ", r)
