import inspect, requests, json
from rich import print_json
from tools.toolDef import *
import rich

from .customPrompt import functions_prompt, get_chat_history

tools_map = {
    "get_weather": get_weather,
    "calculate_mortgage_payment": calculate_mortgage_payment,
    "get_article_details": get_article_details,
    "get_directions": get_directions,
    "convert_currency": convert_currency,
    "get_current_time": get_current_time,
    "generic_response_no_tool": generic_response_no_tool,
}

def generate_full_completion(model_endpoint: str, model: str, prompt: str, **kwargs) -> dict[str, str]:
    params = {"model": model, "prompt": prompt, "stream": False}
    try:
        response = requests.post(
            f"{model_endpoint}/api/generate",
            headers={"Content-Type": "application/json"},
            data=json.dumps(params),
            timeout=60,
        )
        # print(f"🤖 Request: {json.dumps(params)} -> Response: {response.text}")
        response.raise_for_status()
        return json.loads(response.text)
    except requests.RequestException as err:
        return {"error": f"API call error: {str(err)}"}


def call_ai(prompt, model_endpoint, model_name):
    question = functions_prompt + get_chat_history() + "User prompt:\n" + prompt
    response = generate_full_completion(model_endpoint, model_name, question)
    try:
        tidy_response = (
            response.get("response", response)
            .strip()
            .replace("\n", "")
            .replace("\\", "")
        )
        print_json(tidy_response)
        actions = json.loads(tidy_response)
        list_of_actions = actions["tools"]

        if isinstance(list_of_actions['tool'],str):
            print('Single tool execution')
            tool_resp = tools_map[list_of_actions['tool']](**list_of_actions['tool_input'])
            return [tool_resp]
        elif isinstance(list_of_actions['tool'],list):
            print('Multi tool executions')
            tool_resp_list = []
            for tool in list_of_actions['tool']:
                tool_resp = tools_map[tool['tool']](**tool['tool_input'])
                tool_resp_list.append(tool_resp)

            return tool_resp_list
            
        # rich.print(
        #     f"[bold]Total duration: {int(response.get('total_duration')) / 1e9} seconds [/bold]"
        # )
    except Exception as e:
        print(f"❌ Unable to decode JSON.") # {response}")
        return [["Sorry, I dont know how to respond to your request"]]




