#!/bin/bash
INTERVAL=14400 # 4 hours in seconds

echo "[*] Initializing automated background audit node..."
echo "[*] Cycle interval locked at $INTERVAL seconds."

while true; do
    echo "[*] Starting automated synchronization cycle: $(date)"
    
    # 1. Execute the python ingestion script
    python process_intake.py
    
    # 2. Query the updated database to dynamically maintain the evidence spreadsheet
    sqlite3 audit_integrity.db << 'SQL'
.headers on
.mode csv
.output rule_4_1_emergency_escalation.csv
SELECT 
    p.inmate_name, 
    p.case_id, 
    p.arrest_timestamp, 
    c.public_defender_assigned,
    ROUND((strftime('%s', c.assignment_timestamp) - strftime('%s', p.arrest_timestamp)) / 3600.0, 1) as hours_denied_counsel
FROM court_proceedings p
JOIN counsel_appointments c ON p.case_id = c.case_id
WHERE hours_denied_counsel > 72.0;
SQL

    # 3. Synchronize manifest records 
    cat << 'MANIFEST' > source_record_manifest.json
{
    "status": "active",
    "jurisdiction": "MOHAVE",
    "last_audit_sync": "$(date +%Y-%m-%d)",
    "monitored_metrics": [
        "rule_4.1_timelines",
        "6th_amendment_counsel_lag",
        "bail_variance_disparities"
    ],
    "pipeline_status": "daemon_loop_active",
    "legal_footprint": "ARS_12-821.01_staged"
}
MANIFEST

    # 4. Push the freshly isolated evidence metrics straight to the remote mainframe
    git add auto_scheduler.sh rule_4_1_emergency_escalation.csv source_record_manifest.json
    git commit -m "Automated Daemon Sync: Updating live accountability logs [$(date +%Y-%m-%d_%H:%M:%S)]"
    git push origin main
    
    echo "[+] Cycle complete. Entering sleep cycle for $INTERVAL seconds..."
    sleep $INTERVAL
done
