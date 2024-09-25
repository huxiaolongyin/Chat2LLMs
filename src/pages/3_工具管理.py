import json
import streamlit as st
import streamlit_antd_components as sac
from core.streamlit_utils import initialize_page

st.title("🚗 工具集")
st.caption("🚀 进行函数调用管理")

initialize_page()

for item in st.session_state.tool_df:
    tool_cols = st.columns([4, 1], vertical_alignment="center")
    with tool_cols[0]:
        json_data = json.loads(str(item["json"]))
        with st.expander(json_data["name"]):
            st.json(json_data)
            if item["enabled"]:
                value = True
            else:
                value = False
    with tool_cols[1]:
        sac.switch(
            label="是否启用",
            align="center",
            size="sm",
            on_label="是",
            off_label="否",
            position="left",
            value=value,
        )
