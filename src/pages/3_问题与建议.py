import streamlit as st
from core.database import sqlite_connection
from models.suggestion import Suggestion

st.set_page_config(page_title="HTW ChatBot", page_icon=":robot:")

st.title("💡 问题与建议")

# 初始化session state
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

# 定义回调函数
def submit_suggestion():
    with sqlite_connection() as db:
        suggestion = Suggestion(content=st.session_state.text_input)
        db.add(suggestion)
        db.commit()
    st.session_state.text_input = ""  # 清空输入
    st.success("谢谢您宝贵的建议")

# 使用回调函数创建文本区域和提交按钮
text = st.text_area("输入你的问题或建议：", key="text_input")
submit = st.button("提交", on_click=submit_suggestion)