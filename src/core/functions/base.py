from typing import List
import ollama
from core.functions import available_functions
from models import Tool
from core.config import CONFIG
from core.functions import tools
# from core.database import sql_connection

# with sql_connection() as db:
#     # 执行数据库操作
#     res = db.query(Tool)
# tools_content = [i.__dict__ for i in res]
# tools = [
#     {
#         "name": tool["english_name"],
#         "description": tool["description"],
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "city_name": {
#                     "type": "string",
#                     "description": tool["parameters"],
#                 }
#             },
#         },
#     }
#     for tool in tools_content
# ]

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




