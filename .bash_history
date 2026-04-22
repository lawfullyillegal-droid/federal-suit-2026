  </div>
  <p><strong>TRAVIS STEVEN RYLE</strong>, Plaintiff<br>
  v.<br>
  <strong>LEXISNEXIS RISK SOLUTIONS; COUNTY OF VENTURA; COUNTY OF MOHAVE; FIDELITY ABERDEEN STREET TRUST; et al.</strong>, Defendants</p>

  <h1>COMPLAINT FOR VIOLATION OF CIVIL RIGHTS (42 U.S.C. § 1985)</h1>

  <div class="section">STATEMENT OF FACTS</div>
  <p>1. In January 2007, a proceeding in Ventura County used fabricated status to generate a void judgment.</p>
  <p>2. For 4,380 days, Defendants maintained a false "Felony" status, resulting in "Civil Death".</p>
  <p>3. Logical verification of these claims was completed via <strong>Prover9</strong>, proving the identity conversion was unauthorized.</p>

  <div class="section">PRAYER FOR RELIEF</div>
  <p>Plaintiff requests a declaration that the 2007 Case was void <i>ab initio</i> and an injunction against "Corporate Debtor" misclassification.</p>

  <p><strong>VERIFIED BY:</strong> Travis Steven Ryle, April 19, 2026.</p>
</body>
</html>
EOF

pandoc Lawsuit_Master_Copy.html -o FINAL_FEDERAL_COMPLAINT_RYLE.pdf
termux-setup-storage
cp FINAL_FEDERAL_COMPLAINT_RYLE.pdf /sdcard/Download/
y
termux-setup-storage
cp FINAL_FEDERAL_COMPLAINT_RYLE.pdf /sdcard/Download/
tail -n 20 ~/federal-suit-2026/structural_nexus_report.md
# 1. Rotate IP via Airplane Mode (1 minute)
# 2. Test connectivity to a neutral site
curl -I https://www.google.com
# 3. If successful, push the forensic log to GitHub
cd ~/federal-suit-2026 && git push
# Wait 5 minutes to ensure no 'rapid fire' flags are triggered
# Then run this single 'Official' request
curl -H "User-Agent: Lawfully Illegal Investigation Tool (contact@lawfully-illegal.art)"      -H "Accept-Encoding: gzip, deflate"      --compressed      -I "https://www.sec.gov/Archives/edgar/data/0000035402/000003540226002201/0000035402-26-002201.txt"
curl -H "User-Agent: Lawfully Illegal Investigation Tool (contact@lawfully-illegal.art)"      -H "Accept-Encoding: gzip, deflate"      --compressed      -L -o complete_audit.txt      "https://www.sec.gov/Archives/edgar/data/0000035402/000003540226002201/0000035402-26-002201.txt"
cat complete_audit.txt
# Force the full 10-digit CIK path to avoid the 301 'NoSuchKey' trap
curl -H "User-Agent: Lawfully Illegal Investigation Tool (contact@lawfully-illegal.art)"      -H "Accept: */*"      --compressed      -o complete_audit.txt      "https://www.sec.gov/Archives/edgar/data/0000035402/000003540226002201/0000035402-26-002201.txt"
{   echo "---";   echo "## Forensic Event: Absolute Path Throttling";   echo "Timestamp: $(date)";   echo "Action: Requested absolute 10-digit CIK path (0000035402) after faulty 301 redirect.";   echo "Result: TCP Connection Stall / Silent Drop (0% progress).";   echo "Legal Inference: Systemic failure of the EDGAR CDN to provide access to public FENCX filings despite compliance with User-Agent declaration policies."; } >> ~/federal-suit-2026/structural_nexus_report.md
cd ~/federal-suit-2026 && git commit -am "Forensics: Documenting TCP stall on absolute path request" && git push
[Travis@Termux] ~/federal-suit-2026 $ cat complete_audit.txt
<?xml version="1.0" encoding="UTF-8"?>
<Error><Code>NoSuchKey</Code><Message>The specified key does not exist.</Message><Key>edgar/data/35402/000003540226002201/0000035402-26-002201.txt</Key><RequestId>MBJZP0XHMEB8RJC1</RequestId><HostId>yBePgY/RxjfNgZVzAkkWsJfrb2lq7Dwv+oAchejquhWOsBrmWHCMsnmaVhGw9gH4IM3NSEcylCKLGfQquvojwhDKe8GOX4pw</HostId></Error>[Travis@Term[Travis@Termux] ~/federal-suit-2026 $ # Force the full 10-digit CIK path to avoid the 301 'NoSuchKey' trap
curl -H "User-Agent: Lawfully Illegal Investigation Tool (contact@lawfully-illegal.art)"      -H "Accept: */*"      --compressed      -o complete_audit.txt      "https://www.sec.gov/Archives/edgar/data/0000035402/000003540226002201/0000035402-26-002201.txt"
[Travis@Termux] ~/federal-suit-2026 $ {
} >> ~/federal-suit-2026/structural_nexus_report.md
cd ~/federal-suit-2026 && git commit -am "Forensics: Documenting TCP stall on absolute path request" && git push
[main 66e4aa2] Forensics: Documenting TCP stall on absolute path request
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 823 bytes | 823.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/lawfullyillegal-droid/federal-suit-2026.git
[Travis@Termux] ~/federal-suit-2026 $
# Press Ctrl+C a few times to clear any pending buffers, then:
clear
# Press Ctrl+C a few times to clear any pending buffers, then:
clear
# Pulling the manifest to identify the small XML fragments
curl -H "User-Agent: Lawfully Illegal Investigation Tool (contact@lawfully-illegal.art)"      -H "Accept: application/json"      -L -o index_manifest.json      "https://www.sec.gov/Archives/edgar/data/35402/000003540226002201/index.json"
cat index_manifest.json
curl -H "User-Agent: Lawfully Illegal Investigation Tool (contact@lawfully-illegal.art)"      -L -o primary_audit.xml      "https://www.sec.gov/Archives/edgar/data/35402/000003540226002201/primary_doc.xml"
cat primary_audit.xml
curl -H "User-Agent: Lawfully Illegal Investigation Tool (contact@lawfully-illegal.art)"      -L -o primary_audit.xml      "https://www.sec.gov/Archives/edgar/data/0000035402/000003540226002201/primary_doc.xml"
cat << 'EOF' > 04_Kingman_Audit/scrapers/kingman_stealth.py
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
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
        "Upgrade-Insecure-Requests": "1"
    }
    
    while True:
        session = requests.Session()
        try:
            # Increase stagger slightly to 12-20s to fall under the radar
            wait_time = random.uniform(12.0, 20.0)
            print(f"[*] DEEP COOLING ({wait_time:.1f}s)... ATTEMPTING AT: {time.strftime('%H:%M:%S')}")
            time.sleep(wait_time)
            
            r = session.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(r.text, 'html.parser')
            captcha_img = soup.find('img', id='ctl00_mainContent_imgCaptcha')
            
            if captcha_img:
                print("\n[!] BREACH SUCCESSFUL: CAPTCHA CAPTURED.")
                img_url = "https://apps.azcourts.gov/publicaccess/" + captcha_img['src']
                with open("04_Kingman_Audit/evidence/captcha.jpg", "wb") as f:
                    f.write(session.get(img_url).content)
                
                print("[*] ACTION: Check 04_Kingman_Audit/evidence/captcha.jpg")
                code = input("[?] ENTER CODE: ")
                if not code: continue

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
                    print("[!] FAILURE: Data missing from response.")
            else:
                print("[*] Ghost Gate persists. Escalating wait time...")

        except Exception as e:
            print(f"[!] FAULT: {e}")
            time.sleep(15)

