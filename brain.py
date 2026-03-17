import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)
def get_ai_response(messages):
    try:
        # Convert messages into a proper prompt
        prompt = ""
        for m in messages[-6:]:
            if m["role"] != "system":
                role = "User" if m["role"] == "user" else "Assistant"
                prompt += f"{role}: {m['content']}\n"

        response = model.generate_content(prompt)

        if response and response.text:
            return response.text.strip()
        else:
            return "Hmm, I didn't get that. Could you rephrase?"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
