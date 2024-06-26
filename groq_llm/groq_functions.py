
def get_groq_tools():
    groq_tools = []

    tool_name = [
        "get_goals",
        "get_tasks"
    ]

    tool_desc = [
        "Fetch the sprint goals of an iteration.",
        "Fetch the tasks of an iteration, with sprint_id being the sprint goal associated with it"
    ]

    tools_prop = {
        "iteration": {
            "type": "integer",
            "description": "The iteration cycle of the sprint, required for the specific iteration."
        }
    }

    tools_req = ["iteration"]

    for name, desc in zip(tool_name, tool_desc):
        tool_dict = {
            "type": "function",
            "function": {
                "name": name,
                "description": desc,
                "parameters": {
                    "type": "object",
                    "properties": tools_prop,
                    "required": tools_req,
                },
            },
        }
        groq_tools.append(tool_dict)
    
    return groq_tools