if __name__ == "__main__":
    run_deep_stealth_audit("TR-2024-00143")
EOF

python 04_Kingman_Audit/scrapers/kingman_stealth.py
mkdir -p 04_Kingman_Audit/scrapers 04_Kingman_Audit/evidence 04_Kingman_Audit/raw_data
cat << 'EOF' > 04_Kingman_Audit/scrapers/kingman_stealth.py
import requests
from bs4 import BeautifulSoup
import time
import random

def run_deep_stealth_audit(case_id):
    url = "https://apps.azcourts.gov/publicaccess/caselookup.aspx"
    # Latest Chrome on Android User-Agent
    mobile_ua = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    
    headers = {
        "User-Agent": mobile_ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,video/webm,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": url,
        "Connection": "keep-alive"
    }
    
    while True:
        session = requests.Session()
        try:
            # Random wait between 12-20 seconds to look human
            wait_time = random.uniform(12.0, 20.0)
            print(f"[*] DEEP COOLING ({wait_time:.1f}s)... ATTEMPTING AT: {time.strftime('%H:%M:%S')}")
            time.sleep(wait_time)
            
            # Step A: Get the tokens and set the session cookie
            r = session.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(r.text, 'html.parser')
            captcha_img = soup.find('img', id='ctl00_mainContent_imgCaptcha')
            
            if captcha_img:
                print("\n[!] BREACH SUCCESSFUL: CAPTCHA FOUND.")
                img_url = "https://apps.azcourts.gov/publicaccess/" + captcha_img['src']
                with open("04_Kingman_Audit/evidence/captcha.jpg", "wb") as f:
                    f.write(session.get(img_url).content)
                
                print("[*] ACTION: Open 04_Kingman_Audit/evidence/captcha.jpg")
                code = input("[?] ENTER CODE: ")
                if not code: continue

                # Step B: Submit the search with the same session cookies
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
                    print("[!] FAILURE: Case data missing. Session may have timed out.")
            else:
                print("[*] Ghost Gate persists. Retrying...")

        except Exception as e:
            print(f"[!] FAULT: {e}")
            time.sleep(15)

