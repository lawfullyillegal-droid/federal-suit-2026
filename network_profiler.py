import sqlite3
import pandas as pd

def run_network_profiling():
    print("[*] Launching Advanced Personnel Network Profiler...")
    
    conn = sqlite3.connect('audit_integrity.db')
    cursor = conn.cursor()
    
    # Live Data Injection representing the open county roster records
    sample_roster = [
        ("EMP-010", "Michael Smith", "Detention Admin", "2021-03-12", "Sheriff Office Node", "86401"),
        ("EMP-011", "David Smith", "Intake Processing", "2023-06-19", "Michael Smith", "86401"), # Kinship Flag
        ("EMP-012", "Robert Johnson", "Court Operations", "2019-11-02", "Board of Supervisors", "86403"),
        ("EMP-013", "Maria Rodriguez", "Public Defender Node", "2024-01-15", "Admin Director", "86442"),
        ("EMP-014", "William Johnson", "Intake Guard", "2025-02-10", "Robert Johnson", "86403") # Kinship Flag
    ]
    
    # Ingesting open public personnel details
    cursor.executemany("""
        INSERT OR REPLACE INTO public_personnel 
        (employee_id, employee_name, department_node, hire_date, hired_by_authority, assigned_zip)
        VALUES (?, ?, ?, ?, ?, ?)
    """, sample_roster)
    
    # Process the workaround correlation array
    cursor.execute("SELECT employee_id, employee_name, hired_by_authority, department_node FROM public_personnel")
    rows = cursor.fetchall()
    
    for emp_id, name, supervisor, dept in rows:
        last_name = name.split()[-1]
        sup_last_name = supervisor.split()[-1]
        
        # Workaround Metric 1: Automated Kinship Probability Hook
        kinship = "STANDALONE ENTRY"
        anomaly_score = 0.0
        
        if last_name == sup_last_name:
            kinship = f"PROBABLE KINSHIP DIRECT LINK: {supervisor}"
            anomaly_score += 75.0 # High structural anomaly weight
            
        # Workaround Metric 2: Geographic Representation Index
        # Contractors vs local administrative workforce deviations
        if dept == "Intake Processing" or dept == "Detention Admin":
            anomaly_score += 15.5
            
        cursor.execute("""
            INSERT OR REPLACE INTO personnel_network_map 
            (employee_id, kinship_flag_label, statistical_anomaly_score)
            VALUES (?, ?, ?)
        """, (emp_id, kinship, anomaly_score))
        
    conn.commit()
    conn.close()
    print("[+] Structural analysis layer complete. Network map written to DB.")

if __name__ == "__main__":
    run_network_profiling()
