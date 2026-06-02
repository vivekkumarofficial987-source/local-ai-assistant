
import json
from tools import get_time

from ollama import chat

try :
    with open("memeory.json","r") as file :
        messages =json.load(file)
except:

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

    

    if user_input.startswith("add"):
        numbers = user_input.split()

        a = int(numbers[1])
        b = int(numbers[2])

        print("AI:", a + b)
        continue

    
    if user_input.lower() == "time":
        print("AI:", get_time())
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

    


