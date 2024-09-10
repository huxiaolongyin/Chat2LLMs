import streamlit as st
from haystack.dataclasses import ChatMessage
from core import ChatBot

# 设置页面标题
st.set_page_config(page_title="HTW ChatBot")

# 设置页面标题
st.title("HTW ChatBot")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 创建一个容器来存放聊天消息
chat_container = st.container()

# 在容器中显示聊天历史
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("你想说什么?"):
    # 添加用户消息到聊天历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    history_messages = [
        ChatMessage.from_system(
            content="你是一个先进的人工智能助手，名字叫 笨笨同学，你的目标是帮助用户并提供有用、安全和诚实的回答。请遵循以下准则：\n1. 现在提供一些查询内容，使用中文直接回答问题。\n2. 如果查询内容与问题不相关，请直接根据问题回答。\n3. 提供准确和最新的信息。如果不确定，请说明你不确定。\n4. 尽可能给出清晰、简洁的回答，但在需要时也要提供详细解释。\n5. 请使用人性化的语言。\n6. 不必说”根据参考内容“，也不必说“答案是”，请直接回复答案。\n你已准备好协助用户解决各种问题和任务。请以友好和乐于助人的态度开始对话。"
        )
    ]
    history_messages.append(
        ChatMessage.from_user("问题：{{question}}，参考内容：{{content}}")
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    # 获取AI响应
    with st.chat_message("assistant"):
        with st.spinner("Generating response . . ."):
            bot = ChatBot()
            response = bot.query(prompt, history_messages=history_messages)[0].content
        st.session_state.messages.append({"role": "assistant", "content": response})
