SYMPTOM_MAP = {
    "cardiology": ["chest pain", "heart", "palpitations", "high bp", "blood pressure", "breathing problem"],
    "pulmonology": ["cough", "breathing", "asthma", "lungs", "cold", "pneumonia"],
    "ent": ["throat", "ear", "nose", "sinus", "tonsils", "voice"],
    "neurology": ["headache", "migraine", "seizure", "numbness", "brain", "dizziness"],
    "orthopedics": ["bone", "joint", "knee", "back pain", "fracture", "shoulder"],
    "dermatology": ["skin", "rash", "itching", "acne", "hair fall"],
    "gastroenterology": ["stomach", "gas", "vomiting", "digestion", "liver", "abdomen"],
    "general medicine": ["fever", "weakness", "infection", "cold", "body pain"]
}

def recommend_department(symptoms: str):
    symptoms = symptoms.lower()
    matched = []

    for dept, words in SYMPTOM_MAP.items():
        for w in words:
            if w in symptoms:
                matched.append(dept.title())
                break

    if matched:
        return list(set(matched))
    else:
        return ["General Medicine"]
