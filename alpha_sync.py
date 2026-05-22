import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from datetime import datetime

ALPHA_URL = "https://portal.mobileso.com/mcso/jail/jp_ci_c.asp"

def run_sync():
    print(f"[{datetime.now()}] Initiating Alpha Roster Interception...")
    try:
        r = requests.get(ALPHA_URL, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.find_all('tr')
        
        conn = sqlite3.connect('audit_integrity.db')
        cursor = conn.cursor()
        
        found_count = 0
        for row in rows:
            text = " ".join(row.get_text().split())
            # Searching for yesterday's bookings (May 8)
            if "05/08/2026" in text:
                try:
                    parts = text.split()
                    date_idx = parts.index("05/08/2026")
                    b_id = parts[0]
                    name = " ".join(parts[1:date_idx])
                    # Reformat date for SQLite compatibility
                    raw_time = parts[date_idx + 1]
                    ts = f"2026-05-08 {raw_time}"
                    
                    cursor.execute("INSERT OR REPLACE INTO mcso_bookings VALUES (?, ?, ?)", (b_id, name, ts))
                    found_count += 1
                except: continue
        
        conn.commit()
        conn.close()
        print(f"Sync Complete. {found_count} records injected.")
    except Exception as e:
        print(f"Bypass Failed: {e}")

if __name__ == "__main__":
    run_sync()
