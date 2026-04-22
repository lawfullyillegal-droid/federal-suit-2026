import requests
from bs4 import BeautifulSoup
import os

def run_stateful_audit(case_id):
    print(f"[*] INITIATING STATEFUL AUDIT: {case_id}")
    url = "https://apps.azcourts.gov/publicaccess/caselookup.aspx"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    }

    session = requests.Session()

    try:
        # 1. Capture Hidden Tokens
        print("[*] Retrieving Viewstate Tokens...")
        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        viewstate = soup.find(id="__VIEWSTATE")['value']
        validation = soup.find(id="__EVENTVALIDATION")['value']
        viewstate_gen = soup.find(id="__VIEWSTATEGENERATOR")['value']

        # 2. Construct the Payload
        payload = {
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": viewstate_gen,
            "__EVENTVALIDATION": validation,
            "ctl00$mainContent$txtCaseNumber": case_id,
            "ctl00$mainContent$btnSearch": "Search"
        }

        # 3. Execute the Post
        print(f"[*] Injecting Case ID: {case_id}")
        result = session.post(url, data=payload, headers=headers)
        
        # 4. Final Save
        html_path = f"04_Kingman_Audit/raw_data/{case_id}_FINAL_SNAPSHOT.html"
        with open(html_path, "w") as f:
            f.write(result.text)
            
        print(f"[+] AUDIT SUCCESSFUL. Captured: {html_path}")

    except Exception as e:
        print(f"[!] STATEFUL FAULT: {e}")

if __name__ == "__main__":
    run_stateful_audit("TR-2024-00143")
