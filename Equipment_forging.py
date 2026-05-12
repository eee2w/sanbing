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
st.info(
    """
    锻造顺序推荐：只做步骑弓各一套装备，其他金装不要强化和锻造  
    1、步头甲8  弓臂鞋8  
    2、步臂鞋4  弓头甲4  
    3、步头甲12  弓臂鞋12  
    4、步臂鞋 8  骑臂鞋8 骑头甲4  
    5、步头甲16  弓臂鞋16
    """
)

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

# 专武升级消耗函数 - 修正后的逻辑：升级消耗基于总升级次数
def calculate_exclusive_weapon_cost(current_level, target_level):
    """计算专武从当前等级升级到目标等级的总消耗 - 修正版 (仅用于原始0-10级)"""
    if current_level >= target_level:
        return 0
    
    total_fragments = 0
    
    # 修正：第n次升级消耗50*n，从1开始计数
    # 从当前等级到目标等级，每次升级消耗递增
    for level in range(current_level + 1, target_level + 1):
        # 第level次升级消耗：50 * level
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
    
    # 定义扩展的等级列表（0-10级 + 红5级到红10级）
    extended_levels = [str(i) for i in range(11)] + [f"红{i}" for i in range(5, 11)]
    
    # 初始化红级升级所需碎片的配置（6个区间：10->红5, 红5->红6, ..., 红9->红10）
    if "red_upgrade_costs" not in st.session_state:
        # 默认值按递增方式设置，用户可自行修改
        st.session_state.red_upgrade_costs = [500, 600, 700, 800, 900, 1000]
    
    # 创建6个数字输入框让用户自定义每个红级升级区间的碎片消耗
    st.subheader("⚙️ 红色等级升级消耗配置（10级 → 红10级）")
    st.markdown("请为以下每个升级区间设置所需的专武碎片数量：")
    
    # 定义区间名称
    red_intervals = [
        "10级 → 红5级",
        "红5级 → 红6级",
        "红6级 → 红7级",
        "红7级 → 红8级",
        "红8级 → 红9级",
        "红9级 → 红10级"
    ]
    
    # 使用列布局方便输入
    cols = st.columns(3)
    updated_costs = []
    for i, interval in enumerate(red_intervals):
        col = cols[i % 3]
        with col:
            cost = st.number_input(
                f"{interval} 所需碎片",
                min_value=1,
                step=50,
                value=st.session_state.red_upgrade_costs[i],
                key=f"red_cost_{i}"
            )
            updated_costs.append(cost)
    
    # 如果用户修改了任何输入，更新session_state中的配置
    if updated_costs != st.session_state.red_upgrade_costs:
        st.session_state.red_upgrade_costs = updated_costs
    
    # 显示升级规则说明
    st.markdown("""
    ### 专武升级规则
    - **普通等级（0级 → 10级）**：第1级消耗50碎片，后续每级增加50碎片（固定规则，不可修改）
    - **红色等级（10级 → 红10级）**：每个升级区间的消耗由上方自定义配置决定
    """)
    
    # 专武等级选择
    st.subheader("专武等级设置")
    
    col_weapon1, col_weapon2 = st.columns(2)
    
    with col_weapon1:
        # 获取当前等级显示的索引，默认显示'0'
        current_level_idx = st.selectbox(
            "当前等级",
            options=range(len(extended_levels)),
            format_func=lambda x: extended_levels[x],
            index=0,
            key="exclusive_weapon_current_idx"
        )
        exclusive_current_level = extended_levels[current_level_idx]
    
    with col_weapon2:
        # 获取目标等级显示的索引，默认显示'0'
        target_level_idx = st.selectbox(
            "目标等级",
            options=range(len(extended_levels)),
            format_func=lambda x: extended_levels[x],
            index=0,
            key="exclusive_weapon_target_idx"
        )
        exclusive_target_level = extended_levels[target_level_idx]
    
    # 计算专武升级消耗（内部函数，处理扩展等级和自定义红级消耗）
    def calculate_exclusive_weapon_extended(current_idx, target_idx, red_costs):
        """计算从当前等级索引到目标等级索引的总消耗"""
        if current_idx >= target_idx:
            return 0, []  # 消耗为0，且无详细步骤
        
        total_fragments = 0
        step_details = []  # 每个升级区间的详细信息
        
        # 构建每一步的消耗列表
        # 步骤索引 i 表示从 extended_levels[i] 升级到 extended_levels[i+1]
        # 前10步（0-9）：对应普通等级升级（0→1, 1→2, ..., 9→10），消耗 = 50 * (i+1)
        # 后6步（10-15）：对应红色等级升级，消耗 = 用户配置的 red_costs[0]...red_costs[5]
        for step_idx in range(current_idx, target_idx):
            if step_idx < 10:  # 普通等级升级步骤
                # 第 step_idx 次升级（从0开始），消耗 = 50 * (step_idx + 1)
                cost = 50 * (step_idx + 1)
                from_level = extended_levels[step_idx]
                to_level = extended_levels[step_idx + 1]
                step_details.append({
                    "升级区间": f"{from_level} → {to_level}",
                    "所需碎片": cost,
                    "说明": f"第{step_idx+1}次升级（固定规则）"
                })
            else:  # 红色等级升级步骤 (step_idx 10~15)
                # 计算红色区间的索引 (0~5)
                red_idx = step_idx - 10
                if red_idx < len(red_costs):
                    cost = red_costs[red_idx]
                    from_level = extended_levels[step_idx]
                    to_level = extended_levels[step_idx + 1]
                    step_details.append({
                        "升级区间": f"{from_level} → {to_level}",
                        "所需碎片": cost,
                        "说明": f"红色等级升级（用户自定义）"
                    })
                else:
                    # 理论上不会发生，因为红色等级只有6步
                    cost = 0
                    step_details.append({
                        "升级区间": f"{extended_levels[step_idx]} → {extended_levels[step_idx+1]}",
                        "所需碎片": 0,
                        "说明": "未配置"
                    })
            total_fragments += cost
        
        return total_fragments, step_details
    
    # 计算按钮
    if st.button("计算专武升级消耗", type="primary", use_container_width=True):
        # 获取等级索引
        current_idx = extended_levels.index(exclusive_current_level)
        target_idx = extended_levels.index(exclusive_target_level)
        
        if current_idx >= target_idx:
            st.error("目标等级必须大于当前等级！")
        else:
            # 计算总消耗和详细步骤
            total_fragments, detail_data = calculate_exclusive_weapon_extended(
                current_idx, target_idx, st.session_state.red_upgrade_costs
            )
            
            # 保存结果到session_state
            st.session_state.weapon_calc_total_fragments = total_fragments
            st.session_state.weapon_current_level = exclusive_current_level
            st.session_state.weapon_target_level = exclusive_target_level
            st.session_state.weapon_detail_data = detail_data
    
    # 显示专武升级计算结果
    if 'weapon_calc_total_fragments' in st.session_state:
        st.markdown("---")
        st.header("📋 专武升级计算结果")
        
        # 显示总消耗
        st.subheader(f"专武升级消耗 ({st.session_state.weapon_current_level}级 → {st.session_state.weapon_target_level}级)")
        
        st.metric(
            label="总专武碎片消耗",
            value=f"{st.session_state.weapon_calc_total_fragments}个"
        )
        
        # 显示各级消耗详情
        if st.session_state.weapon_detail_data:
            st.subheader("各级消耗详情")
            
            detail_df = pd.DataFrame(st.session_state.weapon_detail_data)
            st.dataframe(
                detail_df,
                column_config={
                    "升级区间": "升级区间",
                    "所需碎片": st.column_config.NumberColumn("所需碎片"),
                    "说明": "说明"
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("没有升级步骤需要消耗（当前等级与目标等级相同）")

# 底部信息
st.markdown("---")
st.caption("装备锻造消耗计算器 v1.4 | 支持装备锻造和专武升级计算（包含红色等级，可自定义红级消耗）")
