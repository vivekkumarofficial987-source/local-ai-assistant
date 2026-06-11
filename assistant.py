
import json
from tools import get_time, add


from ollama import chat

try :
    with open("memory.json","r") as file :
        messages =json.load(file)
except:

    messages=[
    {
        "role":"system",
        'content': 'You are an expert Python teacher. Explain concepts simply and give examples.'

    }
     
]
TOOLS = {
    "time": get_time,
    "add": add
}

 
 
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

    

    if user_input.startswith("add"):
        numbers = user_input.split()

        a = int(numbers[1])
        b = int(numbers[2])

        result = TOOLS["add"](a, b)

        print("AI:", result)
        continue

    
    command = user_input.lower()

    if command in TOOLS:
        result = TOOLS[command]()
        print("AI:", result)
        continue


    
    
    
    stream = chat(
        model="llama3.2",
        messages=messages,
        stream=True
    )

    
    answer= ""

    print("AI: ", end="")

    for chunk in stream:
        content=chunk["message"]["content"]
        answer+=content
        print(content ,end="",flush=True)

    print()

    messages.append({
            "role" : "assistant",
            "content" :answer})
    
    with open("memory.json", "w") as file:
        json.dump(messages, file, indent=4)

    


