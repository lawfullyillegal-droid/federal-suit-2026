import requests
from bs4 import BeautifulSoup
import time
import random

def run_stealth_audit(case_id):
    url = "https://apps.azcourts.gov/publicaccess/caselookup.aspx"
    # Rotating to a common Android Mobile User-Agent
    mobile_ua = "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
    
    headers = {
        "User-Agent": mobile_ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Referer": url
    }
    
    while True:
        session = requests.Session()
        try:
            # Add a random stagger to bypass pattern detection
            stagger = random.uniform(5.0, 8.0)
            print(f"[*] COOLING DOWN ({stagger:.1f}s)... ATTEMPTING AT: {time.strftime('%H:%M:%S')}")
            time.sleep(stagger)
            
            r = session.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')

            captcha_img = soup.find('img', id='ctl00_mainContent_imgCaptcha')
            
            if captcha_img:
                print("\n[!] SUCCESS: WALL BREACHED. CAPTCHA FOUND.")
                img_url = "https://apps.azcourts.gov/publicaccess/" + captcha_img['src']
                with open("04_Kingman_Audit/evidence/captcha.jpg", "wb") as f:
                    f.write(session.get(img_url).content)
                
                print("[*] ACTION: Open 04_Kingman_Audit/evidence/captcha.jpg")
                code = input("[?] ENTER CHARACTERS: ")
                
                if not code: continue

                payload = {
                    "__VIEWSTATE": soup.find(id="__VIEWSTATE")['value'],
                    "__VIEWSTATEGENERATOR": soup.find(id="__VIEWSTATEGENERATOR")['value'],
                    "__EVENTVALIDATION": soup.find(id="__EVENTVALIDATION")['value'],
                    "ctl00$mainContent$txtCaseNumber": case_id,
                    "ctl00$mainContent$txtVerification": code,
                    "ctl00$mainContent$btnSearch": "Search"
                }

                print(f"[*] FINAL INJECTION: {case_id}")
                res = session.post(url, data=payload, headers=headers)

                if case_id in res.text:
                    print("[+] SUCCESS: Audit Captured.")
                    with open(f"04_Kingman_Audit/raw_data/{case_id}_FINAL.html", "w") as f:
                        f.write(res.text)
                    return 
                else:
                    print("[!] FAILURE

cat << 'EOF' > 04_Kingman_Audit/scrapers/kingman_stealth.py
import requests
from bs4 import BeautifulSoup
import time
import random

def run_stealth_audit(case_id):
    url = "https://apps.azcourts.gov/publicaccess/caselookup.aspx"
    # Chrome on Android Mobile Signature
    mobile_ua = "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
    
    headers = {
        "User-Agent": mobile_ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": url
    }
    
    while True:
        session = requests.Session()
        try:
            # Random stagger (5-10s) to bypass script detection
            wait_time = random.uniform(5.0, 10.0)
            print(f"[*] COOLING DOWN ({wait_time:.1f}s)... NEXT ATTEMPT: {time.strftime('%H:%M:%S')}")
            time.sleep(wait_time)
            
            r = session.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            captcha_img = soup.find('img', id='ctl00_mainContent_imgCaptcha')
            
            if captcha_img:
                print("\n[!] WALL BREACHED: CAPTCHA FOUND.")
                img_url = "https://apps.azcourts.gov/publicaccess/" + captcha_img['src']
                with open("04_Kingman_Audit/evidence/captcha.jpg", "wb") as f:
                    f.write(session.get(img_url).content)
                
                print("[*] ACTION: Open 04_Kingman_Audit/evidence/captcha.jpg")
                code = input("[?] ENTER CHARACTERS: ")
                if not code: continue

                payload = {
                    "__VIEWSTATE": soup.find(id="__VIEWSTATE")['value'],
                    "__VIEWSTATEGENERATOR": soup.find(id="__VIEWSTATEGENERATOR")['value'],
                    "__EVENTVALIDATION": soup.find(id="__EVENTVALIDATION")['value'],
                    "ctl00$mainContent$txtCaseNumber": case_id,
                    "ctl00$mainContent$txtVerification": code,
                    "ctl00$mainContent$btnSearch": "Search"
                }

                print(f"[*] FINAL INJECTION: {case_id}")
                res = session.post(url, data=payload, headers=headers)

                if case_id in res.text:
                    print("[+] SUCCESS: Deterministic Truth Secured.")
                    with open(f"04_Kingman_Audit/raw_data/{case_id}_FINAL.html", "w") as f:
                        f.write(res.text)
                    return 
                else:
                    print("[!] FAILURE: Data not in response. Session reset.")
            else:
                print("[*] Ghost Gate Active. Retrying...")

        except Exception as e:
            print(f"[!] FAULT: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_stealth_audit("TR-2024-00143")
