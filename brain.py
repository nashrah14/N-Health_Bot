import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def get_ai_response(messages):
    try:
        chat = model.start_chat(history=[])

        context = ""
        for m in messages[-6:]:  # only last few messages (important)
            if m["role"] != "system":
                context += f"{m['role']}: {m['content']}\n"

        response = chat.send_message(context)
        return response.text.strip()

    except:
        return "Sorry, I'm having trouble right now. Please try again."
