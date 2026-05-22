import sqlite3
import csv

def export_master_audit():
    print("[*] Initiating final systemic audit aggregation...")
    conn = sqlite3.connect('audit_integrity.db')
    cursor = conn.cursor()
    
    # Extract the total correlated network profile
    query = """
        SELECT 
            p.employee_name AS "Official",
            p.department_node AS "Role",
            a.anchor_name AS "Lineage Root",
            COALESCE(i.subject_name, 'No Direct Hold') AS "Target Intersect",
            COALESCE(o.functional_role, 'No Direct Intermediary') AS "Intermediary Vector"
        FROM public_personnel p
        LEFT JOIN generational_anchors a ON p.family_anchor_id = a.anchor_id
        LEFT JOIN isolated_informant_ledger i ON p.employee_id = i.handling_authority_id
        LEFT JOIN operational_intermediaries o ON o.associated_family_line = a.anchor_name;
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    with open('master_systemic_audit_report.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Official', 'Role', 'Lineage Root', 'Target Intersect', 'Intermediary Vector'])
        writer.writerows(rows)
        
    conn.close()
    print("[+] Master systemic audit report compiled successfully: master_systemic_audit_report.csv")

if __name__ == "__main__":
    export_master_audit()
