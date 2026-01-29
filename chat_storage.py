import csv
from datetime import datetime
import os

FILE = "chat_history.csv"

def init_chat_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["session_id", "time", "role", "message"])

def save_message(session_id, role, message):
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            session_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            role,
            message
        ])
