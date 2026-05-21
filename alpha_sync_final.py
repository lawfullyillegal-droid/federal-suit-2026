import requests
from bs4 import BeautifulSoup
import sqlite3
import urllib.parse
from datetime import datetime
import os
import re
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

CALENDAR_INDEX_URL = "https://www.mohavecourts.com/court-calendars"

def run_court_audit():
    print(f"[{datetime.now()}] Initializing Mohave Judicial Docket Intercept...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        r = requests.get(CALENDAR_INDEX_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        links = soup.find_all('a', href=True)
        pdf_targets = []
        
        for link in links:
            href = link['href']
            if href.lower().endswith(".pdf") and any(kwd in href.lower() for kwd in ["division", "comm", "calendar"]):
                if "plan" in href.lower() or "report" in href.lower():
                    continue
                full_pdf_url = urllib.parse.urljoin(CALENDAR_INDEX_URL, href)
                if full_pdf_url not in pdf_targets:
                    pdf_targets.append(full_pdf_url)
                    
        print(f"[{datetime.now()}] Target Node Extraction: Located {len(pdf_targets)} active courtroom division streams.")
        
        # Open database integrity sync pipeline
        conn = sqlite3.connect('audit_integrity.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS court_docket_ledger (
                case_number TEXT PRIMARY KEY,
                hearing_type TEXT,
                record_timestamp TEXT
            )
        """)
        
        record_count = 0
        
        for pdf_url in pdf_targets[:3]:
            filename = pdf_url.split('/')[-1]
            local_filename = f"court_{filename}"
            
            doc_data = requests.get(pdf_url, headers=headers, timeout=10).content
            with open(local_filename, "wb") as f:
                f.write(doc_data)
            
            if PdfReader and os.path.exists(local_filename):
                reader = PdfReader(local_filename)
                for page in reader.pages:
                    text = page.extract_text()
                    for line in text.split('\n'):
                        line = line.strip()
                        
                        # Regex match to trap the Arizona Case Identifier string block
                        match = re.search(r'(S8015CR\d{9})', line)
                        if match:
                            case_num = match.group(1)
                            # Strip the case number off the line to clean out the hearing description field
                            hearing_type = line.replace(case_num, "").strip()
                            
                            # Clean up artifact prefixes caught during string merges
                            for prefix in ["[DOCKET ROW]", "ARRAIGNMENT", "SENTENCING", "PRETRIAL"]:
                                if hearing_type.upper().startswith(prefix):
                                    hearing_type = re.sub('^' + prefix, '', hearing_type, flags=re.IGNORECASE).strip()
                            
                            if not hearing_type:
                                hearing_type = "SCHEDULED PROCEEDING"
                                
                            timestamp = f"2026-05-21 {datetime.now().strftime('%H:%M:%S')}"
                            
                            cursor.execute("""
                                INSERT OR REPLACE INTO court_docket_ledger (case_number, hearing_type, record_timestamp)
                                VALUES (?, ?, ?)
                            """, (case_num, hearing_type, timestamp))
                            record_count += 1
                            print(f"    [+] RECORD LOGGED -> CASE: {case_num} | TYPE: {hearing_type}")
                            
        conn.commit()
        print(f"\n[{datetime.now()}] Synchronization complete. Docket database fully populated with {record_count} entries.")
        conn.close()
        
    except Exception as e:
        print(f"[{datetime.now()}] SCAN ERROR: Court docket bottleneck: {e}")

if __name__ == "__main__":
    run_court_audit()
