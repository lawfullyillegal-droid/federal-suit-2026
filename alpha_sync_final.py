import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from datetime import datetime

# THE LIVE SOURCE
URL = "https://portal.mobileso.com/mcso/jail/jp_ci_c.asp"
DB_PATH = "audit_integrity.db"


def init_db(cursor):
    """Create the bookings table if it does not exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mcso_bookings (
            booking_id TEXT PRIMARY KEY,
            name TEXT,
            timestamp TEXT
        )
    """)


def run_audit():
    today = datetime.now().strftime("%m/%d/%Y")
    print(f"[{datetime.now()}] Intercepting Alpha Roster for {today}...")
    try:
        r = requests.get(URL, timeout=15)
        r.raise_for_status()
        raw_text = r.text

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        init_db(cursor)

        # Regex: Name, ID, today's date (MM/DD/YYYY), and time HH:MM
        # Example: ADKINS, DILLON 12345 06/04/2026 10:32
        date_pattern = re.escape(today)
        pattern = re.compile(
            r'([A-Z][A-Z, ]+?)\s+(\d{4,})\s+(' + date_pattern + r')\s+(\d{2}:\d{2})'
        )

        matches = pattern.findall(raw_text)
        synced = 0
        for name, b_id, date, time_str in matches:
            timestamp = f"{datetime.now().strftime('%Y-%m-%d')} {time_str}"
            cursor.execute(
                "INSERT OR REPLACE INTO mcso_bookings VALUES (?, ?, ?)",
                (b_id, name.strip(), timestamp)
            )
            synced += 1

        conn.commit()
        conn.close()
        print(f"Audit Integrity: {synced} records synced for {today}.")

    except requests.RequestException as e:
        print(f"Network error during audit: {e}")
    except sqlite3.Error as e:
        print(f"Database error during audit: {e}")
    except Exception as e:
        print(f"Shadow Audit Failed: {e}")


if __name__ == "__main__":
    run_audit()
