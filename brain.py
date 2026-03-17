import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)

def get_ai_response(messages):
    try:
        chat = model.start_chat(history=[])

        context = ""
        for m in messages:
            if m["role"] != "system":
                context += f"{m['role']}: {m['content']}\n"

        response = chat.send_message(context)
        return response.text.strip()

    except Exception as e:
        return "⚠️ Sorry, I’m facing some technical issues. Please try again later."
