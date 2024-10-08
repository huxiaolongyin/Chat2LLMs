import ollama
import requests
from typing import List
from core.config import CONFIG
from core.utils import generate_tools_conf

tools, tool_url = generate_tools_conf()


def generate_function_response(question: str, model: str) -> List[dict]:
    """执行通用的函数调用功能，并返回结果"""
    client = ollama.Client(host=CONFIG.OLLAMA_HOST)
    llm_response = client.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        tools=tools,
    )

    # 如果没获取到函数
    if not llm_response["message"].get("tool_calls"):
        print(f"未获取到函数，函数响应：{llm_response}")
        return

    # 如果获取到了函数
    if llm_response["message"].get("tool_calls"):
        result = []
        for tool in llm_response["message"]["tool_calls"]:

            # 获取函数方法
            function_name = tool["function"]["name"]
            print(tool_url[function_name])
            print(tool["function"]["arguments"])    
            function_response = requests.post(
                tool_url[function_name], json=tool["function"]["arguments"]
            ).json()

            result.append(
                {
                    "function_name": function_name,
                    "function_response": function_response,
                },
            )

        return result
