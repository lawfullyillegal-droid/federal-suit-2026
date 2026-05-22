import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.mohave.gov/departments/sheriff/press-release/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def run():
    print("Intercepting Roster Feed...")
    r = requests.get(URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Target links that look like Date-based reports or "Inmate List"
    links = soup.find_all('a', string=re.compile(r'Inmate|List|Roster|May', re.IGNORECASE))
    
    for l in links:
        t = l.get_text().strip()
        h = l.get('href', '')
        full_url = h if h.startswith('http') else f"https://www.mohave.gov{h}"
        print(f"[TARGET] {t} -> {full_url}")

if __name__ == "__main__":
    run()
