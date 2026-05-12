#!/bin/bash
echo "--- COMMENCING RULE 4.1(c) FORENSIC SCAN ---"

python3 -c "
import pandas as pd
import sys
try:
    df = pd.read_csv('rule_4_1_final_audit.csv')
    v = df[df['total_hours'] > 24].copy()
    v['damages'] = (v['total_hours'] - 24) * 250
    total = v['damages'].sum()
    sys.stdout.write(f'STATUS: BREACH CONFIRMED\n')
    sys.stdout.write(f'ENTITIES IN VIOLATION: {len(v)}\n')
    sys.stdout.write(f'AGGREGATED LIABILITY: ${total:,.2f}\n')
    sys.stdout.flush()
    v.to_csv('watchdog_latest_breach.csv', index=False)
except Exception as e:
    sys.stdout.write(f'SCAN ERROR: {e}\n')
"
echo "--- SCAN COMPLETE ---"
