from core.config.setting import CONFIG
import streamlit as st
from typing import List
from models import Message
from core.database import sql_connection
from haystack.dataclasses import Document
from core.retrieval.embedding import HTWDocument
from core.streamlit_config import DEFAULT_MODEL_LIST
from models import Tool
import pandas as pd


def initialize_page():
    """初始化配置"""
    # 初始化session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.message_id = None
    if "knowledge_select_index" not in st.session_state:
        st.session_state.knowledge_select_index = 0
    if "model_list" not in st.session_state:
        st.session_state.model_list = DEFAULT_MODEL_LIST
    if "model_select_index" not in st.session_state:
        st.session_state.model_select_index = 0
    if "store_list" not in st.session_state:
        st.session_state.store_list = HTWDocument().get_store_list()
    # 初始化session state
    if "tool_df" not in st.session_state:
        with sql_connection() as db:
            content = db.query(Tool)
        st.session_state.tool_df = [item.__dict__ for item in content.all()]

    # 加载自定义样式
    with open("src/asset/css/custom.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def display_references(documents: List[Document]):
    """在streamlit 显示文档引用"""
    if documents:
        with st.expander("参考文档"):
            for doc in documents:
                st.write(f"相关度: {doc.score*100:.2f}%。内容：{doc.content}")
                if doc.meta:
                    st.write("元数据:")
                    for key, value in doc.meta.items():
                        st.write(f"- {key}: {value}")


class CallBackFunction:
    """
    回调函数
    """

    @staticmethod
    def knowledge_change():
        """知识库选择改变时的回调函数"""
        st.session_state.knowledge_select_index = st.session_state.store_list.index(
            st.session_state.knowledge_select
        )

    @staticmethod
    def model_change():
        """模型选择改变时的回调函数"""
        st.session_state.model_select_index = st.session_state.model_list.index(
            st.session_state.model_select
        )

        # ollama_persist(model=st.session_state.model_select)

    @staticmethod
    def on_feedback_change():
        """反馈选项改变时的回调函数"""
        feedback_value = st.session_state.feedback

        with sql_connection() as db:
            message = (
                db.query(Message)
                .filter(Message.message_id == st.session_state.message_id)
                .first()
            )
            if message:
                message.evaluation = feedback_value
                db.commit()


class SlideBar:
    """侧边栏集合"""

    @staticmethod
    def main_sidebar():
        """渲染侧边栏"""
        with st.sidebar:
            st.markdown("---")
            knowledge_select = st.selectbox(
                "请选择知识库",
                st.session_state.store_list,
                index=st.session_state.knowledge_select_index,
                on_change=CallBackFunction.knowledge_change,
                key="knowledge_select",
            )
            model = st.selectbox(
                "选择模型(后续支持更多)",
                st.session_state.model_list,
                index=st.session_state.model_select_index,
                on_change=CallBackFunction.model_change,
                key="model_select",
            )
            clean_history = st.button("清空消息历史", use_container_width=True)
            st.markdown(
                f"<div style='text-align: center; bottom: 10px'>v{CONFIG.VERSION}</div>",
                unsafe_allow_html=True,
            )
        return knowledge_select, model, clean_history
