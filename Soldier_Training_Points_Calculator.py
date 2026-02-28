import streamlit as st
import pandas as pd

# 页面标题
st.title("士兵训练计算器 (秒/天版)")

st.markdown("""
本工具根据士兵等级、训练速度加成（百分比）和每次训练数量，计算：
- **每次训练所需总时长**（显示为 时:分:秒）
- 在给定的**加速时长**（单位：天）内，一共能训练多少士兵
""")

# 定义等级对应的单个士兵训练时间（单位：秒）
level_to_time_per_sec = {
    1: 5 * 60,     # 5分钟 = 300秒
    2: 10 * 60,    # 600秒
    3: 15 * 60,    # 900秒
    4: 20 * 60,    # 1200秒
    5: 25 * 60,    # 1500秒
    6: 30 * 60,    # 1800秒
    7: 35 * 60,    # 2100秒
    8: 40 * 60,    # 2400秒
    9: 45 * 60,    # 2700秒
    10: 50 * 60,   # 3000秒
    11: 55 * 60    # 3300秒
}

# 自定义等级显示文本
level_display_names = {
    1: "1级兵",
    2: "2级兵",
    3: "3级兵",
    4: "4级兵",
    5: "5级兵",
    6: "6级兵",
    7: "7级兵",
    8: "8级兵",
    9: "9级兵",
    10: "10级兵",
    11: "宫1兵"
}

# ------------------ 辅助函数：将秒数格式化为 时:分:秒 ------------------
def format_hms(seconds):
    """将秒数转换为 时:分:秒 格式（秒四舍五入取整）"""
    total_sec = int(round(seconds))
    hours = total_sec // 3600
    minutes = (total_sec % 3600) // 60
    secs = total_sec % 60
    return f"{hours}时{minutes}分{secs}秒"

# ------------------ 侧边栏：展示等级-时间对照表 ------------------
with st.sidebar:
    st.header("📋 士兵等级训练时长对照表")
    # 构建表格数据（只保留等级和秒数）
    table_data = []
    for lvl, sec in level_to_time_per_sec.items():
        table_data.append({
            "等级": level_display_names[lvl],
            "训练时长 (秒)": sec
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df.set_index("等级"), use_container_width=True)

# ------------------ 主页面：输入控件 ------------------
st.subheader("⚙️ 设置参数")

# 第一行：等级选择
level = st.selectbox(
    "选择士兵等级",
    options=list(level_to_time_per_sec.keys()),
    format_func=lambda x: level_display_names[x]
)
time_per_sec = level_to_time_per_sec[level]

# 第二行：训练速度加成（单位 %）
col1, col2 = st.columns(2)
with col1:
    v_percent = st.number_input("训练速度 v (%)", value=0.0, step=1.0, format="%.1f")
with col2:
    v_plus_percent = st.number_input("训练速度额外加成 v_plus (%)", value=0.0, step=1.0, format="%.1f")

# 第三行：每次训练数量和加速时长
col3, col4 = st.columns(2)
with col3:
    num = st.number_input("每次训练数量 num", value=1, min_value=1, step=1)
with col4:
    duration_days = st.number_input("加速时长 duration (天)", value=1.0, min_value=0.0, step=0.5, format="%.2f")

# 计算按钮
if st.button("🚀 计算", type="primary"):
    # 将百分比转换为小数
    v = v_percent / 100.0
    v_plus = v_plus_percent / 100.0
    denominator = 1 + v + v_plus

    if denominator <= 0:
        st.error("速度加成之和 (1+v+v_plus) 必须大于 0，请检查输入！")
    else:
        # 计算每次训练总时长（秒）
        time_total_sec = time_per_sec * num / denominator

        # 将加速时长从天转换为秒
        duration_sec = duration_days * 24 * 3600

        # 计算加速时长内可训练的士兵数量
        soldiers_trained = (duration_sec / time_total_sec) * num

        # 显示结果
        st.subheader("📊 计算结果")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            formatted_time = format_hms(time_total_sec)
            st.metric("每次训练总时长 (time_total)", formatted_time)
        with col_res2:
            st.metric("加速时长内可训练士兵数",
                      f"{soldiers_trained:.2f} 名")
