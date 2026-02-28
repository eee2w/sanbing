import streamlit as st

# 页面标题
st.title("士兵训练计算器")

# 说明文字
st.markdown("""
本工具根据士兵等级、训练速度加成和每次训练数量，计算：
- **每次训练所需总时长**（`time_total`）
- 在给定的**加速时长**内，一共能训练多少士兵
""")

# 定义等级对应的单个士兵训练时间（单位：分钟，可自行调整）
level_to_time_per = {
    1: 5,
    2: 10,
    3: 15,
    4: 20,
    5: 25,
    6: 30,
    7: 35,
    8: 40,
    9: 45,
    10: 50,
    11: 55
}

# 侧边栏输入（也可以放在主区域，这里选择侧边栏以保持界面简洁）
with st.sidebar:
    st.header("输入参数")
    # 选择士兵等级
    level = st.selectbox("选择士兵等级 (1-11)", options=list(level_to_time_per.keys()), format_func=lambda x: f"等级 {x}")
    # 显示该等级对应的基础训练时间
    time_per = level_to_time_per[level]
    st.info(f"等级 {level} 的单个士兵训练时间: **{time_per} 分钟**")

    # 其他输入
    v = st.number_input("训练速度 v (例如 0.1 表示 +10%)", value=0.0, step=0.01, format="%.2f")
    v_plus = st.number_input("训练速度额外加成 v_plus", value=0.0, step=0.01, format="%.2f")
    num = st.number_input("每次训练数量 num", value=1, min_value=1, step=1)
    duration = st.number_input("加速时长 duration (分钟)", value=60.0, min_value=0.0, step=1.0)

# 计算主体
if st.button("计算", type="primary"):
    # 检查分母是否为零
    denominator = 1 + v + v_plus
    if denominator <= 0:
        st.error("速度加成之和 (1+v+v_plus) 必须大于 0，请检查输入！")
    else:
        # 计算每次训练总时长
        time_total = time_per * num / denominator
        # 计算加速时长内可训练的士兵数量
        # 注意：duration / time_total 是训练次数，乘以 num 得到士兵数量
        soldiers_trained = (duration / time_total) * num

        # 显示结果
        st.subheader("计算结果")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("每次训练总时长 (time_total)", f"{time_total:.2f} 分钟")
        with col2:
            st.metric("加速时长内可训练士兵数", f"{soldiers_trained:.2f} 名")

        # 额外说明
        st.caption("注：士兵数量为理论值（可包含小数），实际游戏中可能需要向下取整。")
        st.caption(f"公式：time_total = {time_per} × {num} / (1 + {v} + {v_plus}) = {time_total:.2f}")
