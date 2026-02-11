import streamlit as st
from itertools import permutations

# 设置页面
st.set_page_config(
    page_title="田忌赛马策略计算器",
    page_icon="🐎",
    layout="wide"
)

# 应用标题
st.title("🐎 田忌赛马策略计算器")
st.markdown("---")

# 初始化session state
if 'num_horses' not in st.session_state:
    st.session_state.num_horses = 3

if 'attack_horse_names' not in st.session_state:
    st.session_state.attack_horse_names = ["进攻方上马", "进攻方中马", "进攻方下马"]

if 'defense_horse_names' not in st.session_state:
    st.session_state.defense_horse_names = ["防守方上马", "防守方中马", "防守方下马"]

if 'attack_order' not in st.session_state:
    st.session_state.attack_order = [0, 1, 2]  # 默认顺序：上、中、下

# 主界面分为两列
col1, col2 = st.columns(2)

# 左侧：进攻方设置
with col1:
    st.subheader("🏇 进攻方设置")
    
    # 马匹数量控制
    col1_1, col1_2 = st.columns([3, 1])
    
    with col1_1:
        st.markdown("**马匹数量:**")
    
    with col1_2:
        # 添加马匹按钮
        if st.button("➕ 添加马匹", key="add_attack"):
            if st.session_state.num_horses < 6:
                st.session_state.num_horses += 1
                st.session_state.attack_horse_names.append(f"进攻方马{st.session_state.num_horses}")
                st.session_state.defense_horse_names.append(f"防守方马{st.session_state.num_horses}")
                # 初始化进攻方顺序
                st.session_state.attack_order = list(range(st.session_state.num_horses))
                st.rerun()
            else:
                st.warning("最多只能有6匹马！")
    
    # 为每匹马命名
    st.markdown("**为每匹马命名:**")
    
    attack_names_changed = False
    for i in range(st.session_state.num_horses):
        col_name = st.columns([1, 4, 1])
        
        with col_name[0]:
            # 显示马匹编号，1号最强
            st.markdown(f"**{i+1}号马:**")
        
        with col_name[1]:
            new_name = st.text_input(
                f"进攻方马匹{i+1}名称",
                value=st.session_state.attack_horse_names[i],
                key=f"attack_name_{i}",
                label_visibility="collapsed"
            )
            if new_name != st.session_state.attack_horse_names[i]:
                st.session_state.attack_horse_names[i] = new_name
                attack_names_changed = True
        
        with col_name[2]:
            if i >= 2:  # 至少保留2匹马
                if st.button("🗑️", key=f"remove_attack_{i}"):
                    # 删除马匹
                    st.session_state.num_horses -= 1
                    st.session_state.attack_horse_names.pop(i)
                    st.session_state.defense_horse_names.pop(i)
                    # 更新进攻方顺序
                    st.session_state.attack_order = [x if x < i else x-1 for x in st.session_state.attack_order if x != i]
                    st.rerun()
            else:
                st.empty()  # 占位符，保持对齐

# 右侧：防守方设置
with col2:
    st.subheader("🛡️ 防守方设置")
    
    # 马匹数量显示（与进攻方同步）
    col2_1, col2_2 = st.columns([3, 1])
    
    with col2_1:
        st.markdown("**马匹数量:**")
    
    with col2_2:
        # 删除马匹按钮（只在防守方显示）
        if st.button("➖ 删除马匹", key="remove_defense"):
            if st.session_state.num_horses > 2:
                st.session_state.num_horses -= 1
                st.session_state.attack_horse_names.pop()
                st.session_state.defense_horse_names.pop()
                # 更新进攻方顺序
                st.session_state.attack_order = [x for x in st.session_state.attack_order if x < st.session_state.num_horses]
                st.rerun()
            else:
                st.warning("至少需要2匹马！")
    
    # 为防守方马匹命名
    st.markdown("**为每匹马命名:**")
    
    defense_names_changed = False
    for i in range(st.session_state.num_horses):
        col_name = st.columns([1, 4])
        
        with col_name[0]:
            # 显示马匹编号，1号最强
            st.markdown(f"**{i+1}号马:**")
        
        with col_name[1]:
            new_name = st.text_input(
                f"防守方马匹{i+1}名称",
                value=st.session_state.defense_horse_names[i],
                key=f"defense_name_{i}",
                label_visibility="collapsed"
            )
            if new_name != st.session_state.defense_horse_names[i]:
                st.session_state.defense_horse_names[i] = new_name
                defense_names_changed = True

