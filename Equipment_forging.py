import streamlit as st
import pandas as pd
import numpy as np

# 设置页面配置
st.set_page_config(
    page_title="装备锻造消耗计算器",
    page_icon="⚔️",
    layout="wide"
)

# 应用标题
st.title("⚔️ 装备锻造消耗计算器")
st.markdown("---")

# 初始化session_state
if 'forge_cost_table' not in st.session_state:
    # 默认消耗表 - 0-20级，每级消耗[锻造石, 金色装备]
    st.session_state.forge_cost_table = [
        [0, 0],   # 0级(占位)
        [5, 0],   # 1级
        [8, 0],   # 2级
        [12, 0],  # 3级
        [16, 0],  # 4级
        [20, 0],  # 5级
        [25, 1],  # 6级
        [30, 1],  # 7级
        [36, 1],  # 8级
        [42, 1],  # 9级
        [50, 1],  # 10级
        [60, 2],  # 11级
        [70, 2],  # 12级
        [80, 2],  # 13级
        [90, 2],  # 14级
        [100, 2], # 15级
        [120, 3], # 16级
        [140, 3], # 17级
        [160, 3], # 18级
        [180, 3], # 19级
        [200, 4]  # 20级
    ]

if 'equipment_types' not in st.session_state:
    st.session_state.equipment_types = ["头盔", "铠甲", "臂甲", "战靴"]

if 'selected_equipment' not in st.session_state:
    st.session_state.selected_equipment = ["头盔", "铠甲", "臂甲", "战靴"]

# 计算消耗的函数
def calculate_cost(current_level, target_level, equipment_count=1):
    """计算从当前等级升级到目标等级的总消耗"""
    if current_level >= target_level:
        return 0, 0
    
    total_stones = 0
    total_equipments = 0
    
    # 累加从当前等级到目标等级前一级的所有消耗
    for level in range(current_level + 1, target_level + 1):
        total_stones += st.session_state.forge_cost_table[level][0]
        total_equipments += st.session_state.forge_cost_table[level][1]
    
    # 乘以装备件数
    total_stones *= equipment_count
    total_equipments *= equipment_count
    
    return total_stones, total_equipments

# 在顶部添加两个模式选项
st.header("选择计算模式")

# 创建选项卡
tab1, tab2 = st.tabs(["🧮 计算锻造消耗", "📊 展示每级锻造消耗"])

with tab1:
    st.header("🧮 锻造消耗计算")
    
    # 选择装备部位
    st.subheader("选择装备部位")
    selected_types = st.multiselect(
        "选择要计算的装备部位:",
        options=st.session_state.equipment_types,
        default=st.session_state.selected_equipment,
        key="calc_equipment_select"
    )
    
    if selected_types:
        st.session_state.selected_equipment = selected_types
    
    # 装备数量
    equipment_count = st.number_input(
        "每类装备的件数:",
        min_value=1,
        max_value=100,
        value=1,
        help="每类装备需要锻造的件数",
        key="calc_equipment_count"
    )
    
    # 等级选择
    st.subheader("选择等级范围")
    
    col_level1, col_level2 = st.columns(2)
    with col_level1:
        current_level = st.slider(
            "当前等级:",
            min_value=0,
            max_value=19,
            value=0,
            help="装备的当前等级",
            key="calc_current_level"
        )
    
    with col_level2:
        target_level = st.slider(
            "目标等级:",
            min_value=1,
            max_value=20,
            value=10,
            help="希望达到的目标等级",
            key="calc_target_level"
        )
    
    if current_level >= target_level:
        st.warning("⚠️ 目标等级必须大于当前等级!")
    
    # 计算按钮
    if st.button("开始计算", type="primary", use_container_width=True, key="calc_button"):
        if current_level >= target_level:
            st.error("请调整等级设置：目标等级必须大于当前等级")
        else:
            # 计算总消耗
            results = []
            total_stones_all = 0
            total_equipments_all = 0
            
            for eq_type in st.session_state.selected_equipment:
                stones, equipments = calculate_cost(current_level, target_level, equipment_count)
                total_stones_all += stones
                total_equipments_all += equipments
                results.append({
                    "部位": eq_type,
                    "锻造石": stones,
                    "金色装备": equipments
                })
            
            # 保存结果到session_state
            st.session_state.calc_results = results
            st.session_state.calc_total_stones = total_stones_all
            st.session_state.calc_total_equipments = total_equipments_all
            st.session_state.calc_current_level = current_level
            st.session_state.calc_target_level = target_level
            st.session_state.calc_equipment_count = equipment_count
    
    # 显示计算结果
    if 'calc_results' in st.session_state:
        st.markdown("---")
        st.header("📋 计算结果")
        
        # 显示总体结果
        st.subheader(f"总体消耗 (从{st.session_state.calc_current_level}级到{st.session_state.calc_target_level}级)")
        
        col_total1, col_total2 = st.columns(2)
        with col_total1:
            st.metric(
                label="总锻造石消耗",
                value=f"{st.session_state.calc_total_stones}个",
                help=f"{len(st.session_state.selected_equipment)}个部位 × {st.session_state.calc_equipment_count}件 × 每件消耗"
            )
        
        with col_total2:
            st.metric(
                label="总金色装备消耗",
                value=f"{st.session_state.calc_total_equipments}件",
                help=f"{len(st.session_state.selected_equipment)}个部位 × {st.session_state.calc_equipment_count}件 × 每件消耗"
            )
        
        # 显示详细结果
        st.subheader("各部位详细消耗")
        
        results_df = pd.DataFrame(st.session_state.calc_results)
        st.dataframe(
            results_df,
            column_config={
                "部位": "装备部位",
                "锻造石": st.column_config.NumberColumn("锻造石消耗"),
                "金色装备": st.column_config.NumberColumn("金色装备消耗")
            },
            use_container_width=True,
            hide_index=True
        )
        
        # 可视化 - 各部位消耗对比
        st.subheader("消耗对比图")
        
        if not results_df.empty:
            # 创建对比图表
            chart_data = results_df.set_index("部位")
            
            chart_tab1, chart_tab2 = st.tabs(["📊 锻造石消耗", "🛡️ 金色装备消耗"])
            
            with chart_tab1:
                st.bar_chart(chart_data["锻造石"])
            
            with chart_tab2:
                st.bar_chart(chart_data["金色装备"])