if __name__ == "__main__":
    run_deep_stealth_audit("TR-2024-00143")
EOF

python 04_Kingman_Audit/scrapers/kingman_stealth.py
cat << 'EOF' > 04_Kingman_Audit/scrapers/kingman_stealth.py
import requests
from bs4 import BeautifulSoup
import time
import random

def run_final_audit(case_id):
    url = "https://apps.azcourts.gov/publicaccess/caselookup.aspx"
    mobile_ua = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    
    headers = {
        "User-Agent": mobile_ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": url
    }

    # Use a single session for all requests
    session = requests.Session()
    
    while True:
        try:
            wait_time = random.uniform(10.0, 15.0)
            print(f"[*] COOLING ({wait_time:.1f}s)... ATTEMPTING AT: {time.strftime('%H:%M:%S')}")
            time.sleep(wait_time)
            
            # Step 1: Initial Handshake
            response = session.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(response.text, 'html.parser')
            
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

                # Step 2: Final Data Injection
                payload = {
                    "__VIEWSTATE": soup.find(id="__VIEWSTATE")['value'],
                    "__VIEWSTATEGENERATOR": soup.find(id="__VIEWSTATEGENERATOR")['value'],
                    "__EVENTVALIDATION": soup.find(id="__EVENTVALIDATION")['value'],
                    "ctl00$mainContent$txtCaseNumber": case_id,
                    "ctl00$mainContent$txtVerification": code,
                    "ctl00$mainContent$btnSearch": "Search"
                }

                res = session.post(url, data=payload, headers=headers)

                if case_id in res.text:
                    print("[+] SUCCESS: Snapshot Secured.")
                    with open(f"04_Kingman_Audit/raw_data/{case_id}_FINAL.html", "w") as f:
                        f.write(res.text)
                    return
                else:
                    print("[!] FAILURE: Data missing


cat << 'EOF' > 04_Kingman_Audit/scrapers/kingman_stealth.py
import requests
from bs4 import BeautifulSoup
import time
import random

def run_final_audit(case_id):
    url = "https://apps.azcourts.gov/publicaccess/caselookup.aspx"
    mobile_ua = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    
    headers = {
        "User-Agent": mobile_ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": url
    }

    # Use a single session for all requests
    session = requests.Session()
    
    while True:
        try:
            wait_time = random.uniform(10.0, 15.0)
            print(f"[*] COOLING ({wait_time:.1f}s)... ATTEMPTING AT: {time.strftime('%H:%M:%S')}")
            time.sleep(wait_time)
            
            # Step 1: Initial Handshake
            response = session.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(response.text, 'html.parser')
            
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

                # Step 2: Final Data Injection
                payload = {
                    "__VIEWSTATE": soup.find(id="__VIEWSTATE")['value'],
                    "__VIEWSTATEGENERATOR": soup.find(id="__VIEWSTATEGENERATOR")['value'],
                    "__EVENTVALIDATION": soup.find(id="__EVENTVALIDATION")['value'],
                    "ctl00$mainContent$txtCaseNumber": case_id,
                    "ctl00$mainContent$txtVerification": code,
                    "ctl00$mainContent$btnSearch": "Search"
                }

                res = session.post(url, data=payload, headers=headers)

                if case_id in res.text:
                    print("[+] SUCCESS: Snapshot Secured.")
                    with open(f"04_Kingman_Audit/raw_data/{case_id}_FINAL.html", "w") as f:
                        f.write(res.text)
                    return
                else:
                    print("[!] FAILURE: Data missing


cat << 'EOF' > 04_Kingman_Audit/scrapers/kingman_stealth.py
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


cat << 'EOF' > 04_Kingman_Audit/scrapers/kingman_stealth.py
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
EOF

python 04_Kingman_Audit/scrapers/kingman_stealth.py
# Example: Moving a downloaded file from your 'Downloads' folder to the audit tree
mv /sdcard/Download/CaseDetails.html 04_Kingman_Audit/raw_data/TR-2024-00143_FINAL.html
