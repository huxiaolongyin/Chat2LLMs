import streamlit as st
from haystack import Pipeline
from haystack.dataclasses import ChatMessage
from core import ChatBot 

# Constants to store key names in the config dictionary
TITLE_NAME = 'HTW ChatBot'
UI_RENDERED_MESSAGES = 'ui_rendered_messages'
CHAT_HISTORY = 'chat_history'
CONVERSATIONAL_PIPELINE = 'conversational_pipeline'


def main():
    """
    呈现检索增强生成(RAG)聊天机器人应用程序
    """
    config = load_config()
    initialize_session_state(config)
    setup_page()
    render_chat_history()
    manage_chat()


def load_config():
    """
    从文件或对象加载应用程序配置

    Returns:
        dict: Configuration dictionary containing title name,
    UI呈现的消息、聊天历史记录和会话管道实例。  
    """
    return {
        TITLE_NAME: 'HTW ChatBot',
        UI_RENDERED_MESSAGES: [],
        CHAT_HISTORY: [],
        CONVERSATIONAL_PIPELINE: ChatBot()
    }


def setup_page():
    """
        设置Streamlit页面配置和标题。
    """
    st.set_page_config(page_title=st.session_state[TITLE_NAME])
    st.title(st.session_state[TITLE_NAME])


def initialize_session_state(config):
    """
        使用提供的配置初始化Streamlit会话状态变量。

    Args:
        config (dict): Configuration dictionary.
    """
    for key, value in config.items():
        if key not in st.session_state:
            st.session_state[key] = value


def manage_chat():
    """
       处理与会话AI的用户交互，并呈现用户查询和AI响应。
    """
    if prompt := st.chat_input('我能帮你些什么?'):
        # Render user message.
        with st.chat_message('user'):
            st.markdown(prompt)
        st.session_state[UI_RENDERED_MESSAGES].append({'role': 'user', 'content': prompt})

        # Render AI assistant's response.
        with st.chat_message('assistant'):
            with st.spinner('Generating response . . .'):
                response = st.session_state[CONVERSATIONAL_PIPELINE].query(prompt)
        st.session_state[UI_RENDERED_MESSAGES].append({'role': 'assistant', 'content': response[0].content})


def render_chat_history():
    """
        显示会话状态中存储的聊天消息历史记录。
    """
    for message in st.session_state[UI_RENDERED_MESSAGES]:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
            print(message)


if __name__ == '__main__':
    main()