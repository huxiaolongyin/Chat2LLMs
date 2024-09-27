import streamlit as st

st.set_page_config(
    page_title="HTW ChatBot",
    layout="centered",
    page_icon="🤖",
)

pages = [
    st.Page("st_pages/chatbot.py", title="ChatBot", icon=":material/forum:"),
    st.Page(
        "st_pages/知识库管理.py", title="知识库管理", icon=":material/auto_stories:"
    ),
    st.Page(
        "st_pages/助手管理.py", title="助手管理", icon=":material/smart_toy:"
    ),
    st.Page("st_pages/工具管理.py", title="工具管理", icon=":material/construction:"),
    st.Page("st_pages/使用分析.py", title="使用分析", icon=":material/monitoring:"),
    st.Page(
        "st_pages/问题与建议.py", title="问题与建议", icon=":material/psychology_alt:"
    ),
    st.Page("st_pages/使用帮助.py", title="使用帮助", icon=":material/live_help:"),
]


pg = st.navigation(pages)
pg.run()
