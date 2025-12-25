import sqlite3
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# DB_PATH = os.path.join("data", "tickets.db")
DB_PATH = BASE_DIR \\ "data" \\ "tickets.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id TEXT PRIMARY KEY,
    complaint_text TEXT,
    predicted_category TEXT,
    routed_to TEXT,
    confidence REAL,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Helper table for daily counter
cursor.execute("""
CREATE TABLE IF NOT EXISTS ticket_counter (
    date TEXT PRIMARY KEY,
    last_number INTEGER
)
""")


conn.commit()
conn.close()

print("Tables created successfully")
