from datetime import datetime
import pandas as pd
import streamlit as st
from core.database import sql_connection
from sqlalchemy import func
from models import Issue
import altair as alt

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

if "issue_df" not in st.session_state:
    with sql_connection() as db:
        issue_df = pd.read_sql(db.query(Issue).statement, db.bind)
        issue_df = issue_df.fillna("")
        st.session_state.issue_df = issue_df


st.markdown("##### 💡 添加一个反馈")

with st.form("issue_form"):
    issue = st.text_area(
        "输入你的问题或建议：",
        key="text_input",
        placeholder="您的建议是产品改进的重要部分",
        label_visibility="collapsed",
    )
    priority = st.selectbox(
        "优先级",
        options=["低", "中", "高"],
        index=1,
    )

    submited = st.form_submit_button("提交")

if submited:
    try:
        recent_issue_number = int(max(st.session_state.issue_df.issue_id).split("-")[1])
    except:
        recent_issue_number = 0

    data = {
        "issue_id": f"ISSUE-{recent_issue_number+1}",
        "issue": issue,
        "status": "待解决",
        "priority": priority,
        "create_time": datetime.now(),
    }
    issue_df_new = pd.DataFrame(data=[data])
    # 上传到数据库
    with sql_connection() as db:
        issue = Issue(**data)
        db.add(issue)
        db.commit()

    st.write("问题提交成功! 以下是提交的问题明细:")
    st.dataframe(issue_df_new, use_container_width=True)
    st.session_state.issue_df = pd.concat(
        [st.session_state.issue_df, issue_df_new], ignore_index=True, axis=0
    )

st.write(f"问题总数: `{len(st.session_state.issue_df)}`")

st.info(
    "您可以通过双击单元格来编辑票据。注意下面的图是如何自动更新的！"
    "还可以通过单击列标题对表进行排序。",
    icon="✍️",
)


def edited_df_on_change():
    """
    Callback function to handle changes in the edited DataFrame.
    """
    edited_rows = st.session_state.edited_df["edited_rows"].copy()
    for index, row in edited_rows.items():
        original_row = st.session_state.issue_df.loc[index, :]
        original_row.update(row)

        issue_id = original_row["issue_id"]

        with sql_connection() as db:
            issue = db.query(Issue).filter(Issue.issue_id == issue_id).first()
            issue.status = original_row["status"]
            issue.priority = original_row["priority"]
            issue.status = row["status"]
            if issue.status == "关闭":
                issue.complete_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if issue.status == "进行中":
                issue.response_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.commit()


edited_df = st.data_editor(
    st.session_state.issue_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "issue_id": st.column_config.TextColumn(
            "ID",
            help="issue id",
            required=True,
        ),
        "status": st.column_config.SelectboxColumn(
            "状态",
            help="issue status",
            options=["待解决", "进行中", "关闭"],
            required=True,
        ),
        "priority": st.column_config.SelectboxColumn(
            "优先级",
            help="Priority",
            options=["高", "中", "低"],
            required=True,
        ),
        "issue": st.column_config.TextColumn(
            "问题",
            help="issue description",
            required=True,
        ),
        "create_time": st.column_config.DateColumn(
            "创建时间",
            help="issue create time",
            required=True,
        ),
        "response_time": st.column_config.DateColumn(
            "响应时间",
            help="issue response time",
        ),
        "complete_time": st.column_config.DateColumn(
            "完成时间",
            help="issue complete time",
        ),
    },
    key="edited_df",
    on_change=edited_df_on_change,
    # 禁止编辑 ID 和时间
    disabled=["issue_id", "create_time", "complete_time", "response_time"],
)

st.header("统计")

# Show metrics side by side using `st.columns` and `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(
    st.session_state.issue_df[st.session_state.issue_df.status == "待解决"]
)
# 计算今天新增的待解决问题数
today_open_tickets = len(
    st.session_state.issue_df[
        (st.session_state.issue_df.create_time.dt.date == datetime.now().date())
    ]
)

# 计算最新回应时间
try:
    latest_response_time = st.session_state.issue_df["response_time"].max()
    time_difference = pd.Timestamp.now() - latest_response_time
    hours_difference = time_difference.total_seconds() / 3600
except:
    hours_difference = 9999.99


# 计算每个已解决问题的解决时间
try:
    resolution_time = (
        st.session_state.issue_df["complete_time"]
        - st.session_state.issue_df["create_time"]
    ).dt.total_seconds() / 3600
    average_resolution_time = resolution_time.mean()
except:
    average_resolution_time = 9999.99
col1.metric(label="待解决问题数", value=num_open_tickets, delta=today_open_tickets)
col2.metric(label="最新回应时间(小时)", value=f"{hours_difference:.2f}")
col3.metric(
    label="平均解决时间(小时)",
    value=f"{average_resolution_time:.2f}",
)

# Show two Altair charts using `st.altair_chart`.
st.write("")
st.write("##### 每月问题状态")
status_plot = (
    alt.Chart(edited_df)
    .mark_bar()
    .encode(
        x="month(create_time):O",
        y="count():Q",
        xOffset="status:N",
        color="status:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

st.write("##### 当前任务优先级")
priority_plot = (
    alt.Chart(edited_df)
    .mark_arc()
    .encode(theta="count():Q", color="priority:N")
    .properties(height=300)
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")
