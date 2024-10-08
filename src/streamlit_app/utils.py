from datetime import datetime
from core.config.setting import CONFIG
import streamlit as st
from typing import List
from models import Message, Assistant, Tool
from core.database import sql_connection
from haystack.dataclasses import Document
from core.embedding import HTWDocument
from streamlit_app.config import DEFAULT_MODEL_LIST
import pandas as pd
import streamlit_antd_components as sac
from models import Issue


def initialize_page():
    """初始化配置"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.message_id = None

    if "page_current" not in st.session_state:
        st.session_state.page_current = 1

    # 助手列表
    if "assistant_list" not in st.session_state:
        with sql_connection() as db:
            content = db.query(Assistant)
        st.session_state.assistant_list = [item.__dict__ for item in content.all()]

    if "assistant_name_list" not in st.session_state:
        st.session_state.assistant_name_list = [
            item["name"] for item in st.session_state.assistant_list
        ]

    if "assistant_select_index" not in st.session_state:
        st.session_state.assistant_select_index = 0
        st.session_state.assistant_select = st.session_state.assistant_name_list[0]

    if "model_list" not in st.session_state:
        st.session_state.model_list = DEFAULT_MODEL_LIST

    if "model_select_index" not in st.session_state:
        st.session_state.model_select_index = 0

    if "store_list" not in st.session_state:
        st.session_state.store_list = HTWDocument().get_all_knowledge_store_names()

    if "knowledge_select_index" not in st.session_state:
        st.session_state.knowledge_select_index = 0
        st.session_state.knowledge_select = st.session_state.store_list[0]

    if "knowledge_df" not in st.session_state:
        CallBackFunction.knowledge_change()

    if "tool_df" not in st.session_state:
        with sql_connection() as db:
            content = db.query(Tool)
        st.session_state.tool_df = [item.__dict__ for item in content.all()]

    if "tool_params" not in st.session_state:
        st.session_state.tool_params = {"parameters": []}

    if "quick_use_show" not in st.session_state:
        quick_use()
        st.session_state.quick_use_show = True

    # 加载自定义样式
    with open("src/asset/css/custom.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if "assistant_prompt" not in st.session_state:
        CallBackFunction.assistant_change()


@st.dialog("快速入门", width="large")
def quick_use():
    """编写入门指导的对话框"""
    steps = sac.steps(
        items=[
            sac.StepsItem(title="step 1", description="配置"),
            sac.StepsItem(title="step 2", description="沟通"),
            sac.StepsItem(title="step 3", description="参考内容"),
            sac.StepsItem(title="step 4", description="更多"),
        ],
    )
    if steps == "step 1":
        st.subheader("在左边选择合适的助手、知识库、模型")
        st.image("src/asset/static/step1.png")
    elif steps == "step 2":
        st.subheader("与智能助手进行沟通")
        st.image("src/asset/static/step2.png")
    elif steps == "step 3":
        st.subheader("查看参考内容或进行反馈结果")
        st.image("src/asset/static/step3.png")
    elif steps == "step 4":
        st.subheader("查看更多功能")
        with st.expander("知识库管理"):
            st.subheader("支持知识库查看、删除")
            st.image("src/asset/static/step4_1.png")
            st.subheader("支持从excel上传知识库")
            st.write("将每行的知识库内容以冒号分隔，上传到知识库")
            st.image("src/asset/static/step4_2.png")
        with st.expander("工具管理"):
            st.subheader("可到工具列表查看可用工具，提问时会自动关联并使用")
            st.image("src/asset/static/step4_3.png")
        st.subheader("更多功能查看帮助文档")
    if st.button("关闭", use_container_width=True, type="primary"):
        st.rerun()


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
    def assistant_change():
        """助手选择改变时的回调函数"""
        st.session_state.assistant_select_index = (
            st.session_state.assistant_name_list.index(
                st.session_state.assistant_select
            )
        )
        for assistant in st.session_state.assistant_list:
            if assistant["name"] == st.session_state.assistant_select:
                st.session_state.assistant_prompt = assistant["prompt"]

    @staticmethod
    def knowledge_change():
        """知识库选择改变时的回调函数"""
        st.session_state.knowledge_select_index = st.session_state.store_list.index(
            st.session_state.knowledge_select
        )
        knowledge_documents = [
            item.model_dump()
            for item in HTWDocument(
                st.session_state.knowledge_select
            ).get_knowledge_content_or_all()
        ]
        st.session_state.knowledge_df = pd.DataFrame(knowledge_documents).to_dict(
            "records"
        )

    @staticmethod
    def model_change():
        """模型选择改变时的回调函数"""
        st.session_state.model_select_index = st.session_state.model_list.index(
            st.session_state.model_select
        )

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

    @staticmethod
    def assistant_save(
        assistant_id, assistant_name, assistant_description, assistant_prompt
    ):
        """助手保存"""
        if assistant_id == "new":
            assistant = Assistant(
                name=assistant_name,
                description=assistant_description,
                prompt=assistant_prompt,
            )
            with sql_connection() as db:
                db.add(assistant)
        else:
            with sql_connection() as db:
                assistant = (
                    db.query(Assistant)
                    .filter(Assistant.assistant_id == assistant_id)
                    .first()
                )
                assistant.name = assistant_name
                assistant.description = assistant_description
                assistant.prompt = assistant_prompt

        st.session_state.assistant_list = [
            item.__dict__
            for item in db.query(Assistant).order_by(Assistant.create_time).all()
        ]
        st.session_state.assistant_name_list = [
            item["name"] for item in st.session_state.assistant_list
        ]

    @staticmethod
    def assistant_delete(assistant_id):
        """助手删除"""
        with sql_connection() as db:
            assistant = (
                db.query(Assistant)
                .filter(Assistant.assistant_id == assistant_id)
                .first()
            )
            db.delete(assistant)
        st.session_state.assistant_list = [
            item.__dict__
            for item in db.query(Assistant).order_by(Assistant.create_time).all()
        ]

    @staticmethod
    def tool_enabled_change(tool_id):
        """工具启用状态改变时的回调函数"""
        with sql_connection() as db:
            tool = db.query(Tool).filter(Tool.tool_id == tool_id).first()
            tool.enabled = not tool.enabled
        st.session_state.tool_df = [item.__dict__ for item in db.query(Tool).all()]

    @staticmethod
    def tool_del(tool_id):
        """工具删除"""
        with sql_connection() as db:
            tool = db.query(Tool).filter(Tool.tool_id == tool_id).first()
            db.delete(tool)
        st.session_state.tool_df = [item.__dict__ for item in db.query(Tool).all()]

    @staticmethod
    def tool_add(json_data):
        """工具添加"""
        with sql_connection() as db:
            tool = Tool(json=json_data, enabled=1)
            db.add(tool)
        st.session_state.tool_df = [item.__dict__ for item in db.query(Tool).all()]
        st.success("添加成功")

    @staticmethod
    def del_knowledge_store(store: str):
        """知识库删除"""
        HTWDocument().delete_knowledge_store(store=store)
        st.session_state.store_list.remove(store)

    @staticmethod
    def del_knowledge(knowledge_id: list):
        """知识删除"""
        HTWDocument(st.session_state.knowledge_select).delete_knowledge_content(
            knowledge_id
        )
        st.session_state.knowledge_df = [
            item.model_dump()
            for item in HTWDocument(
                st.session_state.knowledge_select
            ).get_knowledge_content_or_all()
        ]

    @staticmethod
    def edited_issue_on_change():
        """
        当 issue 发生改变时，更新数据库
        """
        edited_rows = list(st.session_state.edited_df["edited_rows"].keys())[0]
        issue_changed = list(st.session_state.edited_df["edited_rows"].values())[0]
        for key, value in issue_changed.items():
            st.session_state.issue_df.loc[edited_rows, key] = value
        update_issue = st.session_state.issue_df.loc[edited_rows, :]

        issue_id = update_issue["issue_id"]
        issue = update_issue["issue"]
        status = update_issue["status"]
        priority = update_issue["priority"]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if status == "待解决":
            response_time = None
            complete_time = None
        elif status == "进行中":
            response_time = current_time
            complete_time = None
        else:

            response_time = (
                current_time
                if pd.isna(st.session_state.issue_df.loc[edited_rows, "response_time"])
                else st.session_state.issue_df.loc[edited_rows, "response_time"]
            )
            complete_time = current_time

        st.session_state.issue_df.loc[edited_rows, "response_time"] = response_time
        st.session_state.issue_df.loc[edited_rows, "complete_time"] = complete_time

        with sql_connection() as db:
            issue_data = db.query(Issue).filter(Issue.issue_id == issue_id).first()
            issue_data.issue = issue
            issue_data.status = status
            issue_data.priority = priority
            issue_data.response_time = response_time
            issue_data.complete_time = complete_time

    @staticmethod
    def clean_history():
        """清空消息历史"""
        st.session_state.messages = []
        st.session_state.message_id = None


class SlideBar:
    """侧边栏集合"""

    @staticmethod
    def main_sidebar():
        """渲染侧边栏"""
        with st.sidebar:

            st.markdown("---")
            assistant_select = st.selectbox(
                "选择助手",
                st.session_state.assistant_name_list,
                index=st.session_state.assistant_select_index,
                on_change=CallBackFunction.assistant_change,
                key="assistant_select",
            )
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
            clean_history = st.button(
                "清空消息历史",
                use_container_width=True,
                on_click=CallBackFunction.clean_history,
            )
            st.markdown(
                f"<div style='text-align: center; bottom: 10px'>v{CONFIG.VERSION}</div>",
                unsafe_allow_html=True,
            )
        return knowledge_select, model, clean_history
