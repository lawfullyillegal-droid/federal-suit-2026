import requests
import json
from datetime import datetime

# HARD-CODED TARGET (ENSURE THIS MATCHES YOUR DISCOVERED IP)
TARGET_IP = "192.168.1.XX" 
NODE_ID = "031332"
OUT_FILE = "post_notice_audit_031332.json"

def capture_metadata():
    print(f"[*] STARTING POST-NOTICE AUDIT: Node {NODE_ID}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    endpoints = {
        "device_identity": f"http://{TARGET_IP}/web/guest/en/device/deviceinfo.cgi",
        "job_history": f"http://{TARGET_IP}/web/guest/en/job/history.cgi"
    }
    captured = {}
    for key, url in endpoints.items():
        try:
            print(f"[*] Probing {key} for changes...")
            r = requests.get(url, headers=headers, timeout=10)
            captured[key] = r.text if r.status_code == 200 else f"HTTP_STATUS_{r.status_code}"
        except Exception as e:
            captured[key] = f"OFFLINE_OR_FILTERED: {str(e)}"
    
    audit_data = {
        "audit_type": "POST_NOTICE",
        "timestamp": datetime.now().isoformat(),
        "node_id": NODE_ID,
        "results": captured
    }
    
    with open(OUT_FILE, "w") as f:
        json.dump(audit_data, f, indent=4)
    print(f"\n[!] POST-NOTICE SNAPSHOT SECURED: {OUT_FILE}")

if __name__ == "__main__":
    capture_metadata()
