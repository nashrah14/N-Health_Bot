import streamlit as st
import uuid

from brain import get_ai_response
from hospital_flow import init_patient, get_next_field, QUESTIONS
from doctor_recommender import recommend_department
from storage import init_appointments, save_appointment
from chat_storage import init_chat, save_chat
from hospital_prompt import HOSPITAL_SYSTEM_PROMPT

# ---------------- INIT ----------------
init_appointments()
init_chat()

st.set_page_config(page_title="N-HealthBot Pro", page_icon="🏥")

st.title("🏥 N-HealthBot Pro")

# ---------------- SESSION ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": HOSPITAL_SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello 👋 How can I help you today?"}
    ]

if "patient" not in st.session_state:
    st.session_state.patient = init_patient()

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------------- INPUT ----------------
prompt = st.chat_input("Type your message...")

if prompt:
    p = st.session_state.patient
    lower = prompt.lower()

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_chat("user", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    # -------- INTENT DETECTION --------
    booking_words = ["book", "appointment", "consult", "doctor"]
    symptom_words = ["pain", "fever", "cough", "headache", "vomit", "cold", "dizzy", "weak"]

    is_booking_intent = any(w in lower for w in booking_words)
    has_symptoms = any(w in lower for w in symptom_words)

    # -------- LOGIC --------

    # 1. NORMAL CHAT MODE
    if p["mode"] == "chat":

        if has_symptoms:
            dept = recommend_department(prompt)
            p["problem"] = prompt
            p["department"] = dept
            p["mode"] = "suggested"

            ai_reply = get_ai_response(st.session_state.messages)

            bot_reply = (
                f"{ai_reply}\n\n"
                f"💡 Based on what you shared, consulting **{dept}** would help. "
                f"Would you like me to book an appointment?"
            )

        elif is_booking_intent:
            p["mode"] = "booking"
            bot_reply = "Sure 🙂 Let's get you booked. What's your name?"

        else:
            bot_reply = get_ai_response(st.session_state.messages)

    # 2. SUGGESTED MODE
    elif p["mode"] == "suggested":

        if "yes" in lower or "book" in lower:
            p["mode"] = "booking"
            bot_reply = "Great 🙂 Let's start. What's your name?"

        elif "no" in lower or "later" in lower:
            p["mode"] = "chat"
            bot_reply = "No worries 😊 I'm here whenever you need help."

        else:
            bot_reply = get_ai_response(st.session_state.messages)

    # 3. BOOKING MODE
    elif p["mode"] == "booking":

        field = get_next_field(p)

        if field:
            p[field] = prompt
            next_field = get_next_field(p)

            if next_field:
                questions_map = {
                    "age": "Got it 👍 And your age?",
                    "phone": "Thanks! Could you share your phone number?",
                    "date": "When would you prefer the appointment?"
                }

                bot_reply = questions_map.get(next_field, QUESTIONS[next_field])

            else:
                save_appointment(p)
                p["mode"] = "chat"

                bot_reply = f"""
✅ Appointment booked successfully!

👤 **{p['name']}**  
📅 **{p['date']}**  
🏥 **{p['department']}**

Our team will contact you shortly 😊
"""

        else:
            bot_reply = get_ai_response(st.session_state.messages)

    # 4. FALLBACK
    else:
        bot_reply = get_ai_response(st.session_state.messages)

    # -------- DISPLAY BOT --------
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            st.markdown(bot_reply)

    # Save bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    save_chat("assistant", bot_reply)
