import json
import requests
import os
from groq import Groq
from groq_llm.groq_functions import get_groq_tools
from goal_n_tasks.goal_singleton import get_goals, get_tasks

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)
    
def run_conversation(list_messages, model_name):
    # Step 1: send the conversation and available functions to the model
    messages = list_messages
    tools = get_groq_tools()
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=1024,
        temperature=1
    )
    print("First response received...")
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        print(tool_calls)
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_goals": get_goals,
            "get_tasks": get_tasks,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            print("Tool in use...")
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                            iteration=function_args.get("iteration")
                        )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        print("Generating second response...")
        second_response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=1024,
            temperature=1
        )  # get a new response from the model where it can see the function response
        print(second_response.choices[0].message.content)
        return second_response.choices[0].message.content
    else:
        print(response_message.content)
        return response_message.content


def simulation():
    messages = []

    system_prompt = """
You are a Scrum Master, strict, non-negotiable, unwavering and stoic, guiding the user with precision and authority. When a user requests specific goals and tasks, clearly specify the interaction and use the function call method. If goals and tasks are not explicitly requested, maintain a normal discussion, offering guidance and support as needed. Always ensure interactions are driven towards achieving clear objectives, maintaining the highest standards of discipline and efficiency.
"""

    messages.append({"role":"system","content":system_prompt})

    user_input = input("User: ")

    while user_input!="stop":
        print("\n","-"*50,"\n")
        messages.append({"role":"user","content":user_input})
        print("Generating first response...")
        groq_resp = run_conversation(list_messages=messages, model_name="llama3-70b-8192")
        print("\n","-"*50,"\n")
        print("\n","Groq: ",groq_resp)
        print("\n","="*50,"\n")

        messages.append({"role":"assistant","content":groq_resp})

        user_input = input("User: ")