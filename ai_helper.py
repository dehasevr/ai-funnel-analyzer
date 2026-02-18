import ollama

def ask_llama(prompt):
    response = ollama.chat(
        model="llama3",
        messages=[
            {
            "role":"user",
            "content": prompt
            }
            
        ]
    )
    return response["message"]["content"]

