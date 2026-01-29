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
    # 根据新规则动态生成消耗表 - 0-20级，每级消耗[锻造石, 金色装备]
    # 规则：
    # 1. 锻造石消耗：第1级50，后面每级增加50
    # 2. 金色装备消耗：10级升11级消耗1件，后面每级增加1件
    st.session_state.forge_cost_table = [[0, 0]]  # 0级占位
    
    for level in range(1, 21):
        # 锻造石消耗：50 * level
        stones = 50 * level
        
        # 金色装备消耗：level>10时，消耗(level-10)件
        golden_equipments = max(0, level - 10)
        
        st.session_state.forge_cost_table.append([stones, golden_equipments])

if 'equipment_types' not in st.session_state:
    st.session_state.equipment_types = ["头盔", "铠甲", "臂甲", "战靴"]

# 初始化装备计算列表，所有值都设为0或最小值
if 'equipment_calculations' not in st.session_state:
    st.session_state.equipment_calculations = [{"部位": "头盔", "当前等级": 0, "目标等级": 0}]

# 专武升级消耗函数
def calculate_exclusive_weapon_cost(current_level, target_level):
    """计算专武从当前等级升级到目标等级的总消耗"""
    if current_level >= target_level:
        return 0
    
    total_fragments = 0
    
    # 从当前等级+1到目标等级，每级消耗增加50
    for level in range(current_level + 1, target_level + 1):
        # 第n级需要消耗50*n个碎片
        total_fragments += 50 * level
    
    return total_fragments

# 装备锻造消耗函数
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

# 在顶部添加计算模式选项
st.header("选择计算模式")

# 创建选项卡
tab1, tab2, tab3 = st.tabs(["🧮 计算锻造消耗", "📊 展示每级锻造消耗", "🗡️ 专武升级"])

with tab1:
    st.header("🧮 锻造消耗计算")
    
    # 动态生成装备计算条目
    st.subheader("装备设置")
    
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
                index=equipment["当前等级"],  # 默认为0
                key=f"current_{i}"
            )
        
        with col3:
            equipment["目标等级"] = st.selectbox(
                f"目标等级 {i+1}",
                options=list(range(0, 21)),  # 0-20
                index=equipment["目标等级"],  # 默认为0
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
    
    # 添加装备的按钮（放在最下面）
    col_add, _ = st.columns([1, 5])
    with col_add:
        if st.button("➕ 添加装备", type="secondary"):
            # 新添加的装备也设为默认值0
            st.session_state.equipment_calculations.append({"部位": "头盔", "当前等级": 0, "目标等级": 0})
            st.rerun()
    
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
    
    # 显示当前消耗规则
    st.markdown("""
    ### 当前锻造消耗规则
    - **锻造石消耗**：第1级50个，后面每级增加50个
    - **金色装备消耗**：10级升11级消耗1件，后面每级增加1件
    """)
    
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

with tab3:
    st.header("🗡️ 专武升级")
    
    # 专武升级说明
    st.markdown("""
    ### 专武升级规则
    - 专武等级范围：0级到10级
    - 升级消耗材料：专武碎片
    - 消耗规则：从n级升到n+1级需要消耗50×(n+1)个碎片
    - 例如：0级升1级需要50碎片，1级升2级需要100碎片，以此类推
    """)
    
    # 专武等级选择
    st.subheader("专武等级设置")
    
    col_weapon1, col_weapon2 = st.columns(2)
    
    with col_weapon1:
        exclusive_current_level = st.selectbox(
            "当前等级",
            options=list(range(0, 11)),  # 0-10
            index=0,  # 默认为0
            key="exclusive_current"
        )
    
    with col_weapon2:
        exclusive_target_level = st.selectbox(
            "目标等级",
            options=list(range(0, 11)),  # 0-10
            index=0,  # 默认为0
            key="exclusive_target"
        )
    
    # 计算专武升级消耗
    if st.button("计算专武升级消耗", type="primary", use_container_width=True):
        if exclusive_current_level >= exclusive_target_level:
            st.error("目标等级必须大于当前等级!")
        else:
            # 计算总消耗
            total_fragments = calculate_exclusive_weapon_cost(
                exclusive_current_level, 
                exclusive_target_level
            )
            
            # 保存结果到session_state
            st.session_state.exclusive_total_fragments = total_fragments
            st.session_state.exclusive_current = exclusive_current_level
            st.session_state.exclusive_target = exclusive_target_level
    
    # 显示专武升级计算结果
    if 'exclusive_total_fragments' in st.session_state:
        st.markdown("---")
        st.header("📋 专武升级计算结果")
        
        # 显示总消耗
        st.subheader(f"专武升级消耗 ({st.session_state.exclusive_current}级 → {st.session_state.exclusive_target}级)")
        
        st.metric(
            label="总专武碎片消耗",
            value=f"{st.session_state.exclusive_total_fragments}个"
        )
        
        # 显示各级消耗详情
        st.subheader("各级消耗详情")
        
        detail_data = []
        for level in range(st.session_state.exclusive_current + 1, st.session_state.exclusive_target + 1):
            fragments_needed = 50 * level
            detail_data.append({
                "升级区间": f"{level-1} → {level}",
                "所需碎片": fragments_needed
            })
        
        detail_df = pd.DataFrame(detail_data)
        st.dataframe(
            detail_df,
            column_config={
                "升级区间": "升级区间",
                "所需碎片": st.column_config.NumberColumn("所需碎片")
            },
            use_container_width=True,
            hide_index=True
        )
        
        # 显示累计消耗图
        st.subheader("累计消耗趋势")
        
        cumulative_data = []
        cumulative_fragments = 0
        for level in range(st.session_state.exclusive_current + 1, st.session_state.exclusive_target + 1):
            fragments_needed = 50 * level
            cumulative_fragments += fragments_needed
            cumulative_data.append({
                "等级": level,
                "单级消耗": fragments_needed,
                "累计消耗": cumulative_fragments
            })
        
        if cumulative_data:
            cumulative_df = pd.DataFrame(cumulative_data).set_index("等级")
            st.line_chart(cumulative_df[["单级消耗", "累计消耗"]])

# 底部信息
st.markdown("---")
st.caption("装备锻造消耗计算器 v1.1 | 支持装备锻造和专武升级计算")
