from ollama import chat

messages=[
    {
        "role":"system",
        'content': 'You are an expert Python teacher. Explain concepts simply and give examples.'

    }
     
]

while True:
    user_input = input("you:")

    if user_input.lower()=="exit":
        break

    messages.append(
        {
            "role": "user",
            "content":user_input
        }
    )
    print(messages)
    
    
    response = chat(
        model="llama3.2",
        messages=messages
    )

    
    answer=response["message"]["content"]

    print("AI:",answer)

    messages.append({
            "role" : "assistant",
            "content" :answer})


