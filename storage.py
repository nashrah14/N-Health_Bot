import csv, os
from datetime import datetime

FILE = "appointments.csv"

def init_appointments():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time","name","age","phone","problem","date","department"])

def save_appointment(p):
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(),
            p["name"], p["age"], p["phone"],
            p["problem"], p["date"], p["department"]
        ])