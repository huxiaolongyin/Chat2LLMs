import streamlit as st
from models import Message
from sqlalchemy import func
from core.database import sqlite_connection
import pandas as pd

st.set_page_config(page_title="HTW ChatBot", page_icon=":robot:")

st.title("🎢 使用分析")
st.caption("🚀 聊天记录统计")


with sqlite_connection() as db:
    statistics = (
        db.query(
            func.date(Message.create_time).label("date"),
            func.count().label("message_count"),
        )
        .group_by(func.date(Message.create_time))
        .order_by("date")
    )
    eval = (
        db.query(
            func.date(Message.create_time).label("date"),
            Message.evaluation,
            func.count().label("total"),
        )
        .filter(Message.evaluation.isnot(None))
        .group_by(func.date(Message.create_time), Message.evaluation)
        .order_by("date")
    )

st.markdown("### 交流统计")
statistics_df = pd.DataFrame(statistics.all(), columns=["date", "message_count"])
st.line_chart(
    data=statistics_df,
    x="date",
    y="message_count",
    use_container_width=True,
    x_label="日期",
    y_label="交流数",
    height=400,
    color="#ce393c",
)
st.markdown("---")
st.markdown("### 评价统计")

eval_df = pd.DataFrame(eval.all(), columns=["date", "evaluation", "total"])
chart_data = pd.DataFrame(
    {
        "date": eval_df["date"],
        "好评": eval_df[eval_df["evaluation"] == "1"]["total"],
        "差评": eval_df[eval_df["evaluation"] == "0"]["total"],
    }
)
st.line_chart(
    data=chart_data,
    x="date",
    y=["好评", "差评"],
    use_container_width=True,
    x_label="日期",
    y_label="交流数",
    height=400,
)
