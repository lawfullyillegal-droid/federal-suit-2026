import requests
import json
from datetime import datetime

# HARD-CODED TARGET ACQUIRED FROM SCAN
TARGET_IP = "192.168.1.54" 
NODE_ID = "031332"
OUT_FILE = "live_audit_031332.json"

def capture_metadata():
    print(f"[*] ATTENTION: Executing live capture on {TARGET_IP}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    endpoints = {
        "device_identity": f"http://{TARGET_IP}/web/guest/en/device/deviceinfo.cgi",
        "job_history": f"http://{TARGET_IP}/web/guest/en/job/history.cgi"
    }
    captured = {}
    for key, url in endpoints.items():
        try:
            print(f"[*] Querying {key}...")
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                captured[key] = r.text
                print(f"[+] Success: {len(r.text)} bytes captured.")
            else:
                captured[key] = f"STATUS_{r.status_code}"
                print(f"[-] Access Denied: {r.status_code}")
        except Exception as e:
            captured[key] = f"FAILED: {str(e)}"
            print(f"[!] Connection error on {key}")
    
    with open(OUT_FILE, "w") as f:
        json.dump(captured, f, indent=4)
    print(f"\n[!] FORENSIC DATA STORED IN {OUT_FILE}")

if __name__ == "__main__":
    capture_metadata()
