import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

def find_cfo_in_doc(doc_path):
    doc = fitz.open(doc_path)
    print(f"\n==================== Searching in {doc_path} ====================")
    for pno in range(len(doc)):
        txt = doc[pno].get_text()
        if "kas neto yang diperoleh dari" in txt.lower() or "net cash provided by operating" in txt.lower() or "net cash flows provided by operating" in txt.lower():
            print(f"Match on Page {pno+1}:")
            lines = [l.strip() for l in txt.split('\n') if l.strip()]
            for i, l in enumerate(lines):
                if any(k in l.lower() for k in ["kas neto yang", "net cash provided", "net cash flow", "kas dan setara kas pada akhir", "cash and cash equivalents at end"]):
                    # print nearby lines
                    start = max(0, i-2)
                    end = min(len(lines), i+4)
                    print("  Snippet:", " // ".join(lines[start:end]))
    doc.close()

find_cfo_in_doc("downloads/ar_2012.pdf")
find_cfo_in_doc("downloads/ar_2019.pdf")
find_cfo_in_doc("downloads/ar_2024.pdf")
