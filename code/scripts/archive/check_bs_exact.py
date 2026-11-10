import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

targets = [
    (2012, "downloads/ar_2012.pdf", 140, 144),
    (2013, "downloads/ar_2013.pdf", 146, 150),
    (2015, "downloads/ar_2015.pdf", 176, 180),
    (2019, "downloads/ar_2019.pdf", 214, 218),
    (2020, "downloads/ar_2020.pdf", 215, 219),
    (2021, "downloads/ar_2021.pdf", 177, 181),
    (2022, "downloads/ar_2022.pdf", 188, 193),
]

for yr, path, start_p, end_p in targets:
    doc = fitz.open(path)
    for p in range(start_p, end_p):
        txt = doc[p].get_text()
        if "kas dan setara kas" in txt.lower() and ("aset lancar" in txt.lower() or "current assets" in txt.lower()):
            lines = [l.strip() for l in txt.split('\n') if l.strip()]
            for idx, l in enumerate(lines):
                if "kas dan setara kas" in l.lower():
                    print(f"[{yr} p.{p+1}]")
                    for off in range(-1, 6):
                        if 0 <= idx + off < len(lines):
                            print("   ", lines[idx+off])
                    break
    doc.close()
