import requests
from bs4 import BeautifulSoup

URL = "https://www.mohave.gov/departments/sheriff/press-releases/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Android 14; Mobile; rv:128.0) Gecko/128.0'}

def debug():
    r = requests.get(URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')
    print("--- TOP 10 SITE LINKS ---")
    for l in links[:10]:
        print(f"TEXT: {l.get_text().strip()} | HREF: {l.get('href')}")

if __name__ == "__main__":
    debug()
