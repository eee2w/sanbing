import streamlit as st
from itertools import permutations

# 设置页面
st.set_page_config(
    page_title="田忌赛马策略计算器",
    page_icon="🐎",
    layout="wide"
)

# 标题
st.title("🐎 田忌赛马策略计算器")
st.markdown("---")

# 侧边栏 - 参数设置
with st.sidebar:
    st.header("⚙️ 参数设置")
    
    # 马匹数量选择
    n_horses = st.slider("选择马匹数量", 1, 6, 3, 
                         help="双方都有相同数量的马匹，数字越小实力越强")
    
    st.markdown("---")
    
    st.header("📋 进攻方顺序设置")
    st.markdown("为进攻方的每匹马选择出场顺序：")
    
    # 根据马匹数量生成输入
    horses = list(range(1, n_horses + 1))
    attack_order = []
    
    for i in range(n_horses):
        label = f"第{i+1}场派出马匹"
        # 创建选择框，排除已选择的马匹
        available_horses = [h for h in horses if h not in attack_order]
        horse = st.selectbox(label, available_horses, 
                            key=f"attack_{i}", 
                            help=f"选择第{i+1}场出战的马匹")
        attack_order.append(horse)
    
    st.markdown("---")
    
    # 快速预设按钮
    st.header("🚀 快速预设")
    if st.button("常规顺序 (1→n)"):
        attack_order = list(range(1, n_horses + 1))
        st.session_state.attack_order = attack_order
        st.rerun()
    
    if st.button("倒序 (n→1)"):
        attack_order = list(range(n_horses, 0, -1))
        st.session_state.attack_order = attack_order
        st.rerun()
    
    # 随机顺序
    if st.button("随机顺序"):
        import random
        random_order = list(range(1, n_horses + 1))
        random.shuffle(random_order)
        st.session_state.attack_order = random_order
        st.rerun()

# 保存进攻顺序到session state
if 'attack_order' not in st.session_state:
    st.session_state.attack_order = attack_order
else:
    attack_order = st.session_state.attack_order