# 进攻方出场顺序设置
st.markdown("---")
st.subheader("🎯 进攻方出场顺序设置")

st.markdown("请为进攻方选择每场比赛的出赛马匹（每匹马只能使用一次）：")

# 创建进攻方出场顺序选择
remaining_horses = list(range(st.session_state.num_horses))
attack_order_names = [st.session_state.attack_horse_names[idx] for idx in st.session_state.attack_order]

# 检查是否有重复选择
if len(set(st.session_state.attack_order)) != len(st.session_state.attack_order):
    st.error("每匹马只能出场一次！请重新选择。")
    # 重置为唯一值
    st.session_state.attack_order = list(range(st.session_state.num_horses))
    st.rerun()

# 创建出场顺序选择器
attack_order_updated = False
new_attack_order = []

for i in range(st.session_state.num_horses):
    col_order = st.columns([1, 4])
    
    with col_order[0]:
        st.markdown(f"**第{i+1}场:**")
    
    with col_order[1]:
        # 获取可选的马匹（排除已选择的）
        available_horses = [h for h in range(st.session_state.num_horses) if h not in new_attack_order]
        
        # 如果当前选择不可用，则选择第一个可用马匹
        if st.session_state.attack_order[i] not in available_horses and available_horses:
            st.session_state.attack_order[i] = available_horses[0]
            st.rerun()
        
        selected_horse = st.selectbox(
            f"选择第{i+1}场比赛的马匹",
            options=available_horses,
            index=available_horses.index(st.session_state.attack_order[i]) if st.session_state.attack_order[i] in available_horses else 0,
            format_func=lambda x: st.session_state.attack_horse_names[x],
            key=f"attack_order_{i}",
            label_visibility="collapsed"
        )
        
        if selected_horse != st.session_state.attack_order[i]:
            st.session_state.attack_order[i] = selected_horse
            attack_order_updated = True
        
        new_attack_order.append(selected_horse)

# 显示进攻方出场顺序
st.markdown("### 当前进攻方出场顺序:")
order_display = []
for i, horse_idx in enumerate(st.session_state.attack_order):
    horse_name = st.session_state.attack_horse_names[horse_idx]
    order_display.append(f"第{i+1}场: **{horse_name}**")

st.markdown(" | ".join(order_display))

# 核心算法函数
def compare_horses(defense_idx, attack_idx):
    """比较两匹马的实力，数字越小实力越强"""
    # 数字越小实力越强，所以防守方胜的条件是 defense_idx < attack_idx
    if defense_idx < attack_idx:
        return "win"  # 防守方胜
    elif defense_idx > attack_idx:
        return "lose"  # 进攻方胜
    else:
        return "draw"  # 平局

def find_best_strategies(attack_order, num_horses):
    """找到所有最佳防守策略"""
    defense_horses = list(range(num_horses))
    best_strategies = []
    max_wins = -1
    
    # 遍历所有可能的防守顺序
    for defense_order in permutations(defense_horses):
        wins = 0
        draws = 0
        
        # 计算胜场和平场
        for i in range(num_horses):
            result = compare_horses(defense_order[i], attack_order[i])
            if result == "win":
                wins += 1
            elif result == "draw":
                draws += 1
        
        # 更新最佳策略
        if wins > max_wins:
            max_wins = wins
            best_strategies = [(list(defense_order), wins, draws)]
        elif wins == max_wins:
            best_strategies.append((list(defense_order), wins, draws))
    
    return best_strategies, max_wins

