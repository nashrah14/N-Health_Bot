SYMPTOM_MAP = {
    "Cardiology": ["chest pain", "heart", "palpitations"],
    "Pulmonology": ["cough", "breathing", "cold"],
    "ENT": ["throat", "ear", "nose"],
    "Neurology": ["headache", "dizziness"],
    "Orthopedics": ["joint", "bone", "back pain"],
    "Dermatology": ["skin", "rash"],
    "Gastroenterology": ["stomach", "vomiting"],
    "General Medicine": ["fever", "weakness", "infection"]
}

def recommend_department(symptoms: str):
    symptoms = symptoms.lower()
    for dept, words in SYMPTOM_MAP.items():
        if any(w in symptoms for w in words):
            return dept
    return "General Medicine"