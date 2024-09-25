import pandas as pd
import streamlit as st
from models import Tool
from core.database import sql_connection

st.title("🚗 工具集")
st.caption("🚀 进行函数调用管理")

# 初始化session state
if "tool_df" not in st.session_state:
    with sql_connection() as db:
        tool_df = pd.read_sql(db.query(Tool).statement, con=db.bind)
        tool_df = tool_df.fillna("")
        st.session_state.tool_df = tool_df

st.markdown("##### 💡 添加工具")

with st.form("tool_form"):
    name = st.text_input(
        "工具名称",
        key="name",
        placeholder="获取当前天气信息",
        label_visibility="collapsed",
    )
    link = st.text_input(
        "工具链接",
        key="link",
        placeholder="http//:localhost:8000/api/v1/weather",
        label_visibility="collapsed",
    )
    method = st.selectbox(
        "工具方法",
        key="method",
        options=["GET", "POST"],
        label_visibility="collapsed",
    )
    english_name = st.text_input(
        "工具英文名称",
        key="english_name",
        placeholder="get_current_weather",
    )
    description = st.text_area(
        "工具描述",
        key="description",
        placeholder="仅在用户明确询问天气、温度、降水、气温等气象信息时使用。获取指定城市的当前天气情况。",
    )
    parameters = st.text_area(
        "函数参数",
        key="parameters",
        placeholder="city_name:中国城市的名称，如果不指定则会返回空值, para2: description2 ...",
    )
    submited = st.form_submit_button("提交")

if submited:
    with sql_connection() as db:
        tool = Tool(
            name=name,
            link=link,
            method=method,
            english_name=english_name,
            description=description,
            parameters=parameters,
        )
        db.add(tool)
        db.commit()
    st.success("提交成功")
    # st.session_state.tool_df = pd.read_sql(db.query(Tool).all(), con=db.bind)


st.write(f"工具总数: `{len(st.session_state.tool_df)}`")
st.info(
    "您可以通过双击单元格来编辑工具。注意下面的图是如何自动更新的！"
    "还可以通过单击列标题对表进行排序。",
    icon="✍️",
)


def edited_df_on_change():
    """
    Callback function to handle changes in the edited DataFrame.
    """
    edited_rows = st.session_state.tool_edited_df["edited_rows"].copy()
    for index, row in edited_rows.items():
        original_row = st.session_state.tool_df.loc[index, :]
        original_row.update(row)
        with sql_connection() as db:
            tool = db.query(Tool).filter(Tool.tool_id == original_row.tool_id).first()
            tool.name = original_row.name
            tool.link = original_row.link
            tool.method = original_row.method
            tool.english_name = original_row.english_name
            tool.description = original_row.description
            tool.parameters = original_row.parameters
            db.commit()


# 显示数据
st.data_editor(
    st.session_state.tool_df,
    disabled=["tool_id", "create_time", "update_time"],
    use_container_width=True,
    hide_index=True,
    on_change=edited_df_on_change,
    key="tool_edited_df",
)
