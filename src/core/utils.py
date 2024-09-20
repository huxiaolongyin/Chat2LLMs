import asyncio
import streamlit as st
from typing import List
from models import Message
from core.database import sqlite_connection
from haystack.dataclasses import StreamingChunk, Document, ChatMessage


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


def on_feedback_change():
    """反馈选项改变时的回调函数"""
    feedback_value = st.session_state.feedback

    with sqlite_connection() as db:
        message = (
            db.query(Message)
            .filter(Message.message_id == st.session_state.message_id)
            .first()
        )
        if message:
            message.evaluation = feedback_value
            db.commit()


def get_history_messages(messages: list = None) -> list:
    """获取历史消息"""
    history_messages = [
        ChatMessage.from_system(
            content="你是一个先进的人工智能助手，名字叫 笨笨同学，你的目标是帮助用户并提供有用、安全和诚实的回答。请遵循以下准则：\n1. 现在提供一些查询内容，使用中文直接回答问题。\n2. 如果查询内容与问题不相关，请直接根据问题回答。\n3. 提供准确和最新的信息。如果不确定，请说明你不确定。\n4. 尽可能给出清晰、简洁的回答，但在需要时也要提供详细解释。\n5. 请使用人性化的语言。\n6. 不必说”根据参考内容“，也不必说“答案是”，请直接回复答案。\n你已准备好协助用户解决各种问题和任务。请以友好和乐于助人的态度开始对话。"
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


def display_references(documents: List[Document]):
    """在streamlit 显示文档引用"""
    if documents:
        with st.expander("参考文档"):
            for doc in documents:
                st.write(f"相关度: {doc.score*100:.2f}%。内容：{doc.content}")
                if doc.meta:
                    st.write("元数据:")
                    for key, value in doc.meta.items():
                        st.write(f"- {key}: {value}")


def insert_message(question, answer, store, context_length: int = 8):
    """插入消息到数据库"""
    # 插入消息到数据库
    with sqlite_connection() as db:
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


def model_change():
    """模型选择改变时的回调函数"""
    st.session_state.model_select_index = st.session_state.model_list.index(
        st.session_state.model_select
    )


def knowledge_change():
    """知识库选择改变时的回调函数"""
    st.session_state.knowledge_select_index = st.session_state.store_list.index(
        st.session_state.knowledge_select
    )


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
from core.database import sqlite_connection
from sqlalchemy import text


def find_city_code(city_name):
    """根据城市名称找到城市代码"""
    with sqlite_connection() as session:
        city_code = session.execute(text("SELECT * FROM city_code")).fetchall()
    city_code_dict = {city[0]: city[1] for city in city_code}
    best_match = process.extractOne(city_name, city_code_dict.keys())
    if best_match[1] >= 80:  # 设置一个匹配度阈值，例如 80%
        return city_code_dict[best_match[0]]
    return None  # 如果没有找到足够接近的匹配