# 主页面显示进攻方信息
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    st.subheader("🏇 进攻方派马顺序")
    
    # 创建漂亮的展示框
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h4 style="color: #e74c3c; margin-top: 0;">进攻方顺序:</h4>
        <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
    """, unsafe_allow_html=True)
    
    for i, horse in enumerate(attack_order):
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="background-color: #e74c3c; color: white; width: 60px; height: 60px; 
                        border-radius: 50%; display: flex; align-items: center; 
                        justify-content: center; font-size: 24px; font-weight: bold; margin: 5px;">
                {horse}
            </div>
            <div style="margin-top: 5px; font-weight: bold;">第{i+1}场</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # 马匹实力说明
    with st.expander("📊 马匹实力说明"):
        st.markdown("""
        - 马匹用数字表示：**数字越小，实力越强**
        - 1号马实力最强，{n}号马实力最弱
        - 相同数字的马匹实力相同
        """.format(n=n_horses))

# 核心算法函数
def compare_horses(defense, attack):
    """比较两匹马的实力"""
    if defense < attack:
        return "win"
    elif defense > attack:
        return "lose"
    else:
        return "draw"

def find_best_strategy(attack_order, n_horses):
    """找到最佳防守策略"""
    defense_horses = list(range(1, n_horses + 1))
    best_orders = []
    max_wins = -1
    
    # 暴力搜索所有可能的防守顺序
    for defense_order in permutations(defense_horses):
        wins = 0
        draws = 0
        
        # 计算胜场数
        for i in range(n_horses):
            result = compare_horses(defense_order[i], attack_order[i])
            if result == "win":
                wins += 1
            elif result == "draw":
                draws += 1
        
        # 更新最佳策略
        if wins > max_wins:
            max_wins = wins
            best_orders = [(list(defense_order), wins, draws)]
        elif wins == max_wins:
            best_orders.append((list(defense_order), wins, draws))
    
    return best_orders, max_wins

# 计算按钮
with col3:
    st.subheader("🎯 计算防守策略")
    
    if st.button("🚀 计算最佳防守策略", type="primary", use_container_width=True):
        with st.spinner("正在计算最佳策略..."):
            best_orders, max_wins = find_best_strategy(attack_order, n_horses)
            st.session_state.best_orders = best_orders
            st.session_state.max_wins = max_wins
            st.session_state.calculated = True
            st.rerun()
    
    if st.button("🔄 重置计算", use_container_width=True):
        if 'calculated' in st.session_state:
            del st.session_state.calculated
        if 'best_orders' in st.session_state:
            del st.session_state.best_orders
        st.rerun()

# 显示结果
st.markdown("---")

if 'calculated' in st.session_state and st.session_state.calculated:
    best_orders = st.session_state.best_orders
    max_wins = st.session_state.max_wins
    
    st.subheader("🏆 计算结果")
    
    # 显示最佳策略数量
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.metric("最佳策略数量", len(best_orders))
    
    with col_b:
        st.metric("最大胜场数", f"{max_wins}/{n_horses}")
    
    with col_c:
        win_rate = max_wins / n_horses * 100
        st.metric("胜率", f"{win_rate:.1f}%")
    
    # 判断胜负
    if max_wins > n_horses / 2:
        st.success(f"✅ 防守方可以赢得比赛！胜场超过半数")
    elif max_wins == n_horses / 2:
        st.warning(f"⚠️ 防守方最多只能平局，胜场等于半数")
    else:
        st.error(f"❌ 防守方无法赢得比赛，胜场不足半数")
    
    # 显示最佳策略详情
    st.subheader("📋 最佳防守策略详情")
    
    # 使用选项卡展示不同的最佳策略
    tabs = st.tabs([f"策略 {i+1}" for i in range(min(len(best_orders), 5))])
    
    for idx, tab in enumerate(tabs[:len(best_orders)]):
        with tab:
            defense_order, wins, draws = best_orders[idx]
            losses = n_horses - wins - draws
            
            # 策略概览
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("胜场", wins)
            with col2:
                st.metric("平场", draws)
            with col3:
                st.metric("负场", losses)
            
            # 防守方顺序展示
            st.markdown("**防守方派马顺序：**")
            st.markdown(f"```python\n{defense_order}\n```")
            
            # 详细对战表
            st.markdown("**详细对战分析：**")
            
            # 创建HTML表格
            table_html = """
            <style>
            .match-table {
                width: 100%;
                border-collapse: collapse;
                margin: 10px 0;
            }
            .match-table th, .match-table td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: center;
            }
            .match-table th {
                background-color: #3498db;
                color: white;
            }
            .match-table tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .win { background-color: #d4edda !important; }
            .lose { background-color: #f8d7da !important; }
            .draw { background-color: #fff3cd !important; }
            </style>
            
            <table class="match-table">
                <tr>
                    <th>场次</th>
                    <th>防守方马匹</th>
                    <th>进攻方马匹</th>
                    <th>结果</th>
                    <th>实力对比</th>
                </tr>
            """
            
            for i in range(n_horses):
                defense = defense_order[i]
                attack = attack_order[i]
                result = compare_horses(defense, attack)
                
                if result == "win":
                    result_text = "防守方胜"
                    result_class = "win"
                elif result == "lose":
                    result_text = "进攻方胜"
                    result_class = "lose"
                else:
                    result_text = "平局"
                    result_class = "draw"
                
                # 实力对比描述
                if defense < attack:
                    comparison = f"防守方更强 ({defense} < {attack})"
                elif defense > attack:
                    comparison = f"进攻方更强 ({defense} > {attack})"
                else:
                    comparison = f"实力相等 ({defense} = {attack})"
                
                table_html += f"""
                <tr class="{result_class}">
                    <td>第{i+1}场</td>
                    <td><strong>{defense}</strong></td>
                    <td><strong>{attack}</strong></td>
                    <td><strong>{result_text}</strong></td>
                    <td>{comparison}</td>
                </tr>
                """
            
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)
    
    # 显示所有最佳策略的总结
    if len(best_orders) > 1:
        with st.expander("📊 所有最佳策略总结"):
            for idx, (order, wins, draws) in enumerate(best_orders, 1):
                losses = n_horses - wins - draws
                st.markdown(f"**策略 {idx}:** `{order}` | 胜:{wins} 平:{draws} 负:{losses}")
    
    # 策略分析图表
    st.subheader("📈 策略分析")
    
    if len(best_orders) > 0:
        import plotly.graph_objects as go
        
        # 准备数据
        defense_order, wins, draws = best_orders[0]
        losses = n_horses - wins - draws
        
        # 创建饼图
        fig = go.Figure(data=[go.Pie(
            labels=['胜场', '平场', '负场'],
            values=[wins, draws, losses],
            hole=.3,
            marker_colors=['#2ecc71', '#f39c12', '#e74c3c']
        )])
        
        fig.update_layout(
            title="比赛结果分布",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 对战结果条形图
        results = []
        for i in range(n_horses):
            defense = defense_order[i]
            attack = attack_order[i]
            result = compare_horses(defense, attack)
            results.append(1 if result == "win" else (0 if result == "draw" else -1))
        
        fig2 = go.Figure(data=[go.Bar(
            x=list(range(1, n_horses + 1)),
            y=results,
            text=[f"防守方{defense_order[i]}:进攻方{attack_order[i]}" for i in range(n_horses)],
            marker_color=['#2ecc71' if r == 1 else '#f39c12' if r == 0 else '#e74c3c' for r in results]
        )])
        
        fig2.update_layout(
            title="每场比赛结果 (1=胜, 0=平, -1=负)",
            xaxis_title="场次",
            yaxis_title="结果",
            yaxis=dict(range=[-1.5, 1.5]),
            height=300
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
else:
    # 初始状态显示说明
    st.info("👈 请在左侧设置参数，然后点击【计算最佳防守策略】按钮")
    
    # 显示使用说明
    with st.expander("📖 使用说明"):
        st.markdown("""
        ## 如何使用本工具
        
        1. **设置参数** (左侧边栏):
           - 选择马匹数量 (1-6)
           - 为进攻方设置每场比赛的派马顺序
        
        2. **计算策略**:
           - 点击【计算最佳防守策略】按钮
           - 系统会自动计算防守方的最佳应对顺序
        
        3. **分析结果**:
           - 查看防守方的最佳派马顺序
           - 分析每场比赛的胜负情况
           - 查看详细的比赛结果统计
        
        ## 游戏规则
        
        - 双方马匹数量相同
        - 马匹实力：数字越小实力越强 (1号马最强)
        - 相同数字的马匹实力相等
        - 目标：防守方在已知进攻方顺序的情况下，安排自己的马匹出场顺序以获得最大胜场
        
        ## 算法原理
        
        本工具使用**暴力搜索算法**，遍历防守方所有可能的出场顺序排列，找到能获得最多胜场的策略。
        由于马匹数量最多为6，总共有 6! = 720 种可能的排列，计算量在可接受范围内。
        """)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <p>田忌赛马策略计算器 | 基于Streamlit开发 | 马匹数量限制: 1-6</p>
        <p>算法原理：遍历所有可能的防守顺序，找到最大胜场策略</p>
    </div>
    """,
    unsafe_allow_html=True
)
