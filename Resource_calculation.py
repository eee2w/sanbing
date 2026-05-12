import streamlit as st

# 设置页面标题和布局
st.set_page_config(
    page_title="游戏资源计算器",
    page_icon="🎮",
    layout="centered"
)

# 应用标题
st.title("🎮 游戏资源计算器")
st.info(
    """
    1、打开包裹点击右下角“统计”可以看到当前资源总量  
    2、包裹第一页最上面为三个资源自选包  
    """
)
st.markdown("---")

# 已有资源部分
st.subheader("📦 已有资源")

# 创建每行资源的布局函数
def create_resource_input(label):
    col_num, col_unit = st.columns([4, 1])
    with col_num:
        # 使用text_input而不是number_input，允许空值
        num_str = st.text_input(
            f"{label}数量",
            value="",  # 空值
            placeholder="请输入",
            key=f"{label}_num"
        )
    with col_unit:
        st.markdown('<div style="margin-top: 28px;"></div>', unsafe_allow_html=True)  # 垂直对齐
        unit = st.selectbox(
            "单位",
            ["万", "亿"],
            index=1,  # 默认选中“亿”（索引1）
            key=f"{label}_unit",
            label_visibility="collapsed"
        )
    
    # 将输入转换为浮点数，如果为空则返回0
    try:
        num = float(num_str) if num_str else 0.0
    except ValueError:
        num = 0.0
    
    return num, unit

# 输入每种资源
meat_num, meat_unit = create_resource_input("肉")
wood_num, wood_unit = create_resource_input("木")
coal_num, coal_unit = create_resource_input("煤")
iron_num, iron_unit = create_resource_input("铁")

st.markdown("---")

# 资源包数量部分
st.subheader("🎁 资源包数量")

# 创建资源包数量输入函数
def create_pack_input(label, description):
    col_label, col_input = st.columns([3, 1])
    with col_label:
        st.markdown(f"**{label}**")
        st.caption(description)
    with col_input:
        # 使用text_input，允许空值
        pack_str = st.text_input(
            label,
            value="",
            placeholder="0",
            key=f"{label}_input",
            label_visibility="collapsed"
        )
    
    # 将输入转换为整数，如果为空则返回0
    try:
        pack_value = int(pack_str) if pack_str else 0
    except ValueError:
        pack_value = 0
    
    return pack_value

# 输入资源包数量
pack_1w = create_pack_input("1w资源包数量", "每个1万资源")
pack_10w = create_pack_input("10w资源包数量", "每个10万资源")
pack_100w = create_pack_input("100w资源包数量", "每个100万资源")

st.markdown("---")

# 策略选择
st.subheader("⚙️ 补充策略选择")
strategy = st.radio(
    "请选择资源包使用策略：",
    ["按比例补充（尽量满足4:4:2:1的比例）", "按顺序补充（按照肉→木→煤→铁的顺序补充）"],
    horizontal=True
)

# 计算按钮
st.markdown("---")
calculate_button = st.button("🚀 开始计算", type="primary", use_container_width=True)

def convert_to_wan(value, unit):
    """将值转换为万单位"""
    if unit == "亿":
        return value * 10000
    return value

def format_large_value(value, show_original_unit=False):
    """
    格式化大数值，使其更易读
    
    参数:
    value: 以万为单位的数值
    show_original_unit: 是否显示原始单位(万)
    
    返回:
    格式化后的字符串
    """
    # 1万亿及以上
    if value >= 100000000:  # 1万亿 = 100000000万
        billion_value = value / 10000
        if show_original_unit:
            return f"{billion_value:,.2f}亿 (万亿级别)"
        else:
            return f"{billion_value:,.2f}亿"
    # 10亿及以上
    elif value >= 10000:  # 1亿 = 10000万
        billion_value = value / 10000
        if show_original_unit:
            return f"{billion_value:,.2f}亿 ({value:,.0f}万)"
        else:
            return f"{billion_value:,.2f}亿"
    # 100万及以上
    elif value >= 100:  # 100万 = 100万
        if show_original_unit:
            return f"{value:,.0f}万"
        else:
            return f"{value:,.0f}万"
    # 小于100万
    else:
        return f"{value:,.2f}万"

