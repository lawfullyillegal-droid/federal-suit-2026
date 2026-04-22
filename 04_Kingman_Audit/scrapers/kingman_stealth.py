import requests
from bs4 import BeautifulSoup
import time
import random

def run_deep_stealth_audit(case_id):
    url = "https://apps.azcourts.gov/publicaccess/caselookup.aspx"
    mobile_ua = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    
    headers = {
        "User-Agent": mobile_ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,video/webm,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": url,
        "Connection": "keep-alive"
    }
    
    # FIX: Initialize the session OUTSIDE the loop to keep cookies alive
    session = requests.Session()
    
    while True:
        try:
            wait_time = random.uniform(12.0, 20.0)
            print(f"[*] DEEP COOLING ({wait_time:.1f}s)... ATTEMPTING AT: {time.strftime('%H:%M:%S')}")
            time.sleep(wait_time)
            
            # Step A: Get tokens using the persistent session
            r = session.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(r.text, 'html.parser')
            captcha_img = soup.find('img', id='ctl00_mainContent_imgCaptcha')
            
            if captcha_img:
                print("\n[!] SUCCESS: CAPTCHA FOUND.")
                img_url = "https://apps.azcourts.gov/publicaccess/" + captcha_img['src']
                img_data = session.get(img_url, headers=headers).content
                with open("04_Kingman_Audit/evidence/captcha.jpg", "wb") as f:
                    f.write(img_data)
                
                print("[*] ACTION: Check 04_Kingman_Audit/evidence/captcha.jpg")
                code = input("[?] ENTER CODE: ")
                if not code: continue

                # Step B: Submit search using the SAME cookies and tokens
                payload = {
                    "__VIEWSTATE": soup.find(id="__VIEWSTATE")['value'],
                    "__VIEWSTATEGENERATOR": soup.find(id="__VIEWSTATEGENERATOR")['value'],
                    "__EVENTVALIDATION": soup.find(id="__EVENTVALIDATION")['value'],
                    "ctl00$mainContent$txtCaseNumber": case_id,
                    "ctl00$mainContent$txtVerification": code,
                    "ctl00$mainContent$btnSearch": "Search"
                }

                print(f"[*] FINALIZING AUDIT: {case_id}")
                res = session.post(url, data=payload, headers=headers)

                if case_id in res.text:
                    print("[+] SUCCESS: Snapshot Secured.")
                    with open(f"04_Kingman_Audit/raw_data/{case_id}_FINAL.html", "w") as f:
                        f.write(res.text)
                    return 
                else:
                    print("[!] FAILURE: Case data missing. Session might be flagged.")
            else:
                print("[*] Ghost Gate persists. Holding session and retrying...")

        except Exception as e:
            print(f"[!] FAULT: {e}")
            time.sleep(15)

if __name__ == "__main__":
    run_deep_stealth_audit("TR-2024-00143")
