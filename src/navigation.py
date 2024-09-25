import streamlit as st
from streamlit_option_menu import option_menu

PAGES = {
    "首页": "ChatBot.py",
    "知识库管理": "pages/1_知识库管理.py",
    "助手管理": "pages/2_助手管理.py",
    "工具管理": "pages/3_工具管理.py",
    "使用分析": "pages/4_使用分析.py",
    "问题与建议": "pages/5_问题与建议.py",
    "使用帮助": "pages/6_使用帮助.py",
}

ICONS = [
    "house",
    "database",
    "person",
    "tools",
    "graph-up",
    "chat-dots",
    "question-circle",
]


def sidebar_navigation():
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=list(PAGES.keys()),
            icons=ICONS,
            menu_icon="cast",
            default_index=0,
        )

    # if selected != "首页":
    #     st.switch_page(PAGES[selected])

    return selected
