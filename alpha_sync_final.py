import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from datetime import datetime

# THE LIVE SOURCE
URL = "https://portal.mobileso.com/mcso/jail/jp_ci_c.asp"

def run_audit():
    print(f"[{datetime.now()}] Intercepting Alpha Roster...")
    try:
        r = requests.get(URL, timeout=15)
        # We search the raw text because the portal uses <pre> blocks
        raw_text = r.text
        
        conn = sqlite3.connect('audit_integrity.db')
        cursor = conn.cursor()
        
        # Regex to find: Name, ID, and the Friday (05/08) Booking Date
        # Example pattern: ADKINS, DILLON 12345 05/08/2026 10:32
        pattern = re.compile(r'([A-Z, ]+)\s+(\d+)\s+(05/08/2026)\s+(\d{2}:\d{2})')
        
        matches = pattern.findall(raw_text)
        for name, b_id, date, time in matches:
            timestamp = f"2026-05-08 {time}"
            cursor.execute("INSERT OR REPLACE INTO mcso_bookings VALUES (?, ?, ?)", 
                           (b_id, name.strip(), timestamp))
        
        conn.commit()
        conn.close()
        print(f"Audit Integrity: {len(matches)} records synced.")
        
    except Exception as e:
        print(f"Shadow Audit Failed: {e}")

if __name__ == "__main__":
    run_audit()
