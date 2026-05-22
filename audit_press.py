import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.mohave.gov/departments/sheriff/press-releases/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Android 14; Mobile; rv:128.0) Gecko/128.0'}

def run_extraction():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Expanded pattern for 2026 disclosure formats
        pattern = re.compile(r'booking|roster|inmate|arrest|daily', re.IGNORECASE)
        
        links = soup.find_all('a')
        for link in links:
            text = link.get_text().strip()
            href = link.get('href', '')
            if pattern.search(text) or pattern.search(href):
                print(f"Evidence Located: {text} -> https://www.mohave.gov{href}")
                
    except Exception as e:
        print(f"Audit Failure: {e}")

if __name__ == "__main__":
    run_extraction()
