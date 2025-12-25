import sqlite3
from datetime import datetime
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# DB_PATH = os.path.join("data", "tickets.db")
DB_PATH = BASE_DIR / "data" / "tickets.db"

def save_ticket(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tickets(
                   ticket_id, complaint_text, predicted_category,
         confidence, routed_to, status, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["ticket_id"],
        data["complaint_text"],
        data["predicted_category"],
        data["confidence"],
        data["routed_to"],
        data["status"],
        datetime.now()
    ))

    conn.commit()
    conn.close()
