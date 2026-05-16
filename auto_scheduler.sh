#!/bin/bash
INTERVAL=14400 # 4 hours in seconds

echo "[*] Initializing automated background audit node..."
echo "[*] Cycle interval locked at $INTERVAL seconds."

while true; do
    echo "[*] Starting automated synchronization cycle: $(date)"
    
    # Execute the data intake engine
    python process_intake.py
    
    # Check the database for active violations to generate the tracking matrix
    sqlite3 audit_integrity.db << 'SQL'
.headers on
.mode csv
.output rule_4_1_emergency_escalation.csv
SELECT p.inmate_name, p.case_id, p.arrest_timestamp, c.public_defender_assigned,
       ROUND((strftime('%s', c.assignment_timestamp) - strftime('%s', p.arrest_timestamp)) / 3600.0, 1) as hours_denied_counsel
FROM court_proceedings p
JOIN counsel_appointments c ON p.case_id = c.case_id
WHERE hours_denied_counsel > 72.0;
SQL

    # Push to GitHub using your saved token credentials
    echo "[*] Staging files to repository main branch..."
    ./push_manifest.sh
    
    echo "[+] Cycle complete. Entering sleep cycle..."
    sleep $INTERVAL
done
