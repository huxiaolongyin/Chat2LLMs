import streamlit as st


def main():
    st.set_page_config(
        page_title="HTW ChatBot",
        layout="centered",
        page_icon="🤖",
    )

    pages = [
        st.Page("streamlit_pages/chatbot.py", title="ChatBot", icon=":material/forum:"),
        st.Page(
            "streamlit_pages/知识库管理.py", title="知识库管理", icon=":material/auto_stories:"
        ),
        st.Page("streamlit_pages/助手管理.py", title="助手管理", icon=":material/smart_toy:"),
        st.Page(
            "streamlit_pages/工具管理.py", title="工具管理", icon=":material/construction:"
        ),
        st.Page("streamlit_pages/使用分析.py", title="使用分析", icon=":material/monitoring:"),
        st.Page(
            "streamlit_pages/问题与建议.py",
            title="问题与建议",
            icon=":material/psychology_alt:",
        ),
        st.Page("streamlit_pages/使用帮助.py", title="使用帮助", icon=":material/live_help:"),
    ]

    pg = st.navigation(pages)
    pg.run()


if __name__ == "__main__":
    main()
