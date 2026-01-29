import ollama

def get_ai_response(messages):
    response = ollama.chat(
        model="phi3",
        messages=messages,
        options={
            "temperature": 0.2,
            "num_predict": 120,
            "top_p": 0.9,
            "repeat_penalty": 1.1
        }
    )
    return response["message"]["content"]
