import json
import streamlit as st
import streamlit_antd_components as sac
from core.streamlit_utils import initialize_page, CallBackFunction

st.title("🚗 工具集")
st.caption("🚀 进行函数调用管理")

initialize_page()
tab_select = sac.tabs(
    [
        sac.TabsItem("工具列表", icon=sac.AntIcon("ToolOutlined")),
        sac.TabsItem("工具添加", icon=sac.AntIcon("PlusCircleOutlined")),
    ],
    align="center",
    use_container_width=True,
)


def add_param():
    st.session_state.parameters.append({})


def display_tool_list():
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
                key=f"tool_enabled_{item['tool_id']}",
                on_change=CallBackFunction.tool_enabled_change,
                args=(item["tool_id"],),
            )


def display_tool_add_form():

    st.button("添加参数", on_click=add_param)

    with st.form("tool_form", clear_on_submit=True):
        name = st.text_input(
            "工具英文名称", key="name", placeholder="get_current_city_weather"
        )
        url = st.text_input(
            "接口地址",
            key="url",
            placeholder="http://localhost:8000/api/v1/tools/weather",
        )
        description = st.text_area(
            "工具描述",
            key="description",
            placeholder="仅在用户明确询问天气、温度、降水、气温等气象信息时使用。获取指定城市的当前天气情况。",
        )

        st.markdown("##### 💡 参数")
        for i, param in enumerate(st.session_state.parameters):
            with st.expander(f"参数{i + 1}", expanded=True):
                param_name = st.text_input(
                    "参数名称", key=f"param_name_{i}", value=param.get("name", "")
                )
                param_type = st.text_input(
                    "参数类型", key=f"param_type_{i}", value=param.get("type", "")
                )
                param_description = st.text_input(
                    "参数描述",
                    key=f"param_description_{i}",
                    value=param.get("description", ""),
                )
                param_required = st.selectbox(
                    "参数是否必须",
                    options=["是", "否"],
                    key=f"param_required_{i}",
                    index=0 if param.get("required") == "是" else 1,
                )

                st.session_state.parameters[i] = {
                    "name": param_name,
                    "type": param_type,
                    "description": param_description,
                    "required": param_required,
                }

        if st.form_submit_button("保存"):
            st.success("函数已保存！")
            st.write("保存的参数：")
            st.write(name)
            st.write(url)
            st.write(description)
            for param in st.session_state.parameters:
                st.write(param)


if tab_select == "工具列表":
    display_tool_list()
else:
    display_tool_add_form()
