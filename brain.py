import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response(messages):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")

        # Build prompt properly
        prompt = ""
        for m in messages[-6:]:
            if m["role"] == "user":
                prompt += f"User: {m['content']}\n"
            elif m["role"] == "assistant":
                prompt += f"Assistant: {m['content']}\n"

        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
