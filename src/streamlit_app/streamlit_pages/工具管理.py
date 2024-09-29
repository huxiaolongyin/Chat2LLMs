import json
import streamlit as st
from streamlit_app.utils import initialize_page, CallBackFunction


def add_param():
    if "parameters" not in st.session_state.tool_params:
        st.session_state.tool_params["parameters"] = []
    st.session_state.tool_params["parameters"].append({})


def del_param():
    if "parameters" not in st.session_state.tool_params:
        st.session_state.tool_params["parameters"] = []
    st.session_state.tool_params["parameters"].pop()


def main():
    st.title(":material/construction: 工具集")
    st.caption("🚀 进行函数调用管理")

    initialize_page()
    display_tool_list()

    if st.button("添加工具", type="primary", use_container_width=True):
        display_tool_add_form()


def display_tool_list():
    # 保持原有的工具列表显示逻辑
    for item in st.session_state.tool_df:
        tool_cols = st.columns([7, 0.5, 1], vertical_alignment="center")
        with tool_cols[0]:
            json_data = json.loads(item["json"])
            with st.expander(json_data["name"]):
                st.json(json_data)
                if item["enabled"]:
                    value = True
                else:
                    value = False

        with tool_cols[1]:
            st.toggle(
                '1',
                value=value,
                key=f"tool_enabled_{item['tool_id']}",
                on_change=CallBackFunction.tool_enabled_change,
                args=(item["tool_id"],),
                label_visibility="hidden",
            )
        with tool_cols[2]:
            st.button(
                "删除",
                key=f"tool_del_{item['tool_id']}",
                on_click=display_tool_del_form,
                args=(item["tool_id"],),
            )


@st.dialog("确认删除工具", width="small")
def display_tool_del_form(tool_id):

    for item in st.session_state.tool_df:
        if item["tool_id"] == tool_id:
            st.json(item["json"])
            break
    submit, cancel = st.columns([1, 1])
    with submit:
        if st.button("确认", type="primary", use_container_width=True):
            CallBackFunction.tool_del(tool_id)
            st.rerun()
    with cancel:
        if st.button("取消", use_container_width=True):
            st.rerun()


@st.dialog("添加工具", width="large")
def display_tool_add_form():
    with st.form("tool_form", clear_on_submit=False):
        tool_params = st.session_state.tool_params
        tool_params["name"] = st.text_input(
            "工具英文名称",
            key="name",
            placeholder="get_current_city_weather",
            value=tool_params.get("name", ""),
        )
        tool_params["url"] = st.text_input(
            "接口地址(使用post方法)",
            key="url",
            placeholder="http://localhost:8000/api/v1/tools/weather",
            value=tool_params.get("url", ""),
        )
        tool_params["description"] = st.text_area(
            "工具描述",
            key="description",
            placeholder="仅在用户明确询问天气、温度、降水、气温等气象信息时使用。获取指定城市的当前天气情况。",
            value=tool_params.get("description", ""),
        )

        st.markdown("##### 💡 参数")
        for i, param in enumerate(tool_params["parameters"]):
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
            st.info("保存的工具信息：")
            param_list = st.session_state.tool_params["parameters"]
            json_data = json.dumps(
                {
                    "name": tool_params["name"],
                    "url": tool_params["url"],
                    "description": tool_params["description"],
                    "parameters": {
                        param_list[i]["name"]: {
                            "type": param_list[i]["type"],
                            "description": param_list[i]["description"],
                            "required": param_list[i]["required"],
                        }
                        for i in range(len(param_list))
                    },
                }
            )
            st.json(json_data)
            st.form_submit_button(
                "确认",
                on_click=CallBackFunction.tool_add,
                args=(json_data),
                use_container_width=True,
            )


main()
