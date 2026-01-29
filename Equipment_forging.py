import streamlit as st
import pandas as pd

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

if 'equipment_calculations' not in st.session_state:
    st.session_state.equipment_calculations = [{"部位": "头盔", "当前等级": 0, "目标等级": 10}]

# 计算消耗的函数
def calculate_cost(current_level, target_level):
    """计算从当前等级升级到目标等级的总消耗"""
    if current_level >= target_level:
        return 0, 0
    
    total_stones = 0
    total_equipments = 0
    
    # 累加从当前等级到目标等级前一级的所有消耗
    for level in range(current_level + 1, target_level + 1):
        total_stones += st.session_state.forge_cost_table[level][0]
        total_equipments += st.session_state.forge_cost_table[level][1]
    
    return total_stones, total_equipments

# 在顶部添加两个模式选项
st.header("选择计算模式")

# 创建选项卡
tab1, tab2 = st.tabs(["🧮 计算锻造消耗", "📊 展示每级锻造消耗"])

with tab1:
    st.header("🧮 锻造消耗计算")
    
    # 动态生成装备计算条目
    st.subheader("装备设置")
    
    # 添加装备的按钮
    if st.button("➕ 添加装备", type="secondary"):
        st.session_state.equipment_calculations.append({"部位": "头盔", "当前等级": 0, "目标等级": 10})
        st.rerun()
    
    # 显示所有装备计算条目
    for i, equipment in enumerate(st.session_state.equipment_calculations):
        st.markdown(f"### 装备 {i+1}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            equipment["部位"] = st.selectbox(
                f"选择部位 {i+1}",
                options=st.session_state.equipment_types,
                index=st.session_state.equipment_types.index(equipment["部位"]),
                key=f"equipment_{i}"
            )
        
        with col2:
            equipment["当前等级"] = st.selectbox(
                f"当前等级 {i+1}",
                options=list(range(0, 20)),  # 0-19
                index=equipment["当前等级"],
                key=f"current_{i}"
            )
        
        with col3:
            equipment["目标等级"] = st.selectbox(
                f"目标等级 {i+1}",
                options=list(range(1, 21)),  # 1-20
                index=equipment["目标等级"]-1 if equipment["目标等级"] > 0 else 9,
                key=f"target_{i}"
            )
        
        # 删除按钮
        col_del, _ = st.columns([1, 5])
        with col_del:
            if st.button(f"🗑️ 删除装备 {i+1}", key=f"delete_{i}"):
                if len(st.session_state.equipment_calculations) > 1:
                    st.session_state.equipment_calculations.pop(i)
                    st.rerun()
        
        st.markdown("---")
    
    # 计算按钮
    if st.button("开始计算", type="primary", use_container_width=True):
        # 检查所有装备的有效性
        valid = True
        for i, equipment in enumerate(st.session_state.equipment_calculations):
            if equipment["当前等级"] >= equipment["目标等级"]:
                st.error(f"装备 {i+1}: 目标等级必须大于当前等级!")
                valid = False
        
        if valid:
            # 计算所有装备的消耗
            results = []
            total_stones_all = 0
            total_equipments_all = 0
            
            for i, equipment in enumerate(st.session_state.equipment_calculations):
                stones, equipments = calculate_cost(
                    equipment["当前等级"], 
                    equipment["目标等级"]
                )
                
                total_stones_all += stones
                total_equipments_all += equipments
                
                results.append({
                    "序号": i+1,
                    "部位": equipment["部位"],
                    "当前等级": equipment["当前等级"],
                    "目标等级": equipment["目标等级"],
                    "锻造石": stones,
                    "金色装备": equipments
                })
            
            # 保存结果到session_state
            st.session_state.calc_results = results
            st.session_state.calc_total_stones = total_stones_all
            st.session_state.calc_total_equipments = total_equipments_all
    
    # 显示计算结果
    if 'calc_results' in st.session_state:
        st.markdown("---")
        st.header("📋 计算结果")
        
        # 显示总体结果
        st.subheader(f"总体消耗 (共{len(st.session_state.equipment_calculations)}个装备)")
        
        col_total1, col_total2 = st.columns(2)
        with col_total1:
            st.metric(
                label="总锻造石消耗",
                value=f"{st.session_state.calc_total_stones}个"
            )
        
        with col_total2:
            st.metric(
                label="总金色装备消耗",
                value=f"{st.session_state.calc_total_equipments}件"
            )
        
        # 显示详细结果
        st.subheader("各装备详细消耗")
        
        results_df = pd.DataFrame(st.session_state.calc_results)
        st.dataframe(
            results_df,
            column_config={
                "序号": "序号",
                "部位": "装备部位",
                "当前等级": "当前等级",
                "目标等级": "目标等级",
                "锻造石": st.column_config.NumberColumn("锻造石消耗"),
                "金色装备": st.column_config.NumberColumn("金色装备消耗")
            },
            use_container_width=True,
            hide_index=True
        )

with tab2:
    st.header("📊 每级锻造消耗展示")
    
    # 准备数据框
    cost_data = []
    for level in range(1, 21):
        stones, equipments = st.session_state.forge_cost_table[level]
        
        cost_data.append({
            "等级": level,
            "锻造石": stones,
            "金色装备": equipments
        })
    
    df = pd.DataFrame(cost_data)
    
    # 显示数据表
    st.dataframe(
        df,
        column_config={
            "等级": st.column_config.NumberColumn("等级"),
            "锻造石": st.column_config.NumberColumn("锻造石"),
            "金色装备": st.column_config.NumberColumn("金色装备")
        },
        hide_index=True,
        use_container_width=True
    )

# 底部信息
st.markdown("---")
st.caption("装备锻造消耗计算器 v1.0")
