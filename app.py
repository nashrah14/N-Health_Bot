import streamlit as st
import uuid
from brain import get_ai_response
from hospital_flow import init_patient, get_next_field, QUESTIONS
from doctor_recommender import recommend_department
from storage import init_appointments, save_appointment
from chat_storage import init_chat, save_chat
from hospital_prompt import HOSPITAL_SYSTEM_PROMPT

# Init
init_appointments()
init_chat()

st.set_page_config(page_title="N-HealthBot Pro", page_icon="🏥")

# UI Style
st.markdown("""
<style>
.stChatMessage { padding: 8px }
</style>
""", unsafe_allow_html=True)

st.title("🏥 N-HealthBot Pro")

# Session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role":"system","content":HOSPITAL_SYSTEM_PROMPT},
        {"role":"assistant","content":"Hello 👋 How can I help you?"}
    ]

if "patient" not in st.session_state:
    st.session_state.patient = init_patient()

# Display
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.write(m["content"])

# Input
prompt = st.chat_input("Describe your issue...")

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    save_chat("user", prompt)

    with st.chat_message("user"):
        st.write(prompt)

    p = st.session_state.patient

    # Logic
    if p["mode"] == "chat":
        dept = recommend_department(prompt)
        p["problem"] = prompt
        p["department"] = dept
        p["mode"] = "booking"

        reply = f"I recommend **{dept}**. Shall I book an appointment?"

    elif p["mode"] == "booking":
        field = get_next_field(p)

        if field:
            p[field] = prompt
            next_f = get_next_field(p)

            reply = QUESTIONS[next_f] if next_f else "Processing your appointment..."
        else:
            save_appointment(p)
            p["mode"] = "chat"
            reply = "✅ Appointment booked successfully!"

    else:
        reply = get_ai_response(st.session_state.messages)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            st.write(reply)

    st.session_state.messages.append({"role":"assistant","content":reply})
    save_chat("assistant", reply)