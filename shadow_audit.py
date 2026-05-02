import sqlite3
import datetime

class ShadowAuditor:
    def __init__(self, db_name='audit_integrity.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._setup_db()

    def _setup_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS dockets 
            (case_id INTEGER PRIMARY KEY, timestamp TEXT, status TEXT)''')
        self.conn.commit()

    def scan_gaps(self, start_id, end_id):
        """Detects missing case numbers in a sequence."""
        self.cursor.execute("SELECT case_id FROM dockets WHERE case_id BETWEEN ? AND ?", (start_id, end_id))
        existing_ids = {row[0] for row in self.cursor.fetchall()}
        
        gaps = [i for i in range(start_id, end_id + 1) if i not in existing_ids]
        
        print(f"--- GAP ANALYSIS REPORT [{datetime.datetime.now()}] ---")
        if gaps:
            print(f"[!] ALERT: {len(gaps)} missing records detected in sequence.")
            print(f"[*] Missing IDs: {gaps[:10]} ...") # Shows first 10
        else:
            print("[+] Integrity Check: No sequence gaps found.")

# Initialize and Test
auditor = ShadowAuditor()
# Dummy data for demonstration: we have 101, 102, 105. 103 and 104 are 'ghosts'.
auditor.cursor.execute("INSERT OR IGNORE INTO dockets VALUES (101, '2026-05-01', 'OPEN')")
auditor.cursor.execute("INSERT OR IGNORE INTO dockets VALUES (102, '2026-05-01', 'CLOSED')")
auditor.cursor.execute("INSERT OR IGNORE INTO dockets VALUES (105, '2026-05-02', 'OPEN')")
auditor.conn.commit()

auditor.scan_gaps(101, 105)
