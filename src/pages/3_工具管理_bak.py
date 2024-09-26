from datetime import datetime
import json
import streamlit as st
import streamlit_antd_components as sac
from core.streamlit_utils import initialize_page, CallBackFunction
from core.database import sql_connection
from models import Tool


def add_param():
    if "parameters" not in st.session_state.tool_params:
        st.session_state.tool_params["parameters"] = []
    st.session_state.tool_params["parameters"].append({})


def del_param():
    if "parameters" not in st.session_state.tool_params:
        st.session_state.tool_params["parameters"] = []
    st.session_state.tool_params["parameters"].pop()


def main():
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

    if tab_select == "工具列表":
        display_tool_list()
    else:
        display_tool_add_form()


def display_tool_list():
    # 保持原有的工具列表显示逻辑
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
    with st.form("tool_form", clear_on_submit=False):
        st.session_state.tool_params["name"] = st.text_input(
            "工具英文名称",
            key="name",
            placeholder="get_current_city_weather",
        )
        st.session_state.tool_params["url"] = st.text_input(
            "接口地址",
            key="url",
            placeholder="http://localhost:8000/api/v1/tools/weather",
        )
        st.session_state.tool_params["description"] = st.text_area(
            "工具描述",
            key="description",
            placeholder="仅在用户明确询问天气、温度、降水、气温等气象信息时使用。获取指定城市的当前天气情况。",
        )

        st.markdown("##### 💡 参数")
        for i, param in enumerate(st.session_state.tool_params["parameters"]):
            with st.expander(f"参数{i + 1}", expanded=True):
                param["name"] = st.text_input(
                    "参数名称", key=f"param_name_{i}", value=param.get("name", "")
                )
                param["type"] = st.text_input(
                    "参数类型", key=f"param_type_{i}", value=param.get("type", "")
                )
                param["description"] = st.text_input(
                    "参数描述",
                    key=f"param_description_{i}",
                    value=param.get("description", ""),
                )
                param["required"] = st.selectbox(
                    "参数是否必须",
                    options=["是", "否"],
                    key=f"param_required_{i}",
                    index=1 if param.get("required") == "是" else 0,
                )
        form_cols = st.columns([1, 1], gap="small")
        with form_cols[0]:
            st.form_submit_button(
                "添加参数", on_click=add_param, use_container_width=True
            )

        with form_cols[1]:
            st.form_submit_button(
                "删除参数", on_click=del_param, use_container_width=True
            )

        if st.form_submit_button("保存", type="primary", use_container_width=True):
            st.success("函数已保存！")
            st.write("保存的工具信息：")
            param_list = st.session_state.tool_params["parameters"]
            json_data = {
                "name": {st.session_state.tool_params["name"]},
                "url": {st.session_state.tool_params["url"]},
                "description": {st.session_state.tool_params["description"]},
                "parameters": {
                    param_list[i]["name"]: {
                        "type": param_list[i]["type"],
                        "description": param_list[i]["description"],
                        "required": param_list[i]["required"],
                    }
                    for i in range(len(param_list))
                },
            }
            with sql_connection() as db:
                data = Tool(json=json_data, enabled=1)
                db.add(data)
                db.commit()
                db.refresh()
                db.close()

            st.json(json_data)


main()
