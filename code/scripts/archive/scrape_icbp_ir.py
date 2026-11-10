import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def check_url(url):
    print(f"Checking {url}...")
    try:
        resp = requests.get(url, headers=headers, verify=False, timeout=15)
        print(f"Status: {resp.status_code}, Length: {len(resp.text)}")
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = soup.find_all('a', href=True)
        pdf_links = [l['href'] for l in links if '.pdf' in l['href'].lower()]
        print(f"Found {len(pdf_links)} PDF links")
        for p in pdf_links[:15]:
            print("  ", p)
    except Exception as e:
        print("Error:", e)

check_url("https://www.indofoodcbp.com/investor-relations/financial-statements")
check_url("https://www.indofoodcbp.com/investor-relations/annual-report")

