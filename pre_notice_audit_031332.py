import requests
import json
from datetime import datetime

# HARD-CODED TARGET FROM YOUR SCAN
TARGET_IP = "192.168.1.XX" 
NODE_ID = "031332"
OUT_FILE = "pre_notice_audit_031332.json"

def capture_metadata():
    print(f"[*] Extracting forensic data from Node {NODE_ID} at {TARGET_IP}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    endpoints = {
        "device_identity": f"http://{TARGET_IP}/web/guest/en/device/deviceinfo.cgi",
        "job_history": f"http://{TARGET_IP}/web/guest/en/job/history.cgi"
    }
    captured = {}
    for key, url in endpoints.items():
        try:
            print(f"[*] Querying {key}...")
            r = requests.get(url, headers=headers, timeout=7)
            captured[key] = r.text if r.status_code == 200 else f"Access Denied: {r.status_code}"
        except Exception as e:
            captured[key] = f"Connection Failed: {str(e)}"
    
    audit_data = {
        "timestamp": datetime.now().isoformat(),
        "node_id": NODE_ID,
        "ip": TARGET_IP,
        "results": captured
    }
    
    with open(OUT_FILE, "w") as f:
        json.dump(audit_data, f, indent=4)
    print(f"\n[!] SUCCESS: Forensic snapshot saved to {OUT_FILE}")

if __name__ == "__main__":
    capture_metadata()
