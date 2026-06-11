import json

from ollama import chat
from tools import get_time, add, system_info


# Tool Registry
TOOLS = {
    "time": get_time,
    "add": add,
    "system_info": system_info
}

# Load Memory
try:
    with open("memory.json", "r") as file:
        messages = json.load(file)
except:
    messages = [
        {
            "role": "system",
            "content": "You are an expert with 20 years of experience."
        }
    ]


# Tool Selector
def select_tool(user_input):

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": """
You are a tool selector.

Available tools:

time -> use for:
- what time is it
- current time
- tell me the time
- time now

add -> use for:
- add numbers
- addition
- calculate sums

system_info -> use for:
- RAM usage
- memory usage
- CPU usage
- system performance
- how much RAM am I using
- how much memory is used

IMPORTANT:
Return ONLY valid JSON.

Examples:

User: What time is it?
Response:
{"tool":"time"}

User: Tell me the current time
Response:
{"tool":"time"}

User: Add 10 and 20
Response:
{"tool":"add","a":10,"b":20}

User: How much RAM am I using?
Response:
{"tool":"system_info"}

User: What's my CPU usage?
Response:
{"tool":"system_info"}

User: Hello
Response:
{"tool":"none"}
"""
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response["message"]["content"]

    


# Main Loop
while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # Ask Tool Selector
    tool_answer = select_tool(user_input)

    print("Tool Selector:", tool_answer)

    try:
        tool_call = json.loads(tool_answer)
    except:
        tool_call = {"tool": "none"}

    # Tool Execution
    tool_name = tool_call.get("tool", "none")

    if tool_name != "none":
        print("tool_call =", tool_call)

        if tool_call["tool"] == "time":

            result = TOOLS["time"]()

            print("AI:", result)
            print("Tool Selector:", tool_answer)
            print("Parsed Tool Call:", tool_call)

            continue

        if tool_call["tool"] == "add":

            result = TOOLS["add"](
                tool_call["a"],
                tool_call["b"]
            )

            print("AI:", result)

            continue
        
        if tool_name == "system_info":

            result = TOOLS["system_info"]()

            print(
                    f"AI: CPU Usage: {result['cpu']}% | RAM Usage: {result['ram']}%"
                    )

            continue
    # Normal Chat
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    print(messages)

    stream = chat(
        model="llama3.2",
        messages=messages,
        stream=True
    )

    answer = ""

    print("AI: ", end="")

    for chunk in stream:

        content = chunk["message"]["content"]

        answer += content

        print(content, end="", flush=True)

    print()

    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with open("memory.json", "w") as file:
        json.dump(messages, file, indent=4)