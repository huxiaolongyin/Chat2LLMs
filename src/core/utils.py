import asyncio
import json
from core.config.setting import CONFIG
import requests
import streamlit as st
from models import Message
from core.database import sql_connection
from haystack.dataclasses import StreamingChunk, ChatMessage
from models import Tool


def convert_parameters(params):
    """将参数转换为 tools 的参数格式"""
    new_params = {"type": "object", "properties": {}, "required": []}

    for key, value in params.items():
        new_params["properties"][key] = {
            "type": value["type"],
            "description": value["description"],
        }
        if value.get("required", False):
            new_params["required"].append(key)

    return new_params


def generate_tools_conf():
    """从数据库中加载函数配置，加载可用函数"""

    with sql_connection() as db:
        result = db.query(Tool).filter(Tool.enabled == 1)

    tool_json_list = [json.loads(item.__dict__["json"]) for item in result.all()]
    tools = [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": convert_parameters(tool["parameters"]),
            },
        }
        for tool in tool_json_list
    ]
    tool_url = {tool["name"]: tool["url"] for tool in tool_json_list}
    return tools, tool_url


def check_openinference():
    """检测 llms 的运行情况"""
    from openinference.instrumentation.haystack import HaystackInstrumentor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter,
    )
    from opentelemetry.sdk import trace as trace_sdk
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor

    endpoint = "http://localhost:6006/v1/traces"  # The URL to your Phoenix instance
    tracer_provider = trace_sdk.TracerProvider()
    tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))
    HaystackInstrumentor().instrument(tracer_provider=tracer_provider)


def get_history_messages(messages: list = None) -> list:
    """获取历史消息"""
    history_messages = [
        ChatMessage.from_system(
            content=st.session_state.assistant_prompt
        )
    ]
    for message in messages[-8:]:
        if message["role"] == "user":
            history_messages.append(ChatMessage.from_user(message["content"]))
        elif message["role"] == "assistant":
            history_messages.append(ChatMessage.from_assistant(message["content"]))
    history_messages.append(
        ChatMessage.from_user("问题：{{question}}，参考内容：{{content}}")
    )
    return history_messages


def insert_message(question, answer, store, context_length: int = 8):
    """插入消息到数据库"""
    # 插入消息到数据库
    with sql_connection() as db:
        message = Message(
            chat_id="Browser_APP",
            question=question,
            answer=answer,
            store=store,
            context_length=context_length,
        )
        db.add(message)
        db.flush()

        # 获取最新的message_id
        st.session_state.message_id = message.message_id
        db.commit()


def ollama_persist(model: str):
    """持久化ollama模型"""
    json_data = {"model": model, "messages": [], "keep_alive": "-1m"}
    url = f"http://{CONFIG.OLLAMA_URL}/api/chat"
    requests.post(url=url, json=json_data)


class StreamingMannager:
    """进行流式输出的管理"""

    def __init__(self):
        # 创建一个新的事件循环，来处理队列，初始化队列内容
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.queue = asyncio.Queue()
        self.running = True

    def create_empty_placeholder(self):
        """创建一个空的占位符"""
        self.placeholder = st.empty()
        self.tokens = []

    def write_streaming_chunk(self, chunk: StreamingChunk):
        """写入流式输出的内容"""
        self.queue.put_nowait(chunk)
        self.tokens.append(chunk.content)
        self.placeholder.write("".join(self.tokens))

    def write_end_chunk(self):
        """添加结束指令到序列"""
        self.queue.put_nowait("None")


from fuzzywuzzy import process
from sqlalchemy import text


def find_city_code(city_name):
    """根据城市名称找到城市代码"""
    with sql_connection() as session:
        city_code = session.execute(text("SELECT * FROM city_code")).fetchall()
    city_code_dict = {city[0]: city[1] for city in city_code}
    best_match = process.extractOne(city_name, city_code_dict.keys())
    if best_match[1] >= 80:  # 设置一个匹配度阈值，例如 80%
        return city_code_dict[best_match[0]]
    return None  # 如果没有找到足够接近的匹配
