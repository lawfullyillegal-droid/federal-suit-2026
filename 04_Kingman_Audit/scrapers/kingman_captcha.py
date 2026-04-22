import requests
from bs4 import BeautifulSoup
import os

def harvest_captcha():
    url = "https://apps.azcourts.gov/publicaccess/caselookup.aspx"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    session = requests.Session()

    print("[*] Accessing Portal to trigger CAPTCHA...")
    r = session.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Look for the CAPTCHA image URL
    img_tag = soup.find('img', id='ctl00_mainContent_imgCaptcha')
    if img_tag:
        img_url = "https://apps.azcourts.gov/publicaccess/" + img_tag['src']
        img_data = session.get(img_url).content
        
        with open("04_Kingman_Audit/evidence/captcha_challenge.jpg", "wb") as f:
            f.write(img_data)
        
        print("[+] CAPTCHA captured to: 04_Kingman_Audit/evidence/captcha_challenge.jpg")
        print("[*] Open this image, then we will run the final POST with the solution.")
        
        # Save session tokens for the next step
        with open(".session_tokens", "w") as f:
            f.write(f"{soup.find(id='__VIEWSTATE')['value']}\n")
            f.write(f"{soup.find(id='__EVENTVALIDATION')['value']}\n")
            f.write(f"{soup.find(id='__VIEWSTATEGENERATOR')['value']}")
    else:
        print("[!] No CAPTCHA found. The wall might have temporarily lowered.")

if __name__ == "__main__":
    harvest_captcha()
