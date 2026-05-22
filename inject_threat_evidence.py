import sqlite3

def inject_forensic_records():
    print("[*] Parsing and injecting raw screenshot evidence into forensics ledger...")
    conn = sqlite3.connect('audit_integrity.db')
    cursor = conn.cursor()
    
    evidence_payload = [
        ("EVID-001", "2026-04-10 11:27:00", "(562) 535-0725", "Bailey Cowins", 
         "You r a BITCH. my brother lives off of shinarump and Estella... Ima need the gun back or shoot it to Mike", 
         "Shinarump Dr & Estella Ln, Golden Valley", 1, "A.R.S. 13-2804 / 13-2809"),
         
        ("EVID-002", "2026-05-18 02:00:00", "Via Intermediary", "Julie Brown", 
         "Travis is gonna end up really fucked up over this he better hope we don't catch him together", 
         "Kingman/Golden Valley Sector", 0, "A.R.S. 13-1202 - Criminal Threat")
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO forensic_threat_ledger 
        (evidence_id, timestamp_captured, source_phone, interlocutor_name, verbatim_text, geographic_anchor_cross, weapon_reference_flag, statutory_violations)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, evidence_payload)
    
    conn.commit()
    conn.close()
    print("[+] Evidence profiles fully locked into integrity database.")

if __name__ == "__main__":
    inject_forensic_records()
