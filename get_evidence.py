import requests
from bs4 import BeautifulSoup
import re

# TARGETING THE 2026 SILO
URL = "https://www.mohave.gov/departments/sheriff/press-release/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def run():
    print("Bypassing Silo Infrastructure...")
    r = requests.get(URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Looking for 'May' or '05-0' to find Friday (05-08) and Saturday (05-09)
    pattern = re.compile(r'May|05-08|05-09|Booking|Arrest', re.IGNORECASE)
    
    links = soup.find_all('a')
    found = False
    for l in links:
        t = l.get_text().strip()
        h = l.get('href', '')
        if pattern.search(t) or pattern.search(h):
            full_url = h if h.startswith('http') else f"https://www.mohave.gov{h}"
            print(f"[!] EVIDENCE DISCOVERED: {t}")
            print(f"    LINK: {full_url}")
            found = True
            
    if not found:
        print("Status: Target content shielded. Moving to Directory Enumeration...")

if __name__ == "__main__":
    run()
