import streamlit as st
from core.retrieval import HTWDocument
import pandas as pd

from core.streamlit_utils import CallBackFunction
import streamlit_antd_components as sac

st.set_page_config(
    page_title="HTW ChatBot",
    page_icon="🤖",
)

# 加载自定义样式
with open("src/asset/css/custom.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📝 知识库管理")
st.caption("🚀 汉特云公司的知识库管理系统")

# 获取知识库列表
if "store_list" not in st.session_state:
    st.session_state.store_list = HTWDocument().get_store_list()
if "knowledge_select_index" not in st.session_state:
    st.session_state.knowledge_select_index = 0


def new_knowledge(name: str):
    """新建知识库"""
    result = HTWDocument().new_store(name)
    if not name or name == "请输入知识库名称":
        st.error("知识库创建失败，失败原因：没有输入知识库名称")
        return
    with st.spinner("正在创建知识库..."):
        if result["create_status"] == "SUCCESS":
            st.success("知识库创建成功")
            st.session_state.store_list.append(name)
        else:
            st.error("知识库创建失败，失败原因：" + result["message"])


def del_knowledge(name: str):
    """删除知识库"""
    result = HTWDocument().del_store(store=name)
    if not name or name == "请输入知识库名称":
        st.error("知识库删除失败，失败原因：没有选择知识库")
        return
    with st.spinner("正在删除知识库..."):
        if result["delete_status"] == "SUCCESS":
            st.success("知识库删除成功")
            st.session_state.store_list.remove(name)
        else:
            st.error("知识库删除失败，失败原因：" + result["message"])


with st.sidebar:
    st.markdown("---")
    knowledge_select = st.selectbox(
        "请选择知识库",
        st.session_state.store_list,
        key="knowledge_select",
        on_change=CallBackFunction.knowledge_change,
        index=st.session_state.knowledge_select_index,
    )
    knowledge_list = [
        item.model_dump() for item in HTWDocument(knowledge_select).get_documents()
    ]

    total = len(knowledge_list)
    st.metric(label="知识总数", value=total)
    new_knowledge_name = st.text_input(
        "请输入新知识库名称",
        placeholder="请输入新知识库名称",
        label_visibility="collapsed",
    )
    know_button = st.button(
        "新建知识库",
        on_click=new_knowledge,
        use_container_width=True,
        key="new_knowledge",
        args=(new_knowledge_name,),
    )
    del_button = st.button(
        "删除知识库",
        on_click=del_knowledge,
        args=(knowledge_select,),
        use_container_width=True,
    )

# 创建一个数据框来显示知识库内容
st.markdown("### 知识库内容")
try:
    df = pd.DataFrame(knowledge_list)["content"]
except Exception as e:
    df = pd.DataFrame()
st.dataframe(
    df,
    hide_index=True,
    # height=500,
    column_config={
        # "id": st.column_config.TextColumn("ID", width=150),
        "content": st.column_config.TextColumn("内容"),
    },
    use_container_width=True,
)


st.markdown("---")
st.markdown("### 上传知识库")
st.caption("🚀 将同一行内容，用英文冒号分隔，如：问题:答案——tips: 公司加密文件无法上传")
uploader_file = st.file_uploader(
    "上传知识库", type=["xlsx", "xls"], label_visibility="collapsed"
)


def upload_knowledge(documents: list):
    total = len(documents)
    with st.status(f"正在上传知识到{knowledge_select}...") as status:
        progress_bar = st.progress(0)
        for i, document in enumerate(documents):
            HTWDocument(knowledge_select).write_docs([document])
            progress_bar.progress((i + 1) / total)
        status.update(label="知识库上传成功", state="complete", expanded=False)


if uploader_file is not None:
    if uploader_file.name.endswith(".csv"):
        df = pd.read_csv(uploader_file, sep=";")
    elif uploader_file.name.endswith(".xlsx" or ".xls"):
        df = pd.read_excel(uploader_file)
    process_df = df.apply(lambda row: ":".join(row.values.astype(str)), axis=1)
    st.dataframe(
        process_df,
        hide_index=True,
        use_container_width=True,
    )
    st.markdown(f"知识总数：{len(process_df)}")
    upload_columns = st.columns(3)
    with upload_columns[1]:
        submit_button = st.button(
            "确认上传",
            on_click=upload_knowledge,
            args=(process_df.tolist(),),
            key="submit_knowledge",
            use_container_width=True,
        )
