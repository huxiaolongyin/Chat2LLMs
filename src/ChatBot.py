import streamlit as st
from core.chatbot import ChatBot
from core.retrieval.embedding import HTWDocument
from core.config import CONFIG
from core.utils import (
    get_history_messages,
    on_feedback_change,
    display_references,
    insert_message,
    model_change,
    knowledge_change,
)

# 设置页面配置
st.set_page_config(
    page_title="HTW ChatBot",
    layout="centered",
    page_icon="🤖",
)
# 加载自定义样式
with open("src/asset/css/custom.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 设置页面标题
st.title("💬 HTW ChatBot")
st.caption("🚀 汉特云公司的 LLMs 聊天/知识检索 机器人")


# 初始化状态
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.message_id = None

if "knowledge_select_index" not in st.session_state:
    st.session_state.knowledge_select_index = 0

# 模型列表
if "model_list" not in st.session_state:
    st.session_state.model_list = ["qwen2.5", "llama3.1"]

if "model_select_index" not in st.session_state:
    st.session_state.model_select_index = 0


# 获取知识库列表
if "store_list" not in st.session_state:
    st.session_state.store_list = HTWDocument().get_store_list()


# 添加侧边栏
with st.sidebar:
    st.markdown("---")
    # 知识库选择按钮
    knowledge_select = st.selectbox(
        "请选择知识库",
        st.session_state.store_list,
        index=st.session_state.knowledge_select_index,
        on_change=knowledge_change,
        key="knowledge_select",
    )

    model = st.selectbox(
        "选择模型(后续支持更多)",
        st.session_state.model_list,
        index=st.session_state.model_select_index,
        on_change=model_change,
        key="model_select",
    )

    clean_history = st.button("清空消息历史", use_container_width=True)
    # 在页面底部添加版本信息
    st.markdown(
        f"<div style='text-align: center; bottom: 10px'>v{CONFIG.VERSION}</div>",
        unsafe_allow_html=True,
    )

# 创建一个容器来存放聊天消息, 在容器中显示聊天历史，比较稳定
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# 用户输入
if prompt := st.chat_input("你想说什么?"):

    # 添加用户消息到聊天历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    history_messages = get_history_messages(st.session_state.messages)

    # 获取AI响应
    with st.chat_message("assistant"):
        with st.spinner("生成回答中"):
            chatbot = ChatBot(model=model, store=st.session_state.knowledge_select)
            answer, documents = chatbot.query(prompt, history_messages=history_messages)

            # 显示参考文档
            display_references(documents)

        # 添加回答到聊天历史
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # 添加反馈选项
        st.feedback("thumbs", on_change=on_feedback_change, key="feedback")

    # 插入消息到数据库
    insert_message(
        question=prompt, answer=answer, store=knowledge_select, context_length=8
    )
