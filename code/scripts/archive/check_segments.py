import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open("downloads/ar_2024.pdf")
print("Searching segment info in ar_2024...")
for p in range(len(doc)):
    txt = doc[p].get_text().lower()
    if "informasi segmen" in txt or "segment information" in txt or "divisi mi instan" in txt:
        if "noodles" in txt and "dairy" in txt and "snack foods" in txt:
            print(f"Page {p+1} matches!")
            for l in [line.strip() for line in doc[p].get_text().split('\n') if line.strip()][:35]:
                print("  ", l)
            break
doc.close()
