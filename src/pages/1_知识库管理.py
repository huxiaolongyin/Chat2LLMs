import streamlit as st
from core.retrieval import HTWDocument
import pandas as pd

st.set_page_config(page_title="HTW ChatBot", page_icon=":robot:")
st.title("📝 知识库管理")
st.caption("🚀 汉特云公司的知识库管理系统")

with st.sidebar:
    store_list = HTWDocument().get_store_list()
    knowledge = st.selectbox("请选择知识库", store_list, index=1)
    knowledge_list = [
        item.model_dump() for item in HTWDocument(knowledge).get_documents()
    ]
    total = len(knowledge_list)
    st.metric(label="知识总数", value=total)


df = pd.DataFrame(knowledge_list)
st.dataframe(
    df,
    height=500,
    column_config={
        "id": st.column_config.TextColumn("ID", width=150),
        "content": st.column_config.TextColumn("内容", width=600),
    },
)
