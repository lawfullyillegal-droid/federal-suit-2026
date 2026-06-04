import sqlite3
import json
from datetime import datetime, timedelta

def run_intake_audit():
    conn = sqlite3.connect('audit_integrity.db')
    cursor = conn.cursor()
    
    print("[*] Processing Mohave County Jail data stream...")
    
    # SYSTEM CHECK: Simulating a 73-hour processing lag violation
    test_cases = [
        {
            "case_id": "MOH-2026-00891",
            "inmate_name": "John Doe",
            "arrest_timestamp": (datetime.now() - timedelta(hours=73)).strftime('%Y-%m-%d %H:%M:%S'),
            "initial_appearance_timestamp": None, # Missing = Rule 4.1 Violation
            "formal_charges": "RESTRUCTURING ASSAULT TIER 2",
            "public_defender_assigned": "UNASSIGNED",
            "assignment_timestamp": (datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
            "charge_severity": "Felony",
            "assessed_amount": 15000.00
        }
    ]
    
    for case in test_cases:
        try:
            # 1. Ingest Main Proceedings
            cursor.execute("""
                INSERT OR REPLACE INTO court_proceedings 
                (case_id, inmate_name, jurisdiction, arrest_timestamp, initial_appearance_timestamp, formal_charges)
                VALUES (?, ?, 'MOHAVE', ?, ?, ?)
            """, (case["case_id"], case["inmate_name"], case["arrest_timestamp"], case["initial_appearance_timestamp"], case["formal_charges"]))
            
            # 2. Ingest Counsel Appointment Lag (FIXED BINDINGS)
            cursor.execute("""
                INSERT OR REPLACE INTO counsel_appointments 
                (case_id, public_defender_assigned, assignment_timestamp, hours_to_counsel_assigned)
                VALUES (?, ?, ?, ?)
            """, (case["case_id"], case["public_defender_assigned"], case["assignment_timestamp"], 73.0))
            
            # 3. Ingest Bail Variance Data (FIXED BINDINGS)
            cursor.execute("""
                INSERT OR REPLACE INTO bail_schedules 
                (case_id, charge_severity, assessed_amount, demographic_marker)
                VALUES (?, ?, ?, 'MOHCO_BASE')
            """, (case["case_id"], case["charge_severity"], case["assessed_amount"]))
            
            print(f"[+] Case {case['case_id']} successfully processed into audit database.")
        except Exception as e:
            print(f"[-] Processing error on case {case['case_id']}: {str(e)}")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_intake_audit()
