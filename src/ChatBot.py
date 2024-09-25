import random
import streamlit as st
from core.chatbot import ChatBot
from core.retrieval.embedding import HTWDocument
from core.config import CONFIG
from core.utils import (
    get_history_messages,
    insert_message,
)
from core.streamlit_utils import (
    CallBackFunction,
    SlideBar,
    initialize_page,
    display_references,
)
from core.streamlit_config import WELCOME_MESSAGE

# 设置页面配置
st.set_page_config(
    page_title="HTW ChatBot",
    layout="centered",
    page_icon="🤖",
)
# 设置页面标题
st.title("💬 HTW ChatBot")
st.caption("🚀 汉特云公司的 LLMs 聊天/知识检索 机器人")

# 初始化页面
initialize_page()

# 初始化侧边栏
knowledge_select, model, clean_history = SlideBar.main_sidebar()

# 欢迎词
st.chat_message("assistant").write(WELCOME_MESSAGE)

# 创建一个容器来存放聊天消息, 在容器中显示聊天历史，比较稳定
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input(prompt, model, knowledge_select):
    """处理用户输入"""
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    history_messages = get_history_messages(st.session_state.messages)

    with st.chat_message("assistant"):
        with st.spinner("生成回答中"):
            chatbot = ChatBot(model=model, store=knowledge_select)
            answer, documents = chatbot.query(prompt, history_messages=history_messages)
            display_references(documents)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.feedback(
            "thumbs", on_change=CallBackFunction.on_feedback_change, key="feedback"
        )

    insert_message(
        question=prompt, answer=answer, store=knowledge_select, context_length=8
    )


prompt = st.chat_input("你想说什么?")


if prompt:
    handle_user_input(prompt, model, knowledge_select)

# st.caption("我猜你想问：")
# suggestions = random.sample(PROMPT_SUGGESTIONS, min(3, len(PROMPT_SUGGESTIONS)))
# button_cols = st.columns(3)
# for i, suggestion in enumerate(suggestions):
#     if button_cols[i].button(
#         suggestion,
#         use_container_width=True,
#     ):
#         prompt = suggestion