def calculate_resources(meat, wood, coal, iron, pack_1w, pack_10w, pack_100w, strategy_type):
    """
    计算包裹内资源总数量（单位：万）
    提供两种自选包使用策略
    """
    # 记录原始资源
    original_meat, original_wood, original_coal, original_iron = meat, wood, coal, iron
    
    # 定义比例
    RATIO_MEAT, RATIO_WOOD, RATIO_COAL, RATIO_IRON = 4, 4, 2, 1
    
    # 创建自选包列表，按从大到小排序（100w优先，1w最后）
    packs = []
    packs.extend([100] * pack_100w)
    packs.extend([10] * pack_10w)
    packs.extend([1] * pack_1w)
    
    # 策略1: 按比例补充
    if strategy_type == 0:  # 按比例补充
        # 计算当前各资源的比例倍数
        meat_multiple = meat / RATIO_MEAT if RATIO_MEAT > 0 else 0
        wood_multiple = wood / RATIO_WOOD if RATIO_WOOD > 0 else 0
        coal_multiple = coal / RATIO_COAL if RATIO_COAL > 0 else 0
        iron_multiple = iron / RATIO_IRON if RATIO_IRON > 0 else 0
        
        # 使用所有自选包（从大到小）
        for pack_value in packs:
            # 找出比例倍数最小的资源
            min_multiple = min(meat_multiple, wood_multiple, coal_multiple, iron_multiple)
            
            if meat_multiple == min_multiple:
                meat += pack_value
                meat_multiple = meat / RATIO_MEAT
            elif wood_multiple == min_multiple:
                wood += pack_value
                wood_multiple = wood / RATIO_WOOD
            elif coal_multiple == min_multiple:
                coal_gain = pack_value / 2
                coal += coal_gain
                coal_multiple = coal / RATIO_COAL
            else:
                iron_gain = pack_value / 4
                iron += iron_gain
                iron_multiple = iron / RATIO_IRON
    
    # 策略2: 按顺序补充
    else:  # 按顺序补充
        # 计算当前各资源的比例倍数
        meat_multiple = meat / RATIO_MEAT if RATIO_MEAT > 0 else 0
        wood_multiple = wood / RATIO_WOOD if RATIO_WOOD > 0 else 0
        coal_multiple = coal / RATIO_COAL if RATIO_COAL > 0 else 0
        iron_multiple = iron / RATIO_IRON if RATIO_IRON > 0 else 0
        
        # 找到最大的比例倍数
        max_multiple = max(meat_multiple, wood_multiple, coal_multiple, iron_multiple)
        
        # 阶段1: 补充肉，直到肉的比例倍数等于最大比例倍数
        for pack_value in packs[:]:  # 使用副本遍历
            if meat_multiple < max_multiple:
                # 计算需要多少肉才能达到最大倍数
                meat_needed = max_multiple * RATIO_MEAT - meat
                
                # 使用当前最大的包补充肉
                meat += pack_value
                meat_multiple = meat / RATIO_MEAT
                packs.remove(pack_value)
                
                # 更新最大倍数（因为补充肉后可能肉成为新的最大）
                max_multiple = max(max_multiple, meat_multiple)
            else:
                break
        
        # 阶段2: 补充木头，直到木头的比例倍数等于最大比例倍数
        for pack_value in packs[:]:
            if wood_multiple < max_multiple:
                # 计算需要多少木头才能达到最大倍数
                wood_needed = max_multiple * RATIO_WOOD - wood
                
                # 使用当前最大的包补充木头
                wood += pack_value
                wood_multiple = wood / RATIO_WOOD
                packs.remove(pack_value)
                
                # 更新最大倍数
                max_multiple = max(max_multiple, wood_multiple)
            else:
                break
        
        # 阶段3: 补充煤，直到煤的比例倍数等于最大比例倍数
        for pack_value in packs[:]:
            if coal_multiple < max_multiple:
                # 计算需要多少煤才能达到最大倍数
                coal_needed = max_multiple * RATIO_COAL - coal
                
                # 使用当前最大的包补充煤
                coal_gain = pack_value / 2
                coal += coal_gain
                coal_multiple = coal / RATIO_COAL
                packs.remove(pack_value)
                
                # 更新最大倍数
                max_multiple = max(max_multiple, coal_multiple)
            else:
                break
        
        # 阶段4: 补充铁，直到铁的比例倍数等于最大比例倍数
        for pack_value in packs[:]:
            if iron_multiple < max_multiple:
                # 计算需要多少铁才能达到最大倍数
                iron_needed = max_multiple * RATIO_IRON - iron
                
                # 使用当前最大的包补充铁
                iron_gain = pack_value / 4
                iron += iron_gain
                iron_multiple = iron / RATIO_IRON
                packs.remove(pack_value)
                
                # 更新最大倍数
                max_multiple = max(max_multiple, iron_multiple)
            else:
                break
        
        # 阶段5: 如果还有剩余自选包，切换为按比例补充
        if packs:
            # 重新计算当前比例倍数
            meat_multiple = meat / RATIO_MEAT
            wood_multiple = wood / RATIO_WOOD
            coal_multiple = coal / RATIO_COAL
            iron_multiple = iron / RATIO_IRON
            
            # 按比例补充剩余自选包
            for pack_value in packs:
                # 找出比例倍数最小的资源
                min_multiple = min(meat_multiple, wood_multiple, coal_multiple, iron_multiple)
                
                if meat_multiple == min_multiple:
                    meat += pack_value
                    meat_multiple = meat / RATIO_MEAT
                elif wood_multiple == min_multiple:
                    wood += pack_value
                    wood_multiple = wood / RATIO_WOOD
                elif coal_multiple == min_multiple:
                    coal_gain = pack_value / 2
                    coal += coal_gain
                    coal_multiple = coal / RATIO_COAL
                else:
                    iron_gain = pack_value / 4
                    iron += iron_gain
                    iron_multiple = iron / RATIO_IRON
    
    # 计算最终比例和理想资源量
    final_min_ratio = min(
        meat / RATIO_MEAT if RATIO_MEAT > 0 else float('inf'),
        wood / RATIO_WOOD if RATIO_WOOD > 0 else float('inf'),
        coal / RATIO_COAL if RATIO_COAL > 0 else float('inf'),
        iron / RATIO_IRON if RATIO_IRON > 0 else float('inf')
    )
    
    # 计算理想按比例的资源量
    ideal_meat = final_min_ratio * RATIO_MEAT
    ideal_wood = final_min_ratio * RATIO_WOOD
    ideal_coal = final_min_ratio * RATIO_COAL
    ideal_iron = final_min_ratio * RATIO_IRON
    
    # 计算资源过剩情况
    excess_meat = meat - ideal_meat
    excess_wood = wood - ideal_wood
    excess_coal = coal - ideal_coal
    excess_iron = iron - ideal_iron
    
    # 计算每种资源通过自选包实际增加的数量
    meat_added = meat - original_meat
    wood_added = wood - original_wood
    coal_added = coal - original_coal
    iron_added = iron - original_iron
    
    return {
        'final': {
            'meat': meat,
            'wood': wood,
            'coal': coal,
            'iron': iron
        },
        'original': {
            'meat': original_meat,
            'wood': original_wood,
            'coal': original_coal,
            'iron': original_iron
        },
        'excess': {
            'meat': excess_meat,
            'wood': excess_wood,
            'coal': excess_coal,
            'iron': excess_iron
        },
        'added': {
            'meat': meat_added,
            'wood': wood_added,
            'coal': coal_added,
            'iron': iron_added
        },
        'ideal': {
            'meat': ideal_meat,
            'wood': ideal_wood,
            'coal': ideal_coal,
            'iron': ideal_iron
        },
        'ratio_multiple': final_min_ratio
    }

