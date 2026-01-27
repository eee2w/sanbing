import streamlit as st
import numpy as np

# 设置页面标题和布局
st.set_page_config(
    page_title="游戏资源计算器",
    page_icon="🎮",
    layout="centered"
)

# 应用标题
st.title("🎮 游戏资源计算器")
st.markdown("---")

# 侧边栏说明
with st.sidebar:
    st.header("使用说明")
    st.markdown("""
    ### 功能说明：
    1. 计算使用所有资源包后的资源总量
    2. 显示超过4:4:2:1比例的资源过剩情况
    3. 显示通过资源包补充的资源量
    
    ### 单位说明：
    - 所有资源单位均为"万"
    - 例如：输入"10"表示10万资源
    
    ### 资源包说明：
    - 1w资源包：提供1万资源（按肉/木计算）
    - 10w资源包：提供10万资源
    - 100w资源包：提供100万资源
    """)
    
    st.markdown("---")
    st.info("💡 提示：资源包会按照从大到小的顺序使用（100w → 10w → 1w）")

# 创建两列布局
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 已有资源")
    meat = st.number_input("肉的数量 (万)", min_value=0.0, value=0.0, step=1.0, format="%.1f")
    wood = st.number_input("木头数量 (万)", min_value=0.0, value=0.0, step=1.0, format="%.1f")
    coal = st.number_input("煤的数量 (万)", min_value=0.0, value=0.0, step=1.0, format="%.1f")
    iron = st.number_input("铁的数量 (万)", min_value=0.0, value=0.0, step=1.0, format="%.1f")

with col2:
    st.subheader("🎁 资源包数量")
    pack_1w = st.number_input("1w资源包数量", min_value=0, value=0, step=1)
    pack_10w = st.number_input("10w资源包数量", min_value=0, value=0, step=1)
    pack_100w = st.number_input("100w资源包数量", min_value=0, value=0, step=1)

st.markdown("---")

# 策略选择
st.subheader("⚙️ 补充策略选择")
strategy = st.radio(
    "请选择资源包使用策略：",
    ["按比例补充（尽量满足4:4:2:1的比例）", "按顺序补充（先按肉→木→煤→铁的顺序补充，达到比例后按比例补充）"],
    horizontal=True
)

