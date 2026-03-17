FIELDS = ["name", "age", "phone", "date"]

QUESTIONS = {
    "name": "May I know your full name?",
    "age": "Your age please?",
    "phone": "Your 10-digit phone number?",
    "date": "Preferred appointment time?"
}

def init_patient():
    return {f: None for f in FIELDS} | {
        "mode": "chat",
        "problem": None,
        "department": None,
        "booked": False
    }

def get_next_field(patient):
    for f in FIELDS:
        if not patient[f]:
            return f
    return None