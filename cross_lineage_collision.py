import sqlite3

def run_collision_audit():
    print("[*] Running Cross-Lineage Collision Engine...")
    conn = sqlite3.connect('audit_integrity.db')
    cursor = conn.cursor()
    
    # Advanced query to find inmates intersecting multiple family lineages
    query = """
        SELECT 
            dl.case_id AS "Case ID",
            dl.inmate_name AS "Inmate",
            p1.employee_name AS "Booking Officer",
            p1.family_anchor_id AS "Booking Line",
            dl.assigned_bail_amount AS "Bail Amount ($)",
            ba.agency_name AS "Bonding Entity",
            ba.family_affiliation_node AS "Bonding Line"
        FROM bail_disparity_ledger dl
        JOIN public_personnel p1 ON dl.processing_officer_id = p1.employee_id
        JOIN bail_bond_agencies ba ON dl.securing_agency_id = ba.agency_id
        WHERE p1.family_anchor_id IS NOT NULL 
           OR ba.family_affiliation_node IS NOT NULL;
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print(f"{'Case ID':<16} | {'Inmate':<12} | {'Booking (Line)':<22} | {'Bail ($)':<10} | {'Bonding Entity (Line)':<25}")
    print("-" * 95)
    
    for row in rows:
        case_id, inmate, officer, o_line, bail, agency, a_line = row
        o_display = f"{officer} ({o_line})"
        a_display = f"{agency} ({a_line if a_line else 'None'})"
        print(f"{case_id:<16} | {inmate:<12} | {o_display:<22} | {bail:<10} | {a_display:<25}")
        
    conn.close()

if __name__ == "__main__":
    run_collision_audit()
