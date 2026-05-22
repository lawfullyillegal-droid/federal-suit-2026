import sqlite3

def map_infrastructure_node():
    print("[*] Registering Infrastructure Security Node for Target: Rt Cowins...")
    conn = sqlite3.connect('audit_integrity.db')
    cursor = conn.cursor()
    
    # 1. Inject Rt Cowins into the personnel directory
    rt_profile = [
        ("EMP-022", "Rt Cowins", "Facilities Logistics & Security Specialist", "2015-07-19", "Board of Supervisors", "86413", 2, "ANC-003")
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO public_personnel 
        (employee_id, employee_name, department_node, hire_date, hired_by_authority, assigned_zip, generation_depth, family_anchor_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, rt_profile)
    
    # 2. Assign his node to the physical perimeter security zones
    facility_assets = [
        ("FAC-ZONE-04", "Mohave Detention Center - Kingman", "AdSeg Perimeter & Transport Lock", "EMP-022")
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO facility_control_ledger 
        (asset_id, facility_name, secure_zone_access, assigned_staff_id)
        VALUES (?, ?, ?, ?)
    """, facility_assets)
    
    conn.commit()
    conn.close()
    print("[+] Infrastructure control mapping for Rt Cowins integrated cleanly.")

if __name__ == "__main__":
    map_infrastructure_node()
