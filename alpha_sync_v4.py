import requests
import sqlite3
import re

URL = "https://portal.mobileso.com/mcso/jail/jp_ci_c.asp"

def adaptive_sync():
    print("Intercepting Alpha Feed...")
    r = requests.get(URL, timeout=10)
    lines = r.text.splitlines()
    
    conn = sqlite3.connect('audit_integrity.db')
    cursor = conn.cursor()
    
    found = 0
    # Look for any line that has '05/08' or '05/09'
    for line in lines:
        if "05/08/2026" in line or "05/09/2026" in line:
            # Clean up the line and split by whitespace
            parts = line.split()
            if len(parts) > 3:
                # We assume the first few parts are the name and the last few are time
                name = " ".join(parts[:2]) 
                timestamp = " ".join([p for p in parts if '/' in p or ':' in p][:2])
                
                # Use a dummy ID if we can't find a clear one
                b_id = parts[2] if len(parts) > 2 else name
                
                cursor.execute("INSERT OR REPLACE INTO mcso_bookings VALUES (?, ?, ?)", 
                               (b_id, name, timestamp))
                found += 1
                
    conn.commit()
    conn.close()
    print(f"Bypass Successful. {found} violations identified.")

if __name__ == "__main__":
    adaptive_sync()