with tab2:
    st.header("📊 每级锻造消耗展示")
    
    # 创建消耗数据表格
    st.subheader("各级锻造消耗数据表")
    
    # 准备数据框
    cost_data = []
    for level in range(1, 21):
        stones, equipments = st.session_state.forge_cost_table[level]
        cumulative_stones = sum(st.session_state.forge_cost_table[i][0] for i in range(1, level+1))
        cumulative_equipments = sum(st.session_state.forge_cost_table[i][1] for i in range(1, level+1))
        
        cost_data.append({
            "等级": level,
            "锻造石": stones,
            "金色装备": equipments,
            "累计锻造石": cumulative_stones,
            "累计金色装备": cumulative_equipments
        })
    
    df = pd.DataFrame(cost_data)
    
    # 显示数据表
    st.dataframe(
        df,
        column_config={
            "等级": st.column_config.NumberColumn("等级", disabled=True),
            "锻造石": st.column_config.NumberColumn("锻造石", min_value=0, step=1),
            "金色装备": st.column_config.NumberColumn("金色装备", min_value=0, step=1),
            "累计锻造石": st.column_config.NumberColumn("累计锻造石"),
            "累计金色装备": st.column_config.NumberColumn("累计金色装备")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # 数据编辑功能
    st.subheader("编辑消耗数据")
    
    edited_df = st.data_editor(
        df,
        column_config={
            "等级": st.column_config.NumberColumn("等级", disabled=True),
            "锻造石": st.column_config.NumberColumn("锻造石", min_value=0, step=1),
            "金色装备": st.column_config.NumberColumn("金色装备", min_value=0, step=1),
            "累计锻造石": st.column_config.NumberColumn("累计锻造石", disabled=True),
            "累计金色装备": st.column_config.NumberColumn("累计金色装备", disabled=True)
        },
        hide_index=True,
        use_container_width=True,
        key="data_editor"
    )
    
    # 保存按钮
    if st.button("保存修改的消耗数据", type="primary", key="save_button"):
        # 更新消耗表
        for _, row in edited_df.iterrows():
            level = int(row["等级"])
            stones = int(row["锻造石"])
            equipments = int(row["金色装备"])
            st.session_state.forge_cost_table[level] = [stones, equipments]
        
        st.success("消耗数据已保存!")
        st.rerun()
    
    # 可视化图表
    st.subheader("消耗趋势图")
    
    # 创建两个图表
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("**各级锻造石消耗趋势**")
        # 提取数据
        levels = list(range(1, 21))
        stones_per_level = [st.session_state.forge_cost_table[i][0] for i in range(1, 21)]
        cumulative_stones = [sum(st.session_state.forge_cost_table[j][0] for j in range(1, i+1)) for i in range(1, 21)]
        
        chart_data = pd.DataFrame({
            "等级": levels,
            "单级消耗": stones_per_level,
            "累计消耗": cumulative_stones
        }).set_index("等级")
        
        st.line_chart(chart_data)
    
    with chart_col2:
        st.markdown("**各级金色装备消耗趋势**")
        # 提取数据
        equipments_per_level = [st.session_state.forge_cost_table[i][1] for i in range(1, 21)]
        cumulative_equipments = [sum(st.session_state.forge_cost_table[j][1] for j in range(1, i+1)) for i in range(1, 21)]
        
        chart_data = pd.DataFrame({
            "等级": levels,
            "单级消耗": equipments_per_level,
            "累计消耗": cumulative_equipments
        }).set_index("等级")
        
        st.line_chart(chart_data)
    
    # 统计信息
    st.subheader("统计信息")
    
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    total_stones = sum(st.session_state.forge_cost_table[i][0] for i in range(1, 21))
    total_equipments = sum(st.session_state.forge_cost_table[i][1] for i in range(1, 21))
    
    max_stones_level = max(range(1, 21), key=lambda i: st.session_state.forge_cost_table[i][0])
    max_equipments_level = max(range(1, 21), key=lambda i: st.session_state.forge_cost_table[i][1])
    
    with stats_col1:
        st.metric("总锻造石消耗", f"{total_stones}个")
    
    with stats_col2:
        st.metric("总金色装备消耗", f"{total_equipments}件")
    
    with stats_col3:
        st.metric("最高单级锻造石消耗", 
                 f"{st.session_state.forge_cost_table[max_stones_level][0]}个",
                 f"{max_stones_level}级")

# 底部信息
st.markdown("---")
st.caption("装备锻造消耗计算器 v1.0 | 从0级到20级的锻造消耗计算")
