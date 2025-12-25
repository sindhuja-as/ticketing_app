import sqlite3
from datetime import datetime

def generate_ticket_id(conn):
    today = datetime.now().strftime("%y-%m-%d")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT last_number FROM ticket_counter WHERE date = ?",
        (today,)
    )
    row = cursor.fetchone()

    if row:
        counter = row[0] + 1
        cursor.execute(
            "UPDATE ticket_counter SET last_number = ? WHERE date = ?",
            (counter, today)
        )
    else:
        counter = 1
        cursor.execute(
            "INSERT INTO ticket_counter (date, last_number) VALUES (?, ?)",
            (today, counter)
        )

    conn.commit()
    return f"TCK-{today.replace('-', '')}-{counter:04d}"
