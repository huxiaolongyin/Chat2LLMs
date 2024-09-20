from typing import List
import ollama
from core.functions import available_functions

from core.config import CONFIG
from core.functions import tools


def generate_function_response(question, model) -> List[dict]:
    """返回，执行的函数及函数结果"""
    client = ollama.Client(host=CONFIG.OLLAMA_HOST)
    messages = [
        {
            "role": "user",
            "content": question,
        }
    ]
    response = client.chat(
        model=model,
        messages=messages,
        tools=tools,
    )
    # 如果没获取到函数
    print(response)
    if not response["message"].get("tool_calls"):
        print("The model didn't use the function. Its response was:")
        print(response["message"]["content"])
        return

    # 如果获取到了函数
    if response["message"].get("tool_calls"):
        result = []
        for tool in response["message"]["tool_calls"]:
            function_to_call = available_functions[tool["function"]["name"]]
            function_response = function_to_call(**tool["function"]["arguments"])
            function_name = tool["function"]["name"]
            result.append(
                (
                    {"function_name": function_name},
                    {"function_response": function_response},
                )
            )

        return result
