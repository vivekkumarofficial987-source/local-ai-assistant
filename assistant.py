import json

from ollama import chat
from tools import get_time, add, system_info,save_profile,get_profile



# Tool Registry
TOOLS = {
    "time": get_time,
    "add": add,
    "system_info": system_info,
    "save_profile": save_profile,
    "get_profile": get_profile
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


save_profile -> use when user says:

- my name is ...
- remember that ...
- save this ...

get_profile -> use when user asks:

- what is my name
- what do you know about me
- what is my favorite language

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

User: My name is Vivek

Response:
{"tool":"save_profile","key":"name","value":"Vivek"}

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


def execute_tool(tool_call):

    tool_name = tool_call["tool"]

    if tool_name not in TOOLS:
        return "Tool not found"

    tool_function = TOOLS[tool_name]

    arguments = {
        k: v
        for k, v in tool_call.items()
        if k != "tool"
    }

    return tool_function(**arguments)


def generate_tool_response(user_input, result):

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": """
            You are an AI assistant.

            A tool has already been executed.

            Use the tool result to answer naturally.
            """
            },
            {
                "role": "user",
                "content": f"""
                User Question:
                {user_input}

                Tool Result:
                    {result}
                """
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

        result = execute_tool(tool_call)

        final_answer = generate_tool_response(
            user_input,
            result)

        print("AI:", final_answer)
        

        messages.append({
            "role": "user",
            "content": user_input
                })


        messages.append({
            "role": "assistant",
            "content": final_answer})
        
        with open("memory.json", "w") as file:
            json.dump(messages, file, indent=4)

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