import requests
import sqlite3
import re
from datetime import datetime

URL = "https://portal.mobileso.com/mcso/jail/jp_ci_c.asp"

def wide_net_sync():
    print(f"[{datetime.now()}] Initiating Wide-Net Extraction...")
    try:
        r = requests.get(URL, timeout=10)
        lines = r.text.splitlines()
        
        conn = sqlite3.connect('audit_integrity.db')
        cursor = conn.cursor()
        
        found = 0
        # This regex looks for ANY date-like pattern (MM/DD/YY or MM/DD/YYYY)
        date_pattern = re.compile(r'\d{1,2}/\d{1,2}/\d{2,4}')
        
        for line in lines:
            if date_pattern.search(line):
                parts = line.split()
                if len(parts) > 4:
                    # Capture everything to find the Name and Date
                    b_id = parts[0]
                    # Attempt to isolate name (usually capital letters)
                    name = " ".join([p for p in parts if p.isupper() and ',' in p or p.isalpha()][:2])
                    
                    # Find the date and time strings
                    date_matches = [p for p in parts if '/' in p]
                    time_matches = [p for p in parts if ':' in p]
                    
                    if date_matches and time_matches:
                        # Normalize date to YYYY-MM-DD for SQLite
                        d = date_matches[0]
                        if len(d.split('/')[-1]) == 2: d = d[:-2] + "20" + d[-2:]
                        
                        # Reformat to ISO for the Rule 4.1 calculation
                        m, day, y = d.split('/')
                        iso_ts = f"{y}-{m.zfill(2)}-{day.zfill(2)} {time_matches[0]}"
                        
                        cursor.execute("INSERT OR REPLACE INTO mcso_bookings VALUES (?, ?, ?)", 
                                       (b_id, name, iso_ts))
                        found += 1
        
        conn.commit()
        conn.close()
        print(f"Wide-Net Success: {found} records captured for analysis.")
    except Exception as e:
        print(f"Extraction Error: {e}")

if __name__ == "__main__":
    wide_net_sync()
