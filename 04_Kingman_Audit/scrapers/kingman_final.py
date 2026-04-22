import requests
from bs4 import BeautifulSoup
import time

def finalize_audit(case_id):
    url = "https://apps.azcourts.gov/publicaccess/caselookup.aspx"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    
    while True:
        session = requests.Session()
        print(f"\n[*] INITIATING SESSION ATTEMPT: {time.strftime('%H:%M:%S')}")
        
        try:
            r = session.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')

            vs = soup.find(id="__VIEWSTATE")['value']
            vsg = soup.find(id="__VIEWSTATEGENERATOR")['value']
            ev = soup.find(id="__EVENTVALIDATION")['value']

            captcha_img = soup.find('img', id='ctl00_mainContent_imgCaptcha')
            captcha_code = ""
            
            if captcha_img:
                img_url = "https://apps.azcourts.gov/publicaccess/" + captcha_img['src']
                img_data = session.get(img_url).content
                with open("04_Kingman_Audit/evidence/captcha.jpg", "wb") as f:
                    f.write(img_data)
                print("[!] CAPTCHA DETECTED. Check 04_Kingman_Audit/evidence/captcha.jpg")
                captcha_code = input("[?] ENTER CODE (or press Enter to retry session): ")
                if not captcha_code: continue

            payload = {
                "__VIEWSTATE": vs,
                "__VIEWSTATEGENERATOR": vsg,
                "__EVENTVALIDATION": ev,
                "ctl00$mainContent$txtCaseNumber": case_id,
                "ctl00$mainContent$txtVerification": captcha_code,
                "ctl00$mainContent$btnSearch": "Search"
            }

            print(f"[*] Submitting Case ID: {case_id}")
            response = session.post(url, data=payload, headers=headers, timeout=15)

            if case_id in response.text:
                print("[+] SUCCESS: Data Secured.")
                with open(f"04_Kingman_Audit/raw_data/{case_id}_FINAL_SNAPSHOT.html", "w") as f:
                    f.write(response.text)
                break
            else:
                print("[!] FAILURE: Data not in response. Session likely invalidated.")
                time.sleep(2)

        except Exception as e:
            print(f"[!] SESSION ERROR: {e}")
            time.sleep(2)

if __name__ == "__main__":
    finalize_audit("TR-2024-00143")
