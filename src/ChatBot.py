import streamlit as st
from haystack.dataclasses import ChatMessage
from core.chatbot import ChatBot
from core.retrieval.embedding import HTWDocument
from core.database import sqlite_connection
from models import Message
from core.config import CONFIG

st.set_page_config(page_title="HTW ChatBot", page_icon=":robot:")

# 隐藏顶部菜单和页脚
st.markdown(
    """
    <style>
        # #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        stDecoration {display:none;}
    </style>
""",
    unsafe_allow_html=True,
)

# 添加侧边栏
with st.sidebar:
    store_list = HTWDocument().get_store_list()
    knowledge = st.selectbox("请选择知识库", store_list, index=1)
    model = st.selectbox("选择模型", ["llama3.1", "后续支持"])
    clean_history = st.button("清空消息历史")
    # 在页面底部添加版本信息 style='position: fixed; bottom: 10px; right: 10px; font-size: 12px;'
    st.markdown(
        f"<div style='text-align: center; bottom: 10px'>v{CONFIG.VERSION}</div>",
        unsafe_allow_html=True,
    )

# 设置页面标题
st.title("💬 HTW ChatBot")
st.caption("🚀 汉特云公司的 LLMs 聊天/知识检索 机器人")


# 初始化聊天历史
if "messages" not in st.session_state or clean_history:
    st.session_state.messages = []
    st.session_state.message_id = None

# 创建一个容器来存放聊天消息
chat_container = st.container()

# 在容器中显示聊天历史
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def _history_messages(messages: list = None) -> list:
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


# 用户输入
if prompt := st.chat_input("你想说什么?"):

    # 添加用户消息到聊天历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    history_messages = _history_messages(st.session_state.messages)

    # 获取AI响应
    with st.chat_message("assistant"):
        with st.spinner("生成回答中..."):
            bot = ChatBot(store=knowledge)
            response = bot.query(prompt, history_messages=history_messages)[0].content
        st.session_state.messages.append({"role": "assistant", "content": response})

        # 添加反馈选项
        st.feedback("thumbs", on_change=on_feedback_change, key="feedback")

    # 插入消息到数据库
    with sqlite_connection() as db:
        message = Message(
            chat_id="Browser_APP",
            question=prompt,
            answer=response,
            store=knowledge,
            context_length=8,
        )
        db.add(message)
        db.flush()
        # 获取最新的message_id
        st.session_state.message_id = message.message_id
        db.commit()
