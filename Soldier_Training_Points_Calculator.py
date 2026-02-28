import streamlit as st
import pandas as pd

st.title("最强爆兵积分计算器")

st.markdown("""
支持训练和晋升两种计算模式：
游戏内点击左上方头像下的战力，即可在里面找到**“兵营训练速度”**
""")

# ---------- 常量定义 ----------
MAX_LEVEL = 11  # 最高等级（1~11，可修改）

# ---------- 预设数据 ----------
default_time_per_sec = {
    i: i * 5 * 60.0 for i in range(1, MAX_LEVEL + 1)
}  # 示例：1级=300秒，2级=600秒，... 可根据实际调整

# 各等级训练积分（按需修改）
point_dict = {
    1: 90, 2: 120, 3: 180, 4: 270, 5: 390,
    6: 610, 7: 840, 8: 1150, 9: 1520, 10: 2000,
    11: 2490
}

# 等级显示名称
level_display_names = {
    1: "1级兵", 2: "2级兵", 3: "3级兵", 4: "4级兵", 5: "5级兵",
    6: "6级兵", 7: "7级兵", 8: "8级兵", 9: "9级兵", 10: "10级兵",
    11: "宫1兵"
}

# ---------- 辅助函数 ----------
def format_hms(seconds):
    total_sec = int(round(seconds))
    hours = total_sec // 3600
    minutes = (total_sec % 3600) // 60
    secs = total_sec % 60
    return f"{hours}时{minutes}分{secs}秒"

# ---------- 侧边栏：可编辑的训练时长与积分 ----------
with st.sidebar:
    st.header("⚙️ 单个士兵训练时长")
    
    col_title1, col_title2, col_title3 = st.columns([1.2, 2, 1])
    with col_title1:
        st.markdown("**等级**")
    with col_title2:
        st.markdown("**训练时长 (秒)**")
    with col_title3:
        st.markdown("**积分**")

    for level in range(1, MAX_LEVEL + 1):
        cols = st.columns([1.2, 2, 1])
        with cols[0]:
            st.write(level_display_names[level])
        with cols[1]:
            key = f"time_input_{level}"
            st.number_input(
                "秒",
                value=float(default_time_per_sec[level]),
                min_value=0.1,
                step=0.1,
                format="%.1f",
                key=key,
                label_visibility="collapsed"
            )
        with cols[2]:
            st.write(f"**{point_dict[level]}**")

# ---------- 主页面 ----------
st.subheader("⚙️ 设置参数")

mode = st.radio("选择功能", ["训练", "晋升"], horizontal=True, index=0)

# 根据模式显示等级选择
if mode == "训练":
    level = st.selectbox(
        "选择士兵等级",
        options=list(range(1, MAX_LEVEL + 1)),
        format_func=lambda x: level_display_names[x]
    )
    # 从 session_state 获取时长，若不存在则使用默认值（防御性编程）
    current_time_per_sec = st.session_state.get(f"time_input_{level}", default_time_per_sec[level])
    initial_level = None  # 占位
else:  # 晋升模式
    col_initial, col_target = st.columns(2)
    with col_initial:
        initial_level = st.selectbox(
            "初始等级",
            options=list(range(1, MAX_LEVEL)),  # 不能选最高级作为初始
            format_func=lambda x: level_display_names[x],
            key="initial_level"
        )
    with col_target:
        # 目标等级必须 > 初始等级，且 ≤ MAX_LEVEL
        target_options = list(range(initial_level + 1, MAX_LEVEL + 1))
        target_level = st.selectbox(
            "目标等级",
            options=target_options,
            format_func=lambda x: level_display_names[x],
            key="target_level"
        )
    # 读取时长（同样做防御性获取）
    initial_time = st.session_state.get(f"time_input_{initial_level}", default_time_per_sec[initial_level])
    target_time = st.session_state.get(f"time_input_{target_level}", default_time_per_sec[target_level])

# 训练速度加成
col1, col2 = st.columns(2)
with col1:
    v_percent = st.number_input("训练速度 (%)", value=0.0, step=1.0, format="%.2f")
with col2:
    v_plus_percent = st.number_input("训练速度额外加成 (%)", value=0.0, step=1.0, format="%.1f")

# 每次数量和加速时长
col3, col4 = st.columns(2)
with col3:
    num = st.number_input("每次训练数量", value=1, min_value=1, step=1)
with col4:
    duration_days = st.number_input("加速时长 (天)", value=1.0, min_value=0.0, step=1.0, format="%.2f")

# 计算按钮
if st.button("🚀 计算", type="primary"):
    v = v_percent / 100.0
    v_plus = v_plus_percent / 100.0
    denominator = 1 + v + v_plus

    if denominator <= 0:
        st.error("速度加成之和 (1+v+v_plus) 必须大于 0！")
    else:
        if mode == "训练":
            time_total_sec = current_time_per_sec * num / denominator
            point_per_soldier = point_dict[level]
            label_unit = "训练"
        else:  # 晋升
            time_per_promotion = target_time - initial_time
            if time_per_promotion <= 0:
                st.error("目标等级必须高于初始等级，或训练时长设置有误！")
                # 不再执行后续计算
            else:
                time_total_sec = time_per_promotion * num / denominator
                point_per_soldier = point_dict[target_level] - point_dict[initial_level]
                if point_per_soldier < 0:
                    st.error("目标等级积分低于初始等级，请检查积分设置！")
                else:
                    label_unit = "晋升"
                    # 进行统一计算
                    duration_sec = duration_days * 24 * 3600
                    soldiers_done = (duration_sec / time_total_sec) * num
                    total_points = soldiers_done * point_per_soldier

                    st.subheader("📊 计算结果")
                    col_res1, col_res2, col_res3 = st.columns(3)
                    with col_res1:
                        st.metric(f"每次{label_unit}总时长", format_hms(time_total_sec))
                    with col_res2:
                        st.metric(f"加速时长内可{label_unit}士兵数", f"{soldiers_done:.2f} 名")
                    with col_res3:
                        st.metric(f"{label_unit}总积分", f"{total_points:.2f}")
