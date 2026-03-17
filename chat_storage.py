import csv, os
from datetime import datetime

FILE = "chat_history.csv"

def init_chat():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            csv.writer(f).writerow(["time","role","msg"])

def save_chat(role, msg):
    with open(FILE, "a", newline="") as f:
        csv.writer(f).writerow([datetime.now(), role, msg])