import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.mohave.gov/departments/sheriff/press-releases/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Android 14; Mobile; rv:128.0) Gecko/128.0'}

def run():
    print("Pulling Mohave Press Feed...")
    try:
        r = requests.get(URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all('a')
        
        # Searching for 'Daily' because today is Saturday; they often bundle weekend bookings.
        pattern = re.compile(r'booking|roster|arrest|daily', re.IGNORECASE)
        
        print("\n--- LIVE AUDIT SOURCES ---")
        for l in links:
            t = l.get_text().strip()
            h = l.get('href', '')
            if pattern.search(t) or pattern.search(h):
                print(f"[FOUND] {t}")
                print(f"        URL: https://www.mohave.gov{h}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
