import csv
from datetime import datetime
import os

FILE = "appointments.csv"

def init_appointments():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "appointment_id", "time",
                "name", "age", "phone",
                "problem", "date", "department"
            ])

def save_appointment(data, appointment_id):
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            appointment_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data["name"], data["age"], data["phone"],
            data["problem"], data["date"], data["department"]
        ])
