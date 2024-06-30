import inspect
from tools.toolDef import *
from typing import get_type_hints
import streamlit as st

def get_type_name(t):
    name = str(t)
    if "list" in name or "dict" in name:
        return name
    else:
        return t.__name__


def function_to_json(func):
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)

    function_info = {
        "name": func.__name__,
        "description": func.__doc__,
        "parameters": {"type": "object", "properties": {}},
        "returns": type_hints.get("return", "void").__name__,
    }

    for name, _ in signature.parameters.items():
        param_type = get_type_name(type_hints.get(name, type(None)))
        function_info["parameters"]["properties"][name] = {"type": param_type}

    return json.dumps(function_info, indent=2)

def get_chat_history():
    if 'messages' in st.session_state:
        chat_history = st.session_state.messages
        return 'Chat History\n' + '\n'.join([f"{s['role']}:{s['content']}" for s in chat_history[-5:]])
    return 'Chat History:\n'


functions_prompt = f"""
You have access to the following tools:
{function_to_json(get_weather)}
{function_to_json(calculate_mortgage_payment)}
{function_to_json(get_directions)}
{function_to_json(get_article_details)}
{function_to_json(convert_currency)}
{function_to_json(get_current_time)}
{function_to_json(generic_response_no_tool)}

You must follow these instructions:
Always select one or more of the above tools based on the user query
If a tool is found, you must respond in the JSON format matching the following schema:
{{
   "tools": {{
        "tool": "<name of the selected tool>",
        "tool_input": <parameters for the selected tool, matching the tool's JSON schema
   }}
}}
{{
  "tools": {{
    "tool": [
      {{
        "tool": "name of the selected tool",
        "tool_input": <parameters for the selected tool, matching the tool's JSON schema>
      }},
      {{
        "tool":"name of the selected tool",
        "tool_input":  <parameters for the selected tool, matching the tool's JSON schema>
      }}
    ]
  }}
}}

{{
   "tools": {{
        "tool": "generic_response_no_tool",
        "tool_input": {{
            "answer":"response from the language model for the question"
            }}
   }}
}}


If there are multiple tools required, make sure a list of tools are returned in a JSON array.
If there is no tool that match the user request, 
choose the tool generic_response_no_tool and respond in JSON format as above, 
where tool_input is actually your response to the user prompt.
If know the tool to use but dont know the tool_input, clarify from the user, respond using generic_response_no_tool.
Do not add any additional Notes or Explanations
    """