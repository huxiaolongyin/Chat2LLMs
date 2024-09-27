import streamlit as st
from core.streamlit_utils import initialize_page, CallBackFunction

st.title(":material/smart_toy: 助手管理")
st.caption("🚀 汉特云公司的助手管理")
initialize_page()


row = st.columns(3) * (len(st.session_state.assistant_list) // 3 + 1)


@st.dialog("助手管理", width="small")
def assistant_manage(assistant_id):
    """助手管理对话框"""
    if assistant_id == "new":
        name = st.text_input("助手名称", "")
        description = st.text_input("描述", "")
        prompt = st.text_area("提示词", height=200)
    else:
        for assistant in st.session_state.assistant_list:
            if assistant["assistant_id"] == assistant_id:
                name = st.text_input("助手名称", assistant["name"])
                description = st.text_input("描述", value=assistant["description"])
                prompt = st.text_area("提示词", value=assistant["prompt"], height=200)

    if st.button("保存", use_container_width=True, key="assistant_save"):
        CallBackFunction.assistant_save(assistant_id, name, description, prompt)
        st.rerun()
    if st.button(
        "删除", use_container_width=True, type="primary", key="assistant_delete"
    ):
        CallBackFunction.assistant_delete(assistant_id)
        st.rerun()


for i, col in enumerate(row):
    if i < len(st.session_state.assistant_list):
        with col.container(height=190):
            st.markdown(f'#### {st.session_state.assistant_list[i]["name"]}')
            st.write(st.session_state.assistant_list[i]["description"])
            st.button(
                "查看",
                use_container_width=True,
                key=f"assistant_manage{col}",
                on_click=assistant_manage,
                args=(st.session_state.assistant_list[i]["assistant_id"],),
            )
st.button(
    "添加助手",
    use_container_width=True,
    type="primary",
    key=f"assistant_edit{col}",
    on_click=assistant_manage,
    args=("new",),
)