# 点击按钮时进行计算
if calculate_button:
    # 转换单位为万
    meat = convert_to_wan(meat_num, meat_unit)
    wood = convert_to_wan(wood_num, wood_unit)
    coal = convert_to_wan(coal_num, coal_unit)
    iron = convert_to_wan(iron_num, iron_unit)
    
    # 确定策略类型
    strategy_type = 0 if "按比例补充" in strategy else 1
    
    # 进行计算
    try:
        result = calculate_resources(meat, wood, coal, iron, pack_1w, pack_10w, pack_100w, strategy_type)
        
        # 显示计算结果
        st.markdown("## 📊 计算结果")
        
        # 1. 最终资源总量
        st.markdown("### 1. 最终资源总量（使用所有资源包后）")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # 格式化最终资源量
            final_meat_display = format_large_value(result['final']['meat'])
            # 格式化补充量
            added_meat_display = format_large_value(result['added']['meat'])
            st.metric("肉", final_meat_display, f"+{added_meat_display}")
        with col2:
            final_wood_display = format_large_value(result['final']['wood'])
            added_wood_display = format_large_value(result['added']['wood'])
            st.metric("木", final_wood_display, f"+{added_wood_display}")
        with col3:
            final_coal_display = format_large_value(result['final']['coal'])
            added_coal_display = format_large_value(result['added']['coal'])
            st.metric("煤", final_coal_display, f"+{added_coal_display}")
        with col4:
            final_iron_display = format_large_value(result['final']['iron'])
            added_iron_display = format_large_value(result['added']['iron'])
            st.metric("铁", final_iron_display, f"+{added_iron_display}")
        
        # 2. 资源过剩情况
        st.markdown("### 2. 资源过剩情况（超过4:4:2:1比例的部分）")
        
        excess_resources = []
        if result['excess']['meat'] > 0:
            excess_display = format_large_value(result['excess']['meat'], show_original_unit=True)
            excess_resources.append(f"🥩 肉过剩: {excess_display}")
        if result['excess']['wood'] > 0:
            excess_display = format_large_value(result['excess']['wood'], show_original_unit=True)
            excess_resources.append(f"🪵 木过剩: {excess_display}")
        if result['excess']['coal'] > 0:
            excess_display = format_large_value(result['excess']['coal'], show_original_unit=True)
            excess_resources.append(f"⛏️ 煤过剩: {excess_display}")
        if result['excess']['iron'] > 0:
            excess_display = format_large_value(result['excess']['iron'], show_original_unit=True)
            excess_resources.append(f"⚙️ 铁过剩: {excess_display}")
        
        if excess_resources:
            for excess in excess_resources:
                st.warning(excess)
        else:
            st.success("✅ 无资源过剩，所有资源都按4:4:2:1比例完美分配！")
        
        # 3. 通过资源包补充的资源量
        st.markdown("### 3. 通过资源包补充的资源量")
        
        # 创建进度条显示补充比例
        total_added = (result['added']['meat'] + result['added']['wood'] + 
                      result['added']['coal'] + result['added']['iron'])
        
        if total_added > 0:
            cols = st.columns(4)
            resources = [
                ("🥩 肉", result['added']['meat'], "#FF6B6B"),
                ("🪵 木", result['added']['wood'], "#4ECDC4"),
                ("⛏️ 煤", result['added']['coal'], "#45B7D1"),
                ("⚙️ 铁", result['added']['iron'], "#96CEB4")
            ]
            
            for i, (name, value, color) in enumerate(resources):
                with cols[i]:
                    if total_added > 0:
                        percentage = (value / total_added) * 100
                        st.markdown(f"**{name}**")
                        st.progress(min(100, percentage/100))
                        # 格式化显示
                        display_text = format_large_value(value)
                        st.markdown(f"{display_text} ({percentage:.1f}%)")
        
    except Exception as e:
        st.error(f"计算过程中出现错误: {e}")

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.9em;'>"
    "游戏资源计算器 · 使用Streamlit构建 · 祝您游戏愉快！"
    "</div>",
    unsafe_allow_html=True
)
