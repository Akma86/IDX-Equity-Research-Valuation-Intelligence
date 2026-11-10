import requests
import urllib3
urllib3.disable_warnings()

patterns = [
    'ICBP_AR_{y}.pdf', 'AR_ICBP_{y}.pdf', 'AR ICBP {y}.pdf', 'AR ICBP_{y}.pdf',
    'ICBP - AR {y}.pdf', 'ICBP_AR_{y}_web.pdf', 'ICBP_{y}AR.pdf', 'icbp_{y}ar.pdf',
    'ICBP_Annual_Report_{y}.pdf', 'Annual_Report_ICBP_{y}.pdf', 'AR_ICBP_{y}_final.pdf',
    'ICBP_AR_{y}_web version.pdf', 'ICBP - AR {y} Preview_web version.pdf',
    'AR ICBP {yy}_final.pdf', 'ICBP_{y}AR_final.pdf'
]

for y in range(2010, 2026):
    yy = str(y)[2:]
    found = False
    for p in patterns:
        filename = p.format(y=y, yy=yy)
        for sub in ['annual', 'statement', 'file', 'report']:
            url = f'https://www.indofoodcbp.com/uploads/{sub}/{filename}'
            try:
                r = requests.head(url, verify=False, timeout=3)
                if r.status_code == 200:
                    print(f"{y}: FOUND -> {url} ({r.headers.get('Content-Length', '?')} bytes)")
                    found = True
                    break
            except Exception:
                pass
        if found:
            break
    if not found:
        print(f"{y}: not matched")
