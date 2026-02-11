import streamlit as st
from itertools import permutations
import random

# 设置页面
st.set_page_config(
    page_title="田忌赛马策略计算器",
    page_icon="🐎",
    layout="wide"
)

# 应用标题
st.title("🐎 田忌赛马策略计算器")
st.markdown("---")

# 在侧边栏设置参数
with st.sidebar:
    st.header("⚙️ 参数设置")
    
    # 选择马匹数量
    n_horses = st.slider(
        "选择马匹数量",
        min_value=2,
        max_value=6,
        value=3,
        help="双方都有相同数量的马匹，数字越小实力越强"
    )
    
    st.markdown("---")
    st.header("📋 进攻方顺序设置")
    
    # 根据马匹数量创建进攻方顺序输入
    st.markdown("请设置进攻方每场比赛派出的马匹：")
    
    # 初始化或更新进攻方顺序
    if 'attack_order' not in st.session_state or len(st.session_state.attack_order) != n_horses:
        st.session_state.attack_order = list(range(1, n_horses + 1))
    
    # 为每场比赛选择马匹
    available_horses = list(range(1, n_horses + 1))
    new_order = []
    
    for i in range(n_horses):
        # 排除已经选择的马匹
        remaining_horses = [h for h in available_horses if h not in new_order]
        
        # 创建选择框
        selected = st.selectbox(
            f"第{i+1}场比赛派出马匹",
            options=remaining_horses,
            index=0,
            key=f"attack_select_{i}"
        )
        new_order.append(selected)
    
    # 更新进攻方顺序
    st.session_state.attack_order = new_order
    
    st.markdown("---")
    st.header("🚀 快速设置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("常规顺序"):
            st.session_state.attack_order = list(range(1, n_horses + 1))
            st.rerun()
    
    with col2:
        if st.button("倒序"):
            st.session_state.attack_order = list(range(n_horses, 0, -1))
            st.rerun()
    
    if st.button("随机顺序"):
        random_order = list(range(1, n_horses + 1))
        random.shuffle(random_order)
        st.session_state.attack_order = random_order
        st.rerun()

# 核心算法函数
def compare_horses(defense, attack):
    """比较两匹马的实力"""
    if defense < attack:
        return "win"  # 防守方马更强
    elif defense > attack:
        return "lose"  # 进攻方马更强
    else:
        return "draw"  # 实力相等

def find_best_strategies(attack_order, n_horses):
    """找到所有最佳防守策略"""
    defense_horses = list(range(1, n_horses + 1))
    best_strategies = []
    max_wins = -1
    
    # 遍历所有可能的防守顺序
    for defense_order in permutations(defense_horses):
        wins = 0
        draws = 0
        
        # 计算胜场和平场
        for i in range(n_horses):
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

# 主显示区域
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🏇 比赛信息")
    
    # 显示进攻方顺序
    st.markdown(f"**进攻方派马顺序:**")
    
    # 创建漂亮的马匹显示
    attack_html = '<div style="display: flex; gap: 10px; margin: 15px 0;">'
    for i, horse in enumerate(st.session_state.attack_order):
        attack_html += f'''
        <div style="text-align: center;">
            <div style="background-color: #ff6b6b; color: white; width: 60px; height: 60px; 
                        border-radius: 10px; display: flex; align-items: center; 
                        justify-content: center; font-size: 24px; font-weight: bold;">
                {horse}
            </div>
            <div style="margin-top: 5px; font-weight: bold;">第{i+1}场</div>
        </div>
        '''
    attack_html += '</div>'
    st.markdown(attack_html, unsafe_allow_html=True)
    
    # 显示马匹实力说明
    with st.expander("📊 马匹实力说明"):
        st.markdown(f"""
        - 马匹用数字 **{1}** 到 **{n_horses}** 表示
        - **数字越小，实力越强**
        - 1号马实力最强，{n_horses}号马实力最弱
        - 相同数字的马匹实力相同
        - 比较规则：防守方马数字 < 进攻方马数字 → 防守方胜
        """)

with col2:
    st.subheader("🎯 开始计算")
    
    # 计算按钮
    if st.button("🚀 计算最佳防守策略", type="primary", use_container_width=True):
        st.session_state.calculate_clicked = True
    
    if st.button("🔄 重新开始", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key != 'attack_order':
                del st.session_state[key]
        st.rerun()

# 显示计算结果
if st.session_state.get('calculate_clicked', False):
    attack_order = st.session_state.attack_order
    
    with st.spinner("正在计算最佳防守策略..."):
        best_strategies, max_wins = find_best_strategies(attack_order, n_horses)
        
        st.markdown("---")
        st.subheader("🏆 计算结果")
        
        # 显示统计信息
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("最佳策略数量", len(best_strategies))
        
        with col_stat2:
            st.metric("最大胜场数", f"{max_wins}/{n_horses}")
        
        with col_stat3:
            win_rate = (max_wins / n_horses) * 100
            st.metric("胜率", f"{win_rate:.1f}%")
        
        # 判断比赛结果
        st.markdown("### 📈 比赛预测")
        if max_wins > n_horses / 2:
            st.success(f"✅ **防守方可以赢得比赛！** (胜场数: {max_wins}/{n_horses})")
        elif max_wins == n_horses / 2 and n_horses % 2 == 0:
            st.warning(f"⚠️ **比赛可能平局** (胜场数: {max_wins}/{n_horses})")
        else:
            st.error(f"❌ **防守方难以赢得比赛** (胜场数: {max_wins}/{n_horses})")
        
        # 显示最佳策略
        st.markdown("### 🛡️ 最佳防守策略")
        
        # 创建选项卡显示不同的策略
        if len(best_strategies) <= 5:
            tabs = st.tabs([f"策略 {i+1}" for i in range(len(best_strategies))])
        else:
            st.info(f"找到 {len(best_strategies)} 种最佳策略，显示前5种")
            tabs = st.tabs([f"策略 {i+1}" for i in range(min(5, len(best_strategies)))])
        
        for idx, tab in enumerate(tabs):
            with tab:
                defense_order, wins, draws = best_strategies[idx]
                losses = n_horses - wins - draws
                
                # 显示防守方顺序
                st.markdown(f"**防守方派马顺序:** `{defense_order}`")
                
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
                .horse-number {
                    display: inline-block;
                    width: 30px;
                    height: 30px;
                    line-height: 30px;
                    border-radius: 50%;
                    font-weight: bold;
                    color: white;
                }
                .defense-horse {
                    background-color: #3498db;
                }
                .attack-horse {
                    background-color: #e74c3c;
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
                
                for i in range(n_horses):
                    defense_horse = defense_order[i]
                    attack_horse = attack_order[i]
                    result = compare_horses(defense_horse, attack_horse)
                    
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
                    if defense_horse < attack_horse:
                        comparison = f"防守方更强 ({defense_horse} < {attack_horse})"
                    elif defense_horse > attack_horse:
                        comparison = f"进攻方更强 ({defense_horse} > {attack_horse})"
                    else:
                        comparison = f"实力相等 ({defense_horse} = {attack_horse})"
                    
                    table_html += f'''
                    <tr class="{row_class}">
                        <td>第{i+1}场</td>
                        <td>
                            <span class="horse-number defense-horse">{defense_horse}</span>
                        </td>
                        <td>
                            <span class="horse-number attack-horse">{attack_horse}</span>
                        </td>
                        <td><strong>{result_text}</strong></td>
                        <td>{comparison}</td>
                    </tr>
                    '''
                
                table_html += "</tbody></table>"
                st.markdown(table_html, unsafe_allow_html=True)
        
        # 如果没有显示所有策略，显示更多选项
        if len(best_strategies) > 5:
            with st.expander(f"查看所有 {len(best_strategies)} 种最佳策略"):
                for idx, (order, wins, draws) in enumerate(best_strategies):
                    losses = n_horses - wins - draws
                    st.code(f"策略 {idx+1}: {order} (胜:{wins} 平:{draws} 负:{losses})")
        
        # 简单的图表展示
        st.markdown("### 📊 比赛结果分布")
        
        if len(best_strategies) > 0:
            # 使用第一个策略的数据
            defense_order, wins, draws = best_strategies[0]
            losses = n_horses - wins - draws
            
            # 创建简单的文本图表
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.markdown("**胜/平/负分布:**")
                
                # 创建简单的进度条表示
                total = n_horses
                win_percent = (wins / total) * 100
                draw_percent = (draws / total) * 100
                lose_percent = (losses / total) * 100
                
                st.markdown(f"胜场: {wins}场")
                st.progress(win_percent/100)
                
                st.markdown(f"平场: {draws}场")
                st.progress(draw_percent/100)
                
                st.markdown(f"负场: {losses}场")
                st.progress(lose_percent/100)
            
            with col_chart2:
                st.markdown("**每场比赛结果:**")
                
                # 显示每场比赛的简单结果
                for i in range(n_horses):
                    defense_horse = defense_order[i]
                    attack_horse = attack_order[i]
                    result = compare_horses(defense_horse, attack_horse)
                    
                    if result == "win":
                        result_icon = "✅"
                        result_color = "green"
                    elif result == "lose":
                        result_icon = "❌"
                        result_color = "red"
                    else:
                        result_icon = "➖"
                        result_color = "orange"
                    
                    st.markdown(
                        f"{result_icon} 第{i+1}场: 防守方**{defense_horse}** vs 进攻方**{attack_horse}**"
                    )

# 初始状态显示说明
else:
    st.markdown("## 🎮 如何使用本应用")
    
    with st.expander("点击查看详细说明", expanded=True):
        st.markdown("""
        ### 游戏背景
        田忌赛马是中国古代著名的策略故事。田忌通过调整马匹的出场顺序，以弱胜强战胜了齐威王。
        
        ### 游戏规则
        1. 双方各有相同数量的马匹
        2. 马匹实力用数字表示：**数字越小，实力越强**
        3. 进攻方按照固定顺序派出马匹
        4. 防守方在已知进攻方顺序的情况下，安排自己的马匹出场顺序
        5. 目标：防守方获得尽可能多的胜利
        
        ### 使用步骤
        1. **设置参数**（左侧边栏）:
           - 选择马匹数量（2-6匹）
           - 设置进攻方每场比赛派出的马匹
           - 可以使用"快速设置"按钮快速生成顺序
        
        2. **计算策略**:
           - 点击"计算最佳防守策略"按钮
           - 系统会自动找出防守方的最佳出场顺序
        
        3. **分析结果**:
           - 查看防守方的最佳策略
           - 分析每场比赛的胜负情况
           - 查看比赛统计和预测
        
        ### 示例
        假设双方各有3匹马（1最强，3最弱），进攻方顺序为 [1, 2, 3]：
        - 最佳防守策略可能是 [3, 1, 2]
        - 这样可以用最弱的马对最强的马（输），用最强的马对中等的马（赢），用中等的马对最弱的马（赢）
        - 最终结果：2胜1负，防守方获胜
        
        **现在，请使用左侧边栏设置参数，然后点击"计算最佳防守策略"按钮开始！**
        """)
    
    # 显示示例图片或图表
    st.markdown("---")
    st.markdown("### 🎯 经典案例：3匹马的对战")
    
    example_col1, example_col2 = st.columns(2)
    
    with example_col1:
        st.markdown("**常规策略（失败）:**")
        st.markdown("""
        ```
        进攻方: 1 2 3
        防守方: 1 2 3
        结果:   0胜 0平 3负
        ```
        """)
    
    with example_col2:
        st.markdown("**田忌策略（胜利）:**")
        st.markdown("""
        ```
        进攻方: 1 2 3
        防守方: 3 1 2
        结果:   2胜 0平 1负
        ```
        """)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.9em; padding: 20px 0;">
        <p>田忌赛马策略计算器 | 基于Streamlit开发 | 无需额外依赖</p>
        <p>马匹数量: 2-6匹 | 算法: 暴力搜索（全排列）</p>
    </div>
    """,
    unsafe_allow_html=True
)
