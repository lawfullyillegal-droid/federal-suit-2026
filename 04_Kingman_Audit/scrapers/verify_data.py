from bs4 import BeautifulSoup
import os

file_path = "04_Kingman_Audit/raw_data/TR-2024-00143_FINAL_SNAPSHOT.html"

if not os.path.exists(file_path):
    print("[!] File not found.")
else:
    with open(file_path, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    # 1. Check for the Case ID anywhere in the body
    body_text = soup.get_text()
    if "TR-2024-00143" in body_text:
        print("[+] SUCCESS: Case ID found in HTML.")
        # Attempt to find the specific table row
        for row in soup.find_all("tr"):
            if "TR-2024-00143" in row.get_text():
                print(f"[*] DATA ROW: {row.get_text(separator=' | ', strip=True)}")
    else:
        print("[!] FAILURE: Case ID not found in the response.")
        
        # 2. Check for common barriers
        if "Verification" in body_text or "Captcha" in body_text:
            print("[!] BARRIER: Site requested a CAPTCHA/Verification Word.")
        elif "Session" in body_text:
            print("[!] BARRIER: Session timeout or invalid Viewstate.")
        else:
            print("[*] SERVER RESPONSE PREVIEW (First 500 chars):")
            print(body_text.strip()[:500])
