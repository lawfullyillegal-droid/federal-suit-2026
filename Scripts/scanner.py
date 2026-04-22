import requests
from bs4 import BeautifulSoup

# The 'identifiers' you want to scan for
MY_IDENTIFIERS = ["yourname@email.com", "MyFull Name", "555-0199"]
TARGET_URL = "https://example-site.com/forum"

def scan_site(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This converts the whole page to text to look for your data
        page_text = soup.get_text()
        
        for item in MY_IDENTIFIERS:
            if item in page_text:
                print(f"⚠️ ALERT: Found '{item}' on {url}")
    except Exception as e:
        print(f"Error scanning {url}: {e}")

scan_site(TARGET_URL)
