import streamlit as st
from haystack.dataclasses import ChatMessage


def on_knowledge_change(knowledge):
    """更新知识库"""
    st.session_state.knowledge = knowledge


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
