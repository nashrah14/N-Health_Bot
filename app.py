p = st.session_state.patient
lower = prompt.lower()

# --------- DETECT INTENT ----------
booking_words = ["book", "appointment", "consult", "doctor"]
symptom_words = ["pain","fever","cough","headache","vomit","cold","dizzy","weak"]

is_booking_intent = any(w in lower for w in booking_words)
has_symptoms = any(w in lower for w in symptom_words)

# --------- FLOW CONTROL ----------

# 1. If user is chatting normally → use AI
if p["mode"] == "chat":

    if has_symptoms:
        dept = recommend_department(prompt)
        p["problem"] = prompt
        p["department"] = dept
        p["mode"] = "suggested"

        ai_reply = get_ai_response(st.session_state.messages)

        bot_reply = f"{ai_reply}\n\n💡 Based on this, consulting **{dept}** would help. Would you like me to book an appointment?"

    elif is_booking_intent:
        p["mode"] = "booking"
        bot_reply = "Sure 🙂 Let's get you booked. May I know your name?"

    else:
        bot_reply = get_ai_response(st.session_state.messages)


# 2. If suggestion given → wait for user decision
elif p["mode"] == "suggested":

    if "yes" in lower or "book" in lower:
        p["mode"] = "booking"
        bot_reply = "Great 🙂 Let's start. What's your name?"

    elif "no" in lower or "later" in lower:
        p["mode"] = "chat"
        bot_reply = "No worries 😊 I'm here if you need anything."

    else:
        bot_reply = get_ai_response(st.session_state.messages)


# 3. Booking flow (more conversational)
elif p["mode"] == "booking":

    field = get_next_field(p)

    if field:
        p[field] = prompt
        next_field = get_next_field(p)

        if next_field:
            # conversational questions
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

👤 {p['name']}  
📅 {p['date']}  
🏥 {p['department']}

Our team will contact you shortly 😊
"""

    else:
        bot_reply = get_ai_response(st.session_state.messages)


# fallback
else:
    bot_reply = get_ai_response(st.session_state.messages)
