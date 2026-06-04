import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from datetime import datetime

URL = "https://www.mohave.gov/departments/sheriff/jail/inmate-search/"

def normalize_name(name):
    clean = re.sub(r'[^a-zA-Z\s]', '', name).lower()
    return " ".join(sorted(clean.split()))

def run_mcso_audit():
    # ESSENTIAL: Mimic a real browser to avoid the NoneType error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        response = session.get(URL, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if we are being blocked
        vs_tag = soup.find('input', {'id': '__VIEWSTATE'})
        if not vs_tag:
            print("FAILED: ViewState not found. The site may be blocking the connection.")
            return

        payload = {
            '__VIEWSTATE': vs_tag['value'],
            '__EVENTVALIDATION': soup.find('input', {'id': '__EVENTVALIDATION'})['value'],
            'btnSearch': 'Search',
            'txtLastName': ''
        }
        
        results = session.post(URL, data=payload)
        results_soup = BeautifulSoup(results.text, 'html.parser')
        table = results_soup.find('table', {'id': 'gvInmateList'})
        
        if not table:
            print("FAILED: Booking table not found. Verify the ID 'gvInmateList'.")
            return

        conn = sqlite3.connect('audit_integrity.db')
        cursor = conn.cursor()

        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) < 2: continue
            
            b_id = cols[0].text.strip()
            name = normalize_name(cols[1].text.strip())
            
            cursor.execute('''INSERT OR REPLACE INTO mcso_bookings 
                            (booking_id, inmate_name, booking_timestamp) 
                            VALUES (?, ?, ?)''', 
                            (b_id, name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        conn.commit()
        conn.close()
        print("Audit: Data successfully injected into audit_integrity.db")

    except Exception as e:
        print(f"System Error: {e}")

if __name__ == "__main__":
    run_mcso_audit()
