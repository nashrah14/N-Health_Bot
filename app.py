import streamlit as st
import uuid
import re

from hospital_prompt import HOSPITAL_SYSTEM_PROMPT
from brain import get_ai_response
from hospital_flow import init_patient, get_next_field, QUESTIONS
from storage import init_appointments, save_appointment
from chat_storage import init_chat_file, save_message
from doctor_recommender import recommend_department


# ---------------- INIT FILES ----------------
init_chat_file()
init_appointments()

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="N-HealthBot", page_icon="🏥")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
[data-testid="stChatMessage"] { padding: 6px; }

.chat-user [data-testid="stChatMessageContent"] {
    background-color: #DCF8C6;
    border-radius: 12px;
    padding: 10px 14px;
    max-width: 70%;
    margin-left: auto;
}

.chat-bot [data-testid="stChatMessageContent"] {
    background-color: #F1F0F0;
    border-radius: 12px;
    padding: 10px 14px;
    max-width: 70%;
    margin-right: auto;
}
</style>
""", unsafe_allow_html=True)

st.title("🏥 N-HealthBot - Hospital Assistant")


# ---------------- SMART HELPERS ----------------
YES_WORDS = ["yes","yeah","yep","y","ok","okay","sure","haa","haan","ji","book","appointment","confirm"]
NO_WORDS = ["no","nope","nah","not now","later","cancel","don't","do not"]

def is_yes(text):
    return any(w in text for w in YES_WORDS)

def is_no(text):
    return any(w in text for w in NO_WORDS)

def valid_name(name):
    return bool(re.fullmatch(r"[A-Za-z ]{2,40}", name.strip()))

def valid_age(age):
    return age.isdigit() and 0 < int(age) < 120

def valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

def valid_date(text):
    return len(text.strip()) >= 3

def clean_problem(text):
    keywords = [
        "fever","cold","cough","headache","stomach pain","chest pain",
        "vomiting","infection","weakness","dizziness","breathing"
    ]
    for k in keywords:
        if k in text.lower():
            return k.title()
    return "General Health Issue"


# ---------------- SESSION SETUP ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": HOSPITAL_SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello 👋 Welcome to our hospital. How can I help you today?"}
    ]

if "patient" not in st.session_state:
    st.session_state.patient = init_patient()


# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        css = "chat-user" if msg["role"] == "user" else "chat-bot"
        st.markdown(f"<div class='{css}'>", unsafe_allow_html=True)
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
        st.markdown("</div>", unsafe_allow_html=True)


# ---------------- INPUT ----------------
prompt = st.chat_input("Type your message...")

if prompt:
    sid = st.session_state.session_id
    patient = st.session_state.patient
    lower = prompt.lower()

    # ----- SAVE USER -----
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message(sid, "user", prompt)

    st.markdown("<div class='chat-user'>", unsafe_allow_html=True)
    with st.chat_message("user"):
        st.markdown(prompt)
    st.markdown("</div>", unsafe_allow_html=True)


    # ---------------- LOGIC ----------------

    # 1. SYMPTOMS → SUGGEST DEPARTMENT (ONLY BEFORE BOOKING)
    if patient["mode"] == "chat" and not patient["booked"] and any(w in lower for w in [
        "cold","cough","throat","fever","pain","infection","headache",
        "vomit","stomach","chest","breathing","dizzy","weak"
    ]):
        rec = recommend_department(prompt)
        patient["problem"] = clean_problem(prompt)
        patient["recommended"] = rec
        patient["department"] = rec[0]
        patient["mode"] = "suggested"

        bot_reply = (
            f"I’m sorry you’re feeling unwell. Based on what you shared, "
            f"I recommend consulting **{rec[0]}**. Would you like me to book an "
            f"appointment under this department?"
        )

    # 2. ACCEPT BOOKING
    elif patient["mode"] == "suggested" and is_yes(lower):
        patient["mode"] = "booking"
        bot_reply = "Sure 🙂 " + QUESTIONS[get_next_field(patient)]

    # 3. DECLINE BOOKING
    elif patient["mode"] == "suggested" and is_no(lower):
        patient["mode"] = "chat"
        bot_reply = "No problem. If you need help later, feel free to ask."

    # 4. UNCLEAR RESPONSE
    elif patient["mode"] == "suggested":
        bot_reply = "Just to confirm — would you like me to book an appointment for you?"

    # 5. BOOKING FLOW
    elif patient["mode"] == "booking":
        field = get_next_field(patient)
        valid = True

        if field == "name":
            if valid_name(prompt):
                patient["name"] = prompt.title()
            else:
                bot_reply = "Please enter a valid full name (only letters, like: Ayesha Khan)."
                valid = False

        elif field == "age":
            if valid_age(prompt):
                patient["age"] = prompt
            else:
                bot_reply = "Please enter a valid age (for example: 20)."
                valid = False

        elif field == "phone":
            if valid_phone(prompt):
                patient["phone"] = prompt
            else:
                bot_reply = "Please enter a valid 10-digit phone number."
                valid = False

        elif field == "date":
            if valid_date(prompt):
                patient["date"] = prompt
            else:
                bot_reply = "Please tell a preferred date or time (for example: Tomorrow at 7 PM)."
                valid = False

        if valid:
            next_field = get_next_field(patient)

            if next_field:
                bot_reply = QUESTIONS[next_field]
            else:
                save_appointment(patient, sid)

                patient["booked"] = True  
                patient["mode"] = "chat"

                bot_reply = f"""
✅ **APPOINTMENT REQUEST RECEIVED**

👤 **Name:** {patient['name']}  
🎂 **Age:** {patient['age']}  
📞 **Phone:** {patient['phone']}  
🩺 **Problem:** {patient['problem']}  
📅 **Preferred Time:** {patient['date']}  
🏥 **Department:** {patient['department']}

Our hospital team will contact you shortly to confirm your appointment.

In the meantime, feel free to ask me for home remedies, precautions, or general health advice 🙂
"""

    # 6. DEFAULT CHAT RESPONSE
    else:
        ai_reply = get_ai_response(st.session_state.messages)
        bot_reply = ai_reply.strip()

        if len(bot_reply) > 400:
            bot_reply = bot_reply[:400]
            if "." in bot_reply:
                bot_reply = bot_reply.rsplit(".", 1)[0] + "."


    st.markdown("<div class='chat-bot'>", unsafe_allow_html=True)
    with st.chat_message("assistant"):
        with st.spinner("N-HealthBot is typing..."):
            st.markdown(bot_reply)
    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    save_message(sid, "assistant", bot_reply)
