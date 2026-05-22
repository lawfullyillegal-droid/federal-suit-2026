import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

URL = "https://portal.mobileso.com/mcso/jail/jp_ci_c.asp"

def run_audit():
    print(f"[{datetime.now()}] Extracting Judicial Evidence...")
    try:
        r = requests.get(URL, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # In this portal, the name is usually in the <td> immediately preceding the date
        tds = soup.find_all('td', align="center")
        
        conn = sqlite3.connect('audit_integrity.db')
        cursor = conn.cursor()
        
        found = 0
        for i, td in enumerate(tds):
            text = td.get_text().strip()
            # If the cell looks like a 2026 booking date
            if "/2026" in text:
                # Try to grab the name from the column before it
                name = tds[i-1].get_text().strip() if i > 0 else "UNKNOWN"
                
                # Convert 05/08/2026 10:32:41 to SQLite format 2026-05-08 10:32:41
                m, d, y_time = text.split('/')
                y, time = y_time.split(' ')
                iso_ts = f"{y}-{m.zfill(2)}-{d.zfill(2)} {time}"
                
                cursor.execute("INSERT OR REPLACE INTO mcso_bookings (booking_id, inmate_name, booking_timestamp) VALUES (?, ?, ?)", 
                               (f"B{i}", name, iso_ts))
                found += 1
        
        conn.commit()
        conn.close()
        print(f"Audit Integrity: {found} records captured.")
        
    except Exception as e:
        print(f"Audit Failure: {e}")

if __name__ == "__main__":
    run_audit()
