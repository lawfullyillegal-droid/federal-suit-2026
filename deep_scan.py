import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.mohave.gov/departments/sheriff/press-releases/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Android 14; Mobile; rv:128.0) Gecko/128.0'}

def deep_scan():
    print("Initiating Deep Scan of Sheriff Content...")
    try:
        r = requests.get(URL, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Target the main content area (often 'site-content')
        content = soup.find(id="site-content") or soup
        links = content.find_all('a')
        
        print(f"Total links found in content area: {len(links)}")

        # Look for any link containing '2026' or 'May'
        date_pattern = re.compile(r'2026|May|05-08|05-09', re.IGNORECASE)

        results = []
        for l in links:
            text = l.get_text().strip()
            href = l.get('href', '')
            if date_pattern.search(text) or date_pattern.search(href):
                if href.startswith('http'):
                    full_url = href
                else:
                    full_url = f"https://www.mohave.gov{href}"
                print(f"[TARGET] {text} | URL: {full_url}")
                results.append({'text': text, 'url': full_url})

        return results
                
    except Exception as e:
        print(f"Deep Scan Failed: {e}")
        return []

if __name__ == "__main__":
    deep_scan()
