import os
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime


DEFAULT_URL = "https://www.mohave.gov/departments/sheriff/press-releases/"


def run_audit(url=None):
    """Run the audit against `url`.

    Priority: explicit `url` argument -> `MOHAVE_URL` env var -> `DEFAULT_URL`.
    """
    URL = url or os.environ.get('MOHAVE_URL') or DEFAULT_URL
    try:
        r = requests.get(URL, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        tds = soup.find_all('td', align="center")

        conn = sqlite3.connect('audit_integrity.db')
        cursor = conn.cursor()

        current_live_names = []
        found = 0
        
        for i, td in enumerate(tds):
            text = td.get_text().strip()
            if "/2026" in text and ":" in text:
                name = tds[i-1].get_text().strip() if i > 0 else "UNKNOWN"
                current_live_names.append(name)
                
                # Format: MM/DD/YYYY HH:MM:SS -> YYYY-MM-DD HH:MM:SS
                m, d, remaining = text.split('/')
                y, time = remaining.split(' ')
                iso_ts = f"{y}-{m.zfill(2)}-{d.zfill(2)} {time}"

                cursor.execute("""
                    INSERT INTO mcso_bookings (inmate_name, booking_timestamp) 
                    VALUES (?, ?)
                """, (name, iso_ts))
                found += 1

        # Reconciliation: If they aren't on the site, they were released
        if current_live_names:
            placeholders = ','.join(['?'] * len(current_live_names))
            cursor.execute(f"""
                UPDATE mcso_bookings 
                SET release_timestamp = datetime('now') 
                WHERE release_timestamp IS NULL 
                AND inmate_name NOT IN ({placeholders})
            """, current_live_names)

        conn.commit()
        conn.close()
        print(f"Audit Integrity: {found} records synced. State reconciliation complete.")
        return {'synced': found, 'current_live_names': current_live_names}

    except Exception as e:
        print(f"Audit Failure: {e}")
        return {'error': str(e)}

if __name__ == "__main__":
    run_audit()
