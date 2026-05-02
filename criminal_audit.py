import sqlite3
from datetime import datetime

def audit_bond_bias(case):
    # Standardizing 8th Amendment Check
    if case['bond'] > 5000 and case['charge_class'] == 3:
        print(f"[!] 8th AMENDMENT ALERT: Case {case['id']} | Bond: ${case['bond']} for Class 3")

def audit_counsel_lag(booking_date, appointment_date, case_id):
    # 6th Amendment Appointment Lag Check
    fmt = "%Y-%m-%d %H:%M"
    d1 = datetime.strptime(booking_date, fmt)
    d2 = datetime.strptime(appointment_date, fmt)
    diff = (d2 - d1).days
    
    if diff > 2:
        print(f"[!!!] 6th AMENDMENT LAG: Case {case_id} | {diff} days without counsel while detained.")

# Batch Simulation for David Jay Wayt's Criminal Docket
wayt_cases = [
    {'id': 'J-0805-CR-2026012', 'bond': 7500, 'charge_class': 3},
    {'id': 'J-0805-CR-2026022', 'bond': 10000, 'charge_class': 3}
]

print("--- CERBAT PRECINCT 5 CRIMINAL AUDIT ---")
for case in wayt_cases:
    audit_bond_bias(case)

# Testing Lag: Booked May 1st, Counsel not assigned until May 5th
audit_counsel_lag("2026-05-01 08:00", "2026-05-05 14:00", "J-0805-CR-2026012")
