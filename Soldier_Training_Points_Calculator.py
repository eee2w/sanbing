import streamlit as st
import pandas as pd

# 注入JavaScript（自动全选，可选保留）
st.markdown("""
<script>
document.addEventListener('focus', function(e) {
    if (e.target && e.target.matches && e.target.matches('input[type=number]')) {
        e.target.select();
    }
}, true);
</script>
""", unsafe_allow_html=True)

st.title("最强爆兵积分计算器")
st.markdown("""
支持"训练""晋升"两种模式： 
游戏中点击左上角头像下面的战力，即可在里面找到“兵营训练速度”
""")

# ---------- 预设数据 ----------
# ...（此处保持 default_time_per_sec, point_dict, level_display_names, MAX_LEVEL 不变）
# 略...

# ---------- 辅助函数：秒转时:分:秒 ----------
def format_hms(seconds):
    total_sec = int(round(seconds))
    hours = total_sec // 3600
    minutes = (total_sec % 3600) // 60
    secs = total_sec % 60
    return f"{hours}时{minutes}分{secs}秒"

# ---------- 侧边栏：可编辑的训练时长与积分 ----------
# ...（侧边栏保持原样，使用 st.number_input 方便微调）
# 略...

# ---------- 主页面：模式选择与输入控件 ----------
st.subheader("⚙️ 设置参数")
mode = st.radio("选择功能", ["训练", "晋升"], horizontal=True, index=0)

# 等级选择（与之前相同）
if mode == "训练":
    level = st.selectbox(
        "选择士兵等级",
        options=list(range(1, MAX_LEVEL + 1)),
        format_func=lambda x: level_display_names[x]
    )
    current_time_per_sec = st.session_state[f"time_input_{level}"]
    initial_level = None
else:
    col_initial, col_target = st.columns(2)
    with col_initial:
        initial_level = st.selectbox(
            "初始等级",
            options=list(range(1, MAX_LEVEL)),
            format_func=lambda x: level_display_names[x],
            key="initial_level"
        )
    with col_target:
        target_level = st.selectbox(
            "目标等级",
            options=list(range(initial_level + 1, MAX_LEVEL + 1)),
            format_func=lambda x: level_display_names[x],
            key="target_level"
        )
    initial_time = st.session_state[f"time_input_{initial_level}"]
    target_time = st.session_state[f"time_input_{target_level}"]

# ---------- 改用文本输入框，模仿资源包数量填写方式 ----------
col1, col2 = st.columns(2)
with col1:
    v_percent_str = st.text_input(
        "训练速度 (%)",
        value="",                # 初始为空
        placeholder="0.0",       # 提示默认值
        key="v_percent_input"
    )
with col2:
    v_plus_percent_str = st.text_input(
        "训练速度额外加成 (%)",
        value="",
        placeholder="0.0",
        key="v_plus_percent_input"
    )

col3, col4 = st.columns(2)
with col3:
    num_str = st.text_input(
        "每次训练数量",
        value="",
        placeholder="1",
        key="num_input"
    )
with col4:
    duration_days_str = st.text_input(
        "加速时长 (天)",
        value="",
        placeholder="1.0",
        key="duration_days_input"
    )

# 计算按钮
if st.button("🚀 计算", type="primary"):
    # ---------- 解析并验证输入 ----------
    # 训练速度
    try:
        v_percent = float(v_percent_str) if v_percent_str.strip() else 0.0
    except ValueError:
        v_percent = 0.0
        st.warning("训练速度输入无效，已使用0%")

    # 速度额外加成
    try:
        v_plus_percent = float(v_plus_percent_str) if v_plus_percent_str.strip() else 0.0
    except ValueError:
        v_plus_percent = 0.0
        st.warning("训练速度额外加成输入无效，已使用0%")

    # 每次训练数量（必须为正整数）
    try:
        num = int(num_str) if num_str.strip() else 1
        if num < 1:
            num = 1
            st.warning("每次训练数量不能小于1，已设为1")
    except ValueError:
        num = 1
        st.warning("每次训练数量输入无效，已使用1")

    # 加速时长（必须非负）
    try:
        duration_days = float(duration_days_str) if duration_days_str.strip() else 1.0
        if duration_days < 0:
            duration_days = 0.0
            st.warning("加速时长不能为负，已设为0")
    except ValueError:
        duration_days = 1.0
        st.warning("加速时长输入无效，已使用1天")

    # ---------- 核心计算 ----------
    v = v_percent / 100.0
    v_plus = v_plus_percent / 100.0
    denominator = 1 + v + v_plus

    if denominator <= 0:
        st.error("速度加成之和 (1+v+v_plus) 必须大于 0，请检查输入！")
    else:
        if mode == "训练":
            time_total_sec = current_time_per_sec * num / denominator
            point_per_soldier = point_dict[level]
            label_unit = "训练"
        else:  # 晋升
            time_per_promotion = target_time - initial_time
            if time_per_promotion <= 0:
                st.error("目标等级必须高于初始等级！")
                st.stop()
            time_total_sec = time_per_promotion * num / denominator
            point_per_soldier = point_dict[target_level] - point_dict[initial_level]
            if point_per_soldier < 0:
                st.error("目标等级积分低于初始等级，请检查积分设置！")
                st.stop()
            label_unit = "晋升"

        duration_sec = duration_days * 24 * 3600
        soldiers_done = (duration_sec / time_total_sec) * num
        total_points = soldiers_done * point_per_soldier

        st.subheader("📊 计算结果")
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            formatted_time = format_hms(time_total_sec)
            st.metric(f"每次{label_unit}总时长", formatted_time)
        with col_res2:
            st.metric(f"加速时长内可{label_unit}士兵数", f"{soldiers_done:.2f} 名")
        with col_res3:
            st.metric(f"{label_unit}总积分", f"{total_points:.2f}")
