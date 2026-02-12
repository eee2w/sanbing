import streamlit as st

# ---------- 初始化会话状态 ----------
for box in ['box1', 'box2', 'box3']:
    if box not in st.session_state:
        st.session_state[box] = ''   # 空字符串表示未选择

# ---------- 回调函数：当任意选择框变化时执行 ----------
def on_change(changed_box):
    """当某个选择框的值变化时，检查并清空其他框中相同的选项"""
    new_value = st.session_state[changed_box]
    if new_value:   # 只有选择了非空项时才需要冲突处理
        # 其他两个框的 key
        other_boxes = [b for b in ['box1', 'box2', 'box3'] if b != changed_box]
        for other in other_boxes:
            if st.session_state[other] == new_value:
                st.session_state[other] = ''   # 清空旧框

# ---------- 页面布局 ----------
st.title("⚙️ 人员选择器（甲、乙、丙，每人仅一次）")
st.markdown("三个框分别选择，同一人只能出现在一个框中。\n\n"
            "**规则**：当你在一个框中选中某个人，而这个人已经在其他框中被选中时，"
            "**原先选中这个人的那个框会自动清空**。")

col1, col2, col3 = st.columns(3)

with col1:
    st.selectbox(
        "框 1",
        options=['', '甲', '乙', '丙'],
        key='box1',
        on_change=on_change,
        args=('box1',)
    )

with col2:
    st.selectbox(
        "框 2",
        options=['', '甲', '乙', '丙'],
        key='box2',
        on_change=on_change,
        args=('box2',)
    )

with col3:
    st.selectbox(
        "框 3",
        options=['', '甲', '乙', '丙'],
        key='box3',
        on_change=on_change,
        args=('box3',)
    )

# ---------- 显示当前选择状态（用于验证） ----------
st.divider()
st.subheader("当前选择结果")
st.write(f"📦 框1：{st.session_state.box1 or '（未选）'}")
st.write(f"📦 框2：{st.session_state.box2 or '（未选）'}")
st.write(f"📦 框3：{st.session_state.box3 or '（未选）'}")
