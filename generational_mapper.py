import sqlite3

def build_generational_matrix():
    print("[*] Calculating Multi-Generational Institutional Footprint...")
    conn = sqlite3.connect('audit_integrity.db')
    cursor = conn.cursor()
    
    # 1. Establish the Legacy Roots (Generation 0 - The Anchors)
    legacy_roots = [
        ("ANC-001", "Arthur Smith Senior", 1996, "County Executive Charter"),
        ("ANC-002", "James Johnson Crowley", 1998, "Board of Supervisors Seat A")
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO generational_anchors 
        (anchor_id, anchor_name, original_appointment_year, root_political_node)
        VALUES (?, ?, ?, ?)
    """, legacy_roots)
    
    # 2. Update the active personnel directory with structural depth links
    # Mapping how Generation 1 (Michael) and Generation 2 (David) nest into the legacy line
    generational_updates = [
        ("EMP-010", 2, "ANC-001"), # Michael Smith (Gen 2 in the 30-year timeline)
        ("EMP-011", 3, "ANC-001"), # David Smith (Gen 3 - Active Intake)
        ("EMP-012", 2, "ANC-002"), # Robert Johnson (Gen 2 - Court Operations)
        ("EMP-014", 3, "ANC-002")  # William Johnson (Gen 3 - Intake Guard)
    ]
    
    for emp_id, depth, anchor in generational_updates:
        cursor.execute("""
            UPDATE public_personnel 
            SET generation_depth = ?, family_anchor_id = ? 
            WHERE employee_id = ?
        """, (depth, anchor, emp_id))
        
    conn.commit()
    conn.close()
    print("[+] Generational depth values integrated cleanly.")

if __name__ == "__main__":
    build_generational_matrix()
