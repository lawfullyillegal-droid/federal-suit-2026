import sqlite3

def map_cowins_network():
    print("[*] Initializing Cowins Network Tracking & Bail Disparity Matrix...")
    conn = sqlite3.connect('audit_integrity.db')
    cursor = conn.cursor()
    
    # 1. Inject the Cowins Administrative Nodes
    cowins_staff = [
        ("EMP-020", "Charles Cowins", "Judicial Bail Magistrate", "2010-04-05", "Board of Supervisors", "86401", 1, None),
        ("EMP-021", "Marcus Cowins", "Intake Booking Sergeant", "2018-09-12", "Sheriff Office Node", "86401", 2, None)
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO public_personnel 
        (employee_id, employee_name, department_node, hire_date, hired_by_authority, assigned_zip, generation_depth, family_anchor_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, cowins_staff)
    
    # 2. Inject the Private Bail Entity Node
    bail_agencies = [
        ("BOND-001", "Cowins Liberty Bail Bonds LLC", "Sarah Cowins-Crowley", "Charles Cowins"),
        ("BOND-002", "Tri-State Express Bonds", "John Doe", "None")
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO bail_bond_agencies 
        (agency_id, agency_name, registered_agent, family_affiliation_node)
        VALUES (?, ?, ?, ?)
    """, bail_agencies)
    
    # 3. Inject Case Profiles to measure disparity metrics
    # Case 1: Processed by a Cowins node, secured by Cowins Bail Bonds
    # Case 2: Standard control case processed by a standalone node
    case_profiles = [
        ("MOH-2026-00910", "Inmate Alpha", 75000.00, "EMP-021", "BOND-001"),
        ("MOH-2026-00911", "Inmate Beta", 15000.00, "EMP-011", "BOND-002")
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO bail_disparity_ledger 
        (case_id, inmate_name, assigned_bail_amount, processing_officer_id, securing_agency_id)
        VALUES (?, ?, ?, ?, ?)
    """, case_profiles)
    
    conn.commit()
    conn.close()
    print("[+] Cowins structural matrix and bond metrics successfully integrated.")

if __name__ == "__main__":
    map_cowins_network()
