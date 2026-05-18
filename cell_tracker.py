import subprocess
import json
import sqlite3
from datetime import datetime

DB_FILE = "telemetry.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Establish a table optimized for logging physical radio frequency nodes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tower_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            type TEXT,
            cell_id INTEGER,
            lac_tac INTEGER,
            signal_strength INTEGER,
            is_registered INTEGER
        )
    ''')
    conn.commit()
    return conn

def capture_cell_data():
    try:
        # Call the native Termux binary to query the device's wireless baseband
        result = subprocess.run(['termux-telephony-cellinfo'], capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"[-] Execution error querying telephony framework: {e}")
    return None

def log_telemetry(conn, cell_data):
    if not cell_data or not isinstance(cell_data, list):
        print("[!] No active hardware cell details returned. Check Termux:API permissions.")
        return

    cursor = conn.cursor()
    new_entries = 0
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for cell in cell_data:
        # Extract radio type (LTE, GSM, WCDMA, etc.)
        radio_type = cell.get('type', 'Unknown')
        is_registered = 1 if cell.get('registered') else 0
        
        # Parse standard network identification parameters safely across varying API schemas
        cell_id = cell.get('id') or cell.get('cid') or -1
        lac_tac = cell.get('lac') or cell.get('tac') or -1
        
        # Pull dBm signal metrics
        signal = cell.get('rssi') or cell.get('dbm') or 0

        # Prevent duplicate logging of the same tower state inside the same sample block
        cursor.execute('''
            INSERT INTO tower_logs (timestamp, type, cell_id, lac_tac, signal_strength, is_registered)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, radio_type, cell_id, lac_tac, signal, is_registered))
        new_rows = cursor.rowcount
        new_entries += new_rows

    conn.commit()
    print(f"[+] Operational Telemetry Logged. Indexed {new_entries} active infrastructure points.")

def main():
    conn = init_db()
    cell_data = capture_cell_data()
    log_telemetry(conn, cell_data)
    conn.close()

if __name__ == "__main__":
    main()
