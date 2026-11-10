import fitz # PyMuPDF
import re

doc = fitz.open("test_2015.pdf")
print("Total pages in test_2015.pdf:", len(doc))

target_pages = []
for pno in range(min(50, len(doc))):
    text = doc[pno].get_text()
    if any(k in text.lower() for k in ["financial highlights", "ikhtisar keuangan", "ikhtisar data keuangan"]):
        print(f"Page {pno+1} matches!")
        target_pages.append(pno)

for pno in target_pages:
    print(f"\n--- Page {pno+1} Sample Text ---")
    lines = [line.strip() for line in doc[pno].get_text().split('\n') if line.strip()]
    for line in lines[:35]:
        print("  ", line)

# Clean up test file
doc.close()