# 计算按钮
st.markdown("---")
calculate_button = st.button("🚀 开始计算", type="primary", use_container_width=True)

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
        # 计算当前资源比例倍数
        meat_ratio = meat / RATIO_MEAT if RATIO_MEAT > 0 else 0
        wood_ratio = wood / RATIO_WOOD if RATIO_WOOD > 0 else 0
        coal_ratio = coal / RATIO_COAL if RATIO_COAL > 0 else 0
        iron_ratio = iron / RATIO_IRON if RATIO_IRON > 0 else 0
        
        # 使用所有自选包（从大到小）
        for pack_value in packs:
            # 找出比例最小的资源
            ratios = [meat_ratio, wood_ratio, coal_ratio, iron_ratio]
            min_ratio = min(ratios)
            
            if meat_ratio == min_ratio:
                meat += pack_value
                meat_ratio = meat / RATIO_MEAT
            elif wood_ratio == min_ratio:
                wood += pack_value
                wood_ratio = wood / RATIO_WOOD
            elif coal_ratio == min_ratio:
                coal_gain = pack_value / 2
                coal += coal_gain
                coal_ratio = coal / RATIO_COAL
            else:
                iron_gain = pack_value / 4
                iron += iron_gain
                iron_ratio = iron / RATIO_IRON
    
    # 策略2: 先按顺序补充，达到比例后按比例补充
    else:  # 按顺序补充
        # 阶段1: 补充肉，直到肉的倍数不小于当前最大倍数
        # 使用剩余的最大包来补充肉
        for i in range(len(packs)):
            # 计算当前比例倍数
            meat_multiple = meat / RATIO_MEAT if RATIO_MEAT > 0 else 0
            wood_multiple = wood / RATIO_WOOD if RATIO_WOOD > 0 else 0
            coal_multiple = coal / RATIO_COAL if RATIO_COAL > 0 else 0
            iron_multiple = iron / RATIO_IRON if RATIO_IRON > 0 else 0
            
            max_multiple = max(meat_multiple, wood_multiple, coal_multiple, iron_multiple)
            
            # 如果肉的倍数已经不小于最大倍数，停止补充肉
            if meat_multiple >= max_multiple:
                break
            
            # 使用当前最大的包补充肉
            if packs:  # 检查是否还有包
                max_pack = max(packs)
                meat += max_pack
                packs.remove(max_pack)
        
        # 阶段2: 补充木头，直到木头的倍数不小于当前最大倍数
        for i in range(len(packs)):
            # 计算当前比例倍数
            meat_multiple = meat / RATIO_MEAT if RATIO_MEAT > 0 else 0
            wood_multiple = wood / RATIO_WOOD if RATIO_WOOD > 0 else 0
            coal_multiple = coal / RATIO_COAL if RATIO_COAL > 0 else 0
            iron_multiple = iron / RATIO_IRON if RATIO_IRON > 0 else 0
            
            max_multiple = max(meat_multiple, wood_multiple, coal_multiple, iron_multiple)
            
            # 如果木头的倍数已经不小于最大倍数，停止补充木头
            if wood_multiple >= max_multiple:
                break
            
            # 使用当前最大的包补充木头
            if packs:  # 检查是否还有包
                max_pack = max(packs)
                wood += max_pack
                packs.remove(max_pack)
        
        # 阶段3: 补充煤，直到煤的倍数不小于当前最大倍数
        for i in range(len(packs)):
            # 计算当前比例倍数
            meat_multiple = meat / RATIO_MEAT if RATIO_MEAT > 0 else 0
            wood_multiple = wood / RATIO_WOOD if RATIO_WOOD > 0 else 0
            coal_multiple = coal / RATIO_COAL if RATIO_COAL > 0 else 0
            iron_multiple = iron / RATIO_IRON if RATIO_IRON > 0 else 0
            
            max_multiple = max(meat_multiple, wood_multiple, coal_multiple, iron_multiple)
            
            # 如果煤的倍数已经不小于最大倍数，停止补充煤
            if coal_multiple >= max_multiple:
                break
            
            # 使用当前最大的包补充煤
            if packs:  # 检查是否还有包
                max_pack = max(packs)
                coal_gain = max_pack / 2
                coal += coal_gain
                packs.remove(max_pack)
        
        # 阶段4: 补充铁，直到铁的倍数不小于当前最大倍数
        for i in range(len(packs)):
            # 计算当前比例倍数
            meat_multiple = meat / RATIO_MEAT if RATIO_MEAT > 0 else 0
            wood_multiple = wood / RATIO_WOOD if RATIO_WOOD > 0 else 0
            coal_multiple = coal / RATIO_COAL if RATIO_COAL > 0 else 0
            iron_multiple = iron / RATIO_IRON if RATIO_IRON > 0 else 0
            
            max_multiple = max(meat_multiple, wood_multiple, coal_multiple, iron_multiple)
            
            # 如果铁的倍数已经不小于最大倍数，停止补充铁
            if iron_multiple >= max_multiple:
                break
            
            # 使用当前最大的包补充铁
            if packs:  # 检查是否还有包
                max_pack = max(packs)
                iron_gain = max_pack / 4
                iron += iron_gain
                packs.remove(max_pack)
        
        # 阶段5: 如果还有剩余自选包，切换为按比例补充
        if packs:
            # 重新计算当前比例倍数
            meat_ratio = meat / RATIO_MEAT if RATIO_MEAT > 0 else 0
            wood_ratio = wood / RATIO_WOOD if RATIO_WOOD > 0 else 0
            coal_ratio = coal / RATIO_COAL if RATIO_COAL > 0 else 0
            iron_ratio = iron / RATIO_IRON if RATIO_IRON > 0 else 0
            
            # 按比例补充剩余自选包（从大到小）
            for pack_value in sorted(packs, reverse=True):
                # 找出比例最小的资源
                ratios = [meat_ratio, wood_ratio, coal_ratio, iron_ratio]
                min_ratio = min(ratios)
                
                if meat_ratio == min_ratio:
                    meat += pack_value
                    meat_ratio = meat / RATIO_MEAT
                elif wood_ratio == min_ratio:
                    wood += pack_value
                    wood_ratio = wood / RATIO_WOOD
                elif coal_ratio == min_ratio:
                    coal_gain = pack_value / 2
                    coal += coal_gain
                    coal_ratio = coal / RATIO_COAL
                else:
                    iron_gain = pack_value / 4
                    iron += iron_gain
                    iron_ratio = iron / RATIO_IRON
    
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
            st.metric("肉", f"{result['final']['meat']:.2f}万", f"+{result['added']['meat']:.2f}万")
        with col2:
            st.metric("木", f"{result['final']['wood']:.2f}万", f"+{result['added']['wood']:.2f}万")
        with col3:
            st.metric("煤", f"{result['final']['coal']:.2f}万", f"+{result['added']['coal']:.2f}万")
        with col4:
            st.metric("铁", f"{result['final']['iron']:.2f}万", f"+{result['added']['iron']:.2f}万")
        
        # 2. 资源过剩情况
        st.markdown("### 2. 资源过剩情况（超过4:4:2:1比例的部分）")
        
        excess_resources = []
        if result['excess']['meat'] > 0:
            excess_resources.append(f"🥩 肉过剩: {result['excess']['meat']:.2f}万")
        if result['excess']['wood'] > 0:
            excess_resources.append(f"🪵 木过剩: {result['excess']['wood']:.2f}万")
        if result['excess']['coal'] > 0:
            excess_resources.append(f"⛏️ 煤过剩: {result['excess']['coal']:.2f}万")
        if result['excess']['iron'] > 0:
            excess_resources.append(f"⚙️ 铁过剩: {result['excess']['iron']:.2f}万")
        
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
                        st.markdown(f"{value:.2f}万 ({percentage:.1f}%)")
        
        # 显示比例信息
        st.markdown("---")
        st.markdown("#### 📈 比例信息")
        st.info(f"当前资源可支持 **{result['ratio_multiple']:.2f}倍** 的4:4:2:1比例")
        
        # 显示理想分配量
        with st.expander("查看理想分配详情"):
            st.markdown("**按4:4:2:1比例分配的理想资源量：**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("肉", f"{result['ideal']['meat']:.2f}万")
            with col2:
                st.metric("木", f"{result['ideal']['wood']:.2f}万")
            with col3:
                st.metric("煤", f"{result['ideal']['coal']:.2f}万")
            with col4:
                st.metric("铁", f"{result['ideal']['iron']:.2f}万")
        
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
