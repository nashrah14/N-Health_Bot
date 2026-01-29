FIELDS_ORDER = ["name", "age", "phone", "date"]

QUESTIONS = {
    "name": "May I know your full name?",
    "age": "Thanks. Could you please tell me your age?",
    "phone": "Please share your phone number so our hospital team can contact you.",
    "date": "What date and time would you prefer for the appointment?"
}

def init_patient():
    return {
        "mode": "chat",         
        "name": None,
        "age": None,
        "phone": None,
        "problem": None,
        "date": None,
        "department": None,
        "recommended": None,
        "booked": False          
    }

def get_next_field(patient):
    for field in FIELDS_ORDER:
        if not patient.get(field):
            return field
    return None
