from ollama import chat
import json

from tools import get_time

response = chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": """
You are a tool selector.

Available tools:

1. time
2. add

When a tool is needed respond ONLY with JSON.

Examples:

User: What time is it?
Response:
{"tool":"time"}

User: Add 10 and 20
Response:
{"tool":"add","a":10,"b":20}

If no tool is needed:
{"tool":"none"}
"""
        },
        {
            "role": "user",
            "content": "What time is it?"
        }
    ]
)

answer = response["message"]["content"] # gets the content of the answer llama givs

print(answer)

tool_call = json.loads(answer) # converts  the answer into a dictionary

print(tool_call)

tool_name = tool_call["tool"] #gets the tool name 

print(tool_name)

TOOLS = {
    "time": get_time
}
result = TOOLS[tool_name]()

print(result)

final_response = chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": """
You are an AI assistant.

The tool has already been executed.

Use the tool result directly to answer the user.

Do not say:
'I think'
'It looks like'
'I don't know'

Just answer using the tool result.
"""
        },
        {
            "role": "user",
            "content": f"""
Original Question:
What time is it?

Tool Result:
{result}  
"""
        }
    ]
)

print(final_response["message"]["content"])