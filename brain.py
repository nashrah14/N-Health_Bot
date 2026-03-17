import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)

def get_ai_response(messages):
    try:
        chat = model.start_chat(history=[])

        # Build conversation context
        for m in messages[-6:]:
            if m["role"] == "user":
                chat.send_message(m["content"])
            elif m["role"] == "assistant":
                chat.send_message(m["content"])

        # Get latest response
        response = chat.send_message("Respond naturally to the last user message.")

        return response.text.strip()

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