# 计算按钮
st.markdown("---")
col_btn1, col_btn2 = st.columns([1, 3])

with col_btn1:
    if st.button("🚀 计算最佳防守策略", type="primary", use_container_width=True):
        st.session_state.calculate_clicked = True

with col_btn2:
    if st.button("🔄 重置所有设置", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# 显示计算结果
if st.session_state.get('calculate_clicked', False):
    num_horses = st.session_state.num_horses
    attack_order = st.session_state.attack_order
    
    with st.spinner("正在计算最佳防守策略..."):
        best_strategies, max_wins = find_best_strategies(attack_order, num_horses)
        
        st.markdown("---")
        st.subheader("🏆 计算结果")
        
        # 显示统计信息
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("最佳策略数量", len(best_strategies))
        
        with col_stat2:
            st.metric("最大胜场数", f"{max_wins}/{num_horses}")
        
        with col_stat3:
            win_rate = (max_wins / num_horses) * 100
            st.metric("胜率", f"{win_rate:.1f}%")
        
        # 判断比赛结果
        st.markdown("### 📈 比赛预测")
        if max_wins > num_horses / 2:
            st.success(f"✅ **防守方可以赢得比赛！** (胜场数: {max_wins}/{num_horses})")
        elif max_wins == num_horses / 2 and num_horses % 2 == 0:
            st.warning(f"⚠️ **比赛可能平局** (胜场数: {max_wins}/{num_horses})")
        else:
            st.error(f"❌ **防守方难以赢得比赛** (胜场数: {max_wins}/{num_horses})")
        
        # 显示最佳策略
        st.markdown("### 🛡️ 最佳防守策略")
        
        # 使用第一个最佳策略进行详细展示
        if best_strategies:
            defense_order, wins, draws = best_strategies[0]
            losses = num_horses - wins - draws
            
            # 显示防守方出场顺序
            st.markdown("**防守方出场顺序:**")
            defense_order_names = [st.session_state.defense_horse_names[idx] for idx in defense_order]
            order_display = []
            for i, horse_name in enumerate(defense_order_names):
                order_display.append(f"第{i+1}场: **{horse_name}**")
            
            st.markdown(" | ".join(order_display))
            
            # 显示统计
            col_win, col_draw, col_lose = st.columns(3)
            with col_win:
                st.markdown(f"**{wins}** 胜")
            with col_draw:
                st.markdown(f"**{draws}** 平")
            with col_lose:
                st.markdown(f"**{losses}** 负")
            
            # 详细对战分析
            st.markdown("#### 📋 详细对战分析")
            
            # 创建HTML表格
            table_html = '''
            <style>
            .horse-table {
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                font-family: Arial, sans-serif;
            }
            .horse-table th {
                background-color: #4a6fa5;
                color: white;
                padding: 12px;
                text-align: center;
                font-weight: bold;
            }
            .horse-table td {
                padding: 12px;
                text-align: center;
                border-bottom: 1px solid #ddd;
            }
            .horse-table tr:hover {
                background-color: #f5f5f5;
            }
            .win-row {
                background-color: #d4edda;
            }
            .lose-row {
                background-color: #f8d7da;
            }
            .draw-row {
                background-color: #fff3cd;
            }
            </style>
            
            <table class="horse-table">
                <thead>
                    <tr>
                        <th>场次</th>
                        <th>防守方马匹</th>
                        <th>进攻方马匹</th>
                        <th>比赛结果</th>
                        <th>实力对比</th>
                    </tr>
                </thead>
                <tbody>
            '''
            
            for i in range(num_horses):
                defense_idx = defense_order[i]
                attack_idx = attack_order[i]
                defense_horse_name = st.session_state.defense_horse_names[defense_idx]
                attack_horse_name = st.session_state.attack_horse_names[attack_idx]
                result = compare_horses(defense_idx, attack_idx)
                
                # 确定行样式
                if result == "win":
                    row_class = "win-row"
                    result_text = "防守方胜"
                elif result == "lose":
                    row_class = "lose-row"
                    result_text = "进攻方胜"
                else:
                    row_class = "draw-row"
                    result_text = "平局"
                
                # 实力对比描述
                # 注意：数字越小实力越强
                defense_horse_num = defense_idx + 1  # 转换为1-based编号
                attack_horse_num = attack_idx + 1    # 转换为1-based编号
                
                if defense_idx < attack_idx:
                    # 防守方马编号更小，实力更强
                    comparison = f"防守方更强 ({defense_horse_num}号马 > {attack_horse_num}号马)"
                elif defense_idx > attack_idx:
                    # 进攻方马编号更小，实力更强
                    comparison = f"进攻方更强 ({defense_horse_num}号马 < {attack_horse_num}号马)"
                else:
                    comparison = f"实力相等 ({defense_horse_num}号马 = {attack_horse_num}号马)"
                
                table_html += f'''
                <tr class="{row_class}">
                    <td>第{i+1}场</td>
                    <td><strong>{defense_horse_name}</strong></td>
                    <td><strong>{attack_horse_name}</strong></td>
                    <td><strong>{result_text}</strong></td>
                    <td>{comparison}</td>
                </tr>
                '''
            
            table_html += "</tbody></table>"
            st.markdown(table_html, unsafe_allow_html=True)
            
            # 显示其他最佳策略
            if len(best_strategies) > 1:
                with st.expander(f"查看其他 {len(best_strategies)-1} 种最佳策略"):
                    for idx, (order, wins, draws) in enumerate(best_strategies[1:], 2):
                        order_names = [st.session_state.defense_horse_names[i] for i in order]
                        st.markdown(f"**策略 {idx}:** {order_names} (胜:{wins} 平:{draws})")

# 初始状态显示说明
else:
    st.markdown("---")
    with st.expander("ℹ️ 使用说明", expanded=True):
        st.markdown("""
        ### 游戏规则
        
        田忌赛马是中国古代著名的策略故事。田忌通过调整马匹的出场顺序，以弱胜强战胜了齐威王。
        
        ### 使用步骤
        
        1. **设置马匹数量** (通过"添加马匹"和"删除马匹"按钮)
           - 最少2匹，最多6匹马
        
        2. **为马匹命名**
           - 为进攻方和防守方的每匹马命名
           - 命名规则：数字越小，实力越强 (1号马最强)
        
        3. **设置进攻方出场顺序**
           - 为进攻方选择每场比赛的出赛马匹
           - 每匹马只能出场一次
        
        4. **计算防守策略**
           - 点击"计算最佳防守策略"按钮
           - 系统会自动计算出防守方的最佳出场顺序
        
        5. **分析结果**
           - 查看防守方的最佳出场顺序
           - 分析每场比赛的胜负情况
           - 查看比赛预测和统计信息
        
        ### 实力规则
        
        - **数字越小，实力越强** (1号马最强)
        - 相同数字的马匹实力相等
        - 防守方马数字 < 进攻方马数字 → 防守方胜
        - 防守方马数字 > 进攻方马数字 → 进攻方胜
        - 防守方马数字 = 进攻方马数字 → 平局
        
        **实力对比说明：**
        - "防守方更强 (2号马 > 3号马)" 表示防守方的2号马比进攻方的3号马实力更强
        - "进攻方更强 (4号马 < 1号马)" 表示进攻方的1号马比防守方的4号马实力更强
        - 这里的">"和"<"表示"实力强于"和"实力弱于"
        
        **现在，请先设置马匹和进攻方顺序，然后点击"计算最佳防守策略"按钮开始！**
        """)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.9em; padding: 20px 0;">
        <p>田忌赛马策略计算器 | 基于Streamlit开发</p>
        <p>马匹数量: 2-6匹 | 算法: 暴力搜索（全排列）</p>
    </div>
    """,
    unsafe_allow_html=True
)
