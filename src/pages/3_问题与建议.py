import pandas as pd
import streamlit as st
from core.database import sql_connection
from sqlalchemy import func
from models import Suggestion

st.set_page_config(
    page_title="HTW ChatBot",
    page_icon="🤖",
)

# 加载自定义样式
with open("src/asset/css/custom.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("💡 问题与建议")
st.caption("🚀 输入你的问题或建议")
# 初始化session state
if "text_input" not in st.session_state:
    st.session_state.text_input = ""


# 定义回调函数
def submit_suggestion():
    """提交建议时的回调函数"""
    if st.session_state.text_input == "":
        st.error("请输入您的建议")
        return
    with sql_connection() as db:
        suggestion = Suggestion(content=st.session_state.text_input)
        db.add(suggestion)
        db.commit()
    st.session_state.text_input = ""  # 清空输入
    st.success("谢谢您宝贵的建议")


# 使用回调函数创建文本区域和提交按钮
text = st.text_area(
    "输入你的问题或建议：",
    key="text_input",
    placeholder="您的建议是产品改进的重要部分",
    label_visibility="collapsed",
    height=200,
)
submit = st.button("提交", on_click=submit_suggestion)

with sql_connection() as db:
    suggestion_count = (
        db.query(
            func.date_format(Suggestion.create_time, "%Y-%m-%d").label("date"), func.count().label("total")
        )
        .group_by(func.date_format(Suggestion.create_time, "%Y-%m-%d"))
        .order_by("date")
    )

st.markdown("### 反馈统计")
statistics_df = pd.DataFrame(suggestion_count.all(), columns=["date", "total"])
st.bar_chart(
    data=statistics_df,
    x="date",
    y="total",
    use_container_width=True,
    x_label="日期",
    y_label="反馈数",
    height=400,
    color="#ce393c",
)