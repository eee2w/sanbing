import streamlit as st
import pandas as pd

st.title("最强爆兵积分计算器(更新到宫2)")
st.markdown("""  
支持"训练""晋升"两种模式  
点击左上角双箭头打开侧边栏即可查看不同等级士兵的训练时长与积分   
游戏中点击左上角头像下面的战力，即可在里面找到“兵营训练速度”
""")

# ---------- 统一数据管理 ----------
LEVEL_DATA = pd.DataFrame({
    "level": list(range(1, 14)),
    "name": ["1级兵", "2级兵", "3级兵", "4级兵", "5级兵",
             "6级兵", "7级兵", "8级兵", "9级兵", "10级兵",
             "宫1兵", "宫2兵","宫3兵"],
    "time_default": [11.5, 16.5, 23.5, 31.5, 42.5,
                     59.5, 82.5, 111.5, 129.5, 151.5,
                     166.0, 182.0, 200.0],
    "points": [90, 210, 180, 270, 390, 610, 840, 1150,
               1520, 2000, 2490, 3094, 3800]
}).set_index("level")

MAX_LEVEL = 13

# 辅助函数：秒转时:分:秒
def format_hms(seconds):
    total_sec = int(round(seconds))
    hours = total_sec // 3600
    minutes = (total_sec % 3600) // 60
    secs = total_sec % 60
    return f"{hours}时{minutes}分{secs}秒"

# 辅助函数：安全解析浮点数
def parse_float(val_str, default, label="数值"):
    try:
        return float(val_str) if val_str.strip() else default
    except ValueError:
        st.warning(f"{label}输入无效，已使用默认值 {default}")
        return default

# 辅助函数：安全解析正整数
def parse_positive_int(val_str, default, label="数值"):
    try:
        v = int(val_str) if val_str.strip() else default
        if v < 1:
            v = default
            st.warning(f"{label}不能小于1，已设为 {default}")
        return v
    except ValueError:
        st.warning(f"{label}输入无效，已使用默认值 {default}")
        return default

# ---------- 侧边栏：可编辑的训练时长 ----------
with st.sidebar:
    st.header("⚙️ 单个士兵训练时长")

    # 初始化 session_state 中的训练时长（如果尚未设置）
    for lvl in LEVEL_DATA.index:
        key = f"time_input_{lvl}"
        if key not in st.session_state:
            st.session_state[key] = LEVEL_DATA.loc[lvl, "time_default"]

    # 表头
    col_title1, col_title2, col_title3 = st.columns([1.2, 2, 1])
    with col_title1:
        st.markdown("**等级**")
    with col_title2:
        st.markdown("**训练时长 (秒)**")
    with col_title3:
        st.markdown("**积分**")

    # 每一行的输入框
    for lvl in LEVEL_DATA.index:
        cols = st.columns([1.2, 2, 1])
        with cols[0]:
            st.write(LEVEL_DATA.loc[lvl, "name"])
        with cols[1]:
            st.number_input(
                "秒",
                value=st.session_state[f"time_input_{lvl}"],
                min_value=0.1,
                step=0.1,
                format="%.1f",
                key=f"time_input_{lvl}",
                label_visibility="collapsed"
            )
        with cols[2]:
            st.write(f"**{LEVEL_DATA.loc[lvl, 'points']}**")

# ---------- 主页面 ----------
st.subheader("⚙️ 设置参数")

# 模式选择
mode = st.radio("选择功能", ["训练", "晋升"], horizontal=True, index=0)

# 根据模式显示等级选择
if mode == "训练":
    level = st.selectbox(
        "选择士兵等级",
        options=list(LEVEL_DATA.index),
        format_func=lambda x: LEVEL_DATA.loc[x, "name"]
    )
    initial_level = None   # 标记为训练模式
else:
    col_initial, col_target = st.columns(2)
    with col_initial:
        # 初始等级不能是最大等级
        initial_level = st.selectbox(
            "初始等级",
            options=list(range(1, MAX_LEVEL)),  # 1~11
            format_func=lambda x: LEVEL_DATA.loc[x, "name"],
            key="initial_level"
        )
    with col_target:
        # 目标等级自动限制为大于初始等级
        target_options = list(range(initial_level + 1, MAX_LEVEL + 1))
        target_level = st.selectbox(
            "目标等级",
            options=target_options,
            format_func=lambda x: LEVEL_DATA.loc[x, "name"],
            key="target_level"
        )

# 输入参数：训练速度、额外加成、数量、加速时长
col1, col2 = st.columns(2)
with col1:
    v_percent_str = st.text_input("训练速度 (%)", value="", placeholder="0.0", key="v_percent")
with col2:
    v_plus_percent_str = st.text_input("单兵种额外加成(%)(包括武将加成和兵机阁/议政堂)", value="", placeholder="0.0", key="v_plus")

col3, col4 = st.columns(2)
with col3:
    num_str = st.text_input("单次训练数量", value="", placeholder="1", key="num")
with col4:
    duration_days_str = st.text_input("加速时长 (天)", value="", placeholder="1.0", key="duration")

# 计算按钮
if st.button("🚀 计算", type="primary"):
    # 解析输入
    v_percent = parse_float(v_percent_str, 0.0, "训练速度")
    v_plus_percent = parse_float(v_plus_percent_str, 0.0, "额外加成")
    num = parse_positive_int(num_str, 1, "每次训练数量")
    duration_days = parse_float(duration_days_str, 1.0, "加速时长")
    if duration_days < 0:
        duration_days = 0.0
        st.warning("加速时长不能为负，已设为0")

    # 速度分母
    denominator = 1 + v_percent / 100.0 + v_plus_percent / 100.0
    if denominator <= 0:
        st.error("速度加成之和 (1+v+v_plus) 必须大于 0，请检查输入！")
        st.stop()

    # 根据模式计算
    if mode == "训练":
        time_per_unit = st.session_state[f"time_input_{level}"] / denominator
        points_per_unit = LEVEL_DATA.loc[level, "points"]
        label_unit = "训练"
    else:
        # 晋升模式：时间差 = 目标时长 - 初始时长
        time_diff = st.session_state[f"time_input_{target_level}"] - st.session_state[f"time_input_{initial_level}"]
        if time_diff <= 0:
            st.error("目标等级训练时长必须大于初始等级，请检查侧边栏设置！")
            st.stop()
        time_per_unit = time_diff / denominator
        points_per_unit = LEVEL_DATA.loc[target_level, "points"] - LEVEL_DATA.loc[initial_level, "points"]
        if points_per_unit < 0:
            st.error("目标等级积分低于初始等级，请检查积分数据！")
            st.stop()
        label_unit = "晋升"

    # 总耗时（一次操作）
    total_time_sec = time_per_unit * num

    # 加速时长内可完成的士兵数
    duration_sec = duration_days * 24 * 3600
    soldiers_done = (duration_sec / total_time_sec) * num
    total_points = soldiers_done * points_per_unit

    # 显示结果
    st.subheader("📊 计算结果")
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric(f"每次{label_unit}总时长", format_hms(total_time_sec))
    with col_res2:
        st.metric(f"消耗加速可{label_unit}士兵数", f"{soldiers_done:.2f} 名")
    with col_res3:
        st.metric(f"{label_unit}总积分", f"{total_points:.2f}")
