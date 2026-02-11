import streamlit as st
from itertools import permutations
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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
    st.session_state.attack_order = [0, 1, 2]

# 初始化实力位置（格子编号），0表示未分配，1~2N表示格子位置
if 'horse_positions' not in st.session_state:
    st.session_state.horse_positions = {
        'attack': {i: 0 for i in range(st.session_state.num_horses)},
        'defense': {i: 0 for i in range(st.session_state.num_horses)}
    }

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
                # 初始化实力位置
                st.session_state.horse_positions['attack'][st.session_state.num_horses-1] = 0
                st.session_state.horse_positions['defense'][st.session_state.num_horses-1] = 0
                st.rerun()
            else:
                st.warning("最多只能有6匹马！")
    
    # 为每匹马命名
    st.markdown("**为每匹马命名:**")
    
    for i in range(st.session_state.num_horses):
        col_name = st.columns([1, 4, 1])
        
        with col_name[0]:
            st.markdown(f"**马{i+1}:**")
        
        with col_name[1]:
            new_name = st.text_input(
                f"进攻方马匹{i+1}名称",
                value=st.session_state.attack_horse_names[i],
                key=f"attack_name_{i}",
                label_visibility="collapsed"
            )
            if new_name != st.session_state.attack_horse_names[i]:
                st.session_state.attack_horse_names[i] = new_name
        
        with col_name[2]:
            if i >= 2:
                if st.button("🗑️", key=f"remove_attack_{i}"):
                    # 删除马匹
                    st.session_state.num_horses -= 1
                    st.session_state.attack_horse_names.pop(i)
                    st.session_state.defense_horse_names.pop(i)
                    # 更新进攻方顺序
                    st.session_state.attack_order = [x if x < i else x-1 for x in st.session_state.attack_order if x != i]
                    # 更新实力位置
                    st.session_state.horse_positions['attack'].pop(i)
                    st.session_state.horse_positions['defense'].pop(i)
                    st.rerun()
            else:
                st.empty()

# 右侧：防守方设置
with col2:
    st.subheader("🛡️ 防守方设置")
    
    # 马匹数量显示
    col2_1, col2_2 = st.columns([3, 1])
    
    with col2_1:
        st.markdown("**马匹数量:**")
    
    with col2_2:
        # 删除马匹按钮
        if st.button("➖ 删除马匹", key="remove_defense"):
            if st.session_state.num_horses > 2:
                st.session_state.num_horses -= 1
                st.session_state.attack_horse_names.pop()
                st.session_state.defense_horse_names.pop()
                # 更新进攻方顺序
                st.session_state.attack_order = [x for x in st.session_state.attack_order if x < st.session_state.num_horses]
                # 更新实力位置
                attack_keys = list(st.session_state.horse_positions['attack'].keys())
                defense_keys = list(st.session_state.horse_positions['defense'].keys())
                st.session_state.horse_positions['attack'].pop(attack_keys[-1])
                st.session_state.horse_positions['defense'].pop(defense_keys[-1])
                st.rerun()
            else:
                st.warning("至少需要2匹马！")
    
    # 为防守方马匹命名
    st.markdown("**为每匹马命名:**")
    
    for i in range(st.session_state.num_horses):
        col_name = st.columns([1, 4])
        
        with col_name[0]:
            st.markdown(f"**马{i+1}:**")
        
        with col_name[1]:
            new_name = st.text_input(
                f"防守方马匹{i+1}名称",
                value=st.session_state.defense_horse_names[i],
                key=f"defense_name_{i}",
                label_visibility="collapsed"
            )
            if new_name != st.session_state.defense_horse_names[i]:
                st.session_state.defense_horse_names[i] = new_name

# 双方战力对比
st.markdown("---")
st.subheader("📊 双方战力对比")

st.markdown("""
**使用方法：** 将每匹马拖放到格子中（通过选择格子编号）。格子从上到下编号（1在最上方，实力最强）。
如果两匹马在同一个格子中，则实力相当。在更上方格子中的马实力更强。
""")

# 计算总格子数（双方马匹数量总和）
total_slots = st.session_state.num_horses * 2

# 创建战力对比界面
st.markdown("### 设置马匹实力位置")

# 创建两列显示进攻方和防守方
col_attack_power, col_defense_power = st.columns(2)

with col_attack_power:
    st.markdown("**进攻方马匹位置:**")
    for i in range(st.session_state.num_horses):
        col_pos = st.columns([3, 2])
        with col_pos[0]:
            st.markdown(f"{st.session_state.attack_horse_names[i]}")
        with col_pos[1]:
            # 格子位置选择器，1在最上方，实力最强
            position = st.selectbox(
                "格子位置",
                options=["未分配"] + list(range(1, total_slots + 1)),
                index=st.session_state.horse_positions['attack'][i] if st.session_state.horse_positions['attack'][i] > 0 else 0,
                key=f"attack_position_{i}",
                label_visibility="collapsed"
            )
            if position == "未分配":
                st.session_state.horse_positions['attack'][i] = 0
            else:
                st.session_state.horse_positions['attack'][i] = position

with col_defense_power:
    st.markdown("**防守方马匹位置:**")
    for i in range(st.session_state.num_horses):
        col_pos = st.columns([3, 2])
        with col_pos[0]:
            st.markdown(f"{st.session_state.defense_horse_names[i]}")
        with col_pos[1]:
            position = st.selectbox(
                "格子位置",
                options=["未分配"] + list(range(1, total_slots + 1)),
                index=st.session_state.horse_positions['defense'][i] if st.session_state.horse_positions['defense'][i] > 0 else 0,
                key=f"defense_position_{i}",
                label_visibility="collapsed"
            )
            if position == "未分配":
                st.session_state.horse_positions['defense'][i] = 0
            else:
                st.session_state.horse_positions['defense'][i] = position

# 可视化战力对比 - 使用Plotly创建格子图
st.markdown("### 战力对比可视化")

def create_slot_visualization():
    """创建格子可视化图表"""
    
    # 收集数据
    data = []
    
    # 收集进攻方马匹
    for i in range(st.session_state.num_horses):
        pos = st.session_state.horse_positions['attack'][i]
        if pos > 0:
            data.append({
                '阵营': '进攻方',
                '马匹': st.session_state.attack_horse_names[i],
                '格子位置': pos,
                '马匹索引': i,
                '颜色': '#FF6B6B'  # 进攻方红色
            })
    
    # 收集防守方马匹
    for i in range(st.session_state.num_horses):
        pos = st.session_state.horse_positions['defense'][i]
        if pos > 0:
            data.append({
                '阵营': '防守方',
                '马匹': st.session_state.defense_horse_names[i],
                '格子位置': pos,
                '马匹索引': i,
                '颜色': '#4ECDC4'  # 防守方青色
            })
    
    if not data:
        st.warning("请为马匹分配格子位置")
        return
    
    # 创建图表
    fig = go.Figure()
    
    # 添加格子线
    for slot in range(1, total_slots + 1):
        # 格子背景
        fig.add_shape(
            type="rect",
            xref="paper",
            yref="y",
            x0=0,
            x1=1,
            y0=slot - 0.4,
            y1=slot + 0.4,
            fillcolor="rgba(200, 200, 200, 0.2)",
            line=dict(color="rgba(150, 150, 150, 0.5)", width=1),
            layer="below"
        )
        
        # 格子编号
        fig.add_annotation(
            x=0.02,
            y=slot,
            text=f"格子 {slot}",
            showarrow=False,
            font=dict(size=10, color="gray"),
            xanchor="left",
            yanchor="middle"
        )
    
    # 添加马匹标记
    for item in data:
        # 根据阵营确定x位置
        if item['阵营'] == '进攻方':
            x_pos = 0.25
        else:
            x_pos = 0.75
        
        # 添加马匹标记
        fig.add_trace(go.Scatter(
            x=[x_pos],
            y=[item['格子位置']],
            mode="markers+text",
            marker=dict(
                size=30,
                color=item['颜色'],
                line=dict(width=2, color="white")
            ),
            text=[item['马匹'].replace('进攻方', '').replace('防守方', '')],
            textposition="middle center",
            textfont=dict(color="white", size=10, weight="bold"),
            name=item['阵营'],
            hovertemplate=f"<b>{item['马匹']}</b><br>阵营: {item['阵营']}<br>格子位置: {item['格子位置']}<extra></extra>"
        ))
    
    # 更新图表布局
    fig.update_layout(
        title="战力对比格子图 (位置越高，实力越强)",
        xaxis=dict(
            range=[0, 1],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            title=None
        ),
        yaxis=dict(
            range=[0.5, total_slots + 0.5],
            autorange="reversed",  # 反转y轴，使1在最上方
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            title="实力等级 (↑更强)"
        ),
        height=400,
        showlegend=True,
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        annotations=[
            dict(
                x=0.25,
                y=total_slots + 0.7,
                text="进攻方",
                showarrow=False,
                font=dict(size=12, color="#FF6B6B", weight="bold"),
                xanchor="center"
            ),
            dict(
                x=0.75,
                y=total_slots + 0.7,
                text="防守方",
                showarrow=False,
                font=dict(size=12, color="#4ECDC4", weight="bold"),
                xanchor="center"
            )
        ]
    )
    
    # 添加分隔线
    fig.add_shape(
        type="line",
        xref="paper",
        yref="paper",
        x0=0.5,
        x1=0.5,
        y0=0,
        y1=1,
        line=dict(color="gray", width=1, dash="dash"),
    )
    
    st.plotly_chart(fig, use_container_width=True)

# 显示可视化
create_slot_visualization()

# 进攻方出场顺序设置
st.markdown("---")
st.subheader("🎯 进攻方出场顺序设置")

st.markdown("请为进攻方选择每场比赛的出赛马匹（每匹马只能使用一次）：")

# 创建进攻方出场顺序选择
remaining_horses = list(range(st.session_state.num_horses))

# 检查是否有重复选择
if len(set(st.session_state.attack_order)) != len(st.session_state.attack_order):
    st.error("每匹马只能出场一次！请重新选择。")
    st.session_state.attack_order = list(range(st.session_state.num_horses))
    st.rerun()

# 创建出场顺序选择器
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
        
        new_attack_order.append(selected_horse)

# 显示进攻方出场顺序
st.markdown("### 当前进攻方出场顺序:")
order_display = []
for i, horse_idx in enumerate(st.session_state.attack_order):
    horse_name = st.session_state.attack_horse_names[horse_idx]
    # 获取马匹的格子位置
    horse_position = st.session_state.horse_positions['attack'][horse_idx]
    pos_text = f"(格子{horse_position})" if horse_position > 0 else "(未分配位置)"
    order_display.append(f"第{i+1}场: **{horse_name}** {pos_text}")

st.markdown(" | ".join(order_display))

# 核心算法函数
def compare_horses(defense_idx, attack_idx):
    """比较两匹马的实力，根据格子位置"""
    defense_pos = st.session_state.horse_positions['defense'][defense_idx]
    attack_pos = st.session_state.horse_positions['attack'][attack_idx]
    
    # 如果有马匹未分配位置，按最弱处理
    if defense_pos == 0:
        defense_pos = total_slots + 1  # 未分配视为最弱
    if attack_pos == 0:
        attack_pos = total_slots + 1  # 未分配视为最弱
    
    # 格子位置越小（越靠上）实力越强
    if defense_pos < attack_pos:  # 防守方位置更靠上
        return "win"  # 防守方胜
    elif defense_pos > attack_pos:
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
        # 检查是否所有马匹都已分配位置
        attack_missing = sum(1 for i in range(st.session_state.num_horses) 
                           if st.session_state.horse_positions['attack'][i] == 0)
        defense_missing = sum(1 for i in range(st.session_state.num_horses) 
                            if st.session_state.horse_positions['defense'][i] == 0)
        
        if attack_missing > 0 or defense_missing > 0:
            st.error(f"请先为所有马匹分配格子位置！进攻方还有{attack_missing}匹未分配，防守方还有{defense_missing}匹未分配。")
        else:
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
            defense_order_info = []
            for i, idx in enumerate(defense_order):
                horse_name = st.session_state.defense_horse_names[idx]
                horse_position = st.session_state.horse_positions['defense'][idx]
                defense_order_info.append(f"第{i+1}场: **{horse_name}** (格子{horse_position})")
            
            st.markdown(" | ".join(defense_order_info))
            
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
            
            # 创建表格数据
            table_data = []
            
            for i in range(num_horses):
                defense_idx = defense_order[i]
                attack_idx = attack_order[i]
                
                defense_horse_name = st.session_state.defense_horse_names[defense_idx]
                defense_horse_pos = st.session_state.horse_positions['defense'][defense_idx]
                
                attack_horse_name = st.session_state.attack_horse_names[attack_idx]
                attack_horse_pos = st.session_state.horse_positions['attack'][attack_idx]
                
                result = compare_horses(defense_idx, attack_idx)
                
                # 确定结果文本
                if result == "win":
                    result_text = "防守方胜"
                    result_color = "🟢"
                elif result == "lose":
                    result_text = "进攻方胜"
                    result_color = "🔴"
                else:
                    result_text = "平局"
                    result_color = "🟡"
                
                # 实力对比描述
                if defense_horse_pos < attack_horse_pos:
                    comparison = f"防守方更强 (格子{defense_horse_pos}在上方)"
                elif defense_horse_pos > attack_horse_pos:
                    comparison = f"进攻方更强 (格子{attack_horse_pos}在上方)"
                else:
                    comparison = f"实力相等 (同在格子{defense_horse_pos})"
                
                table_data.append({
                    "场次": f"第{i+1}场",
                    "防守方马匹": f"{defense_horse_name} (格子{defense_horse_pos})",
                    "进攻方马匹": f"{attack_horse_name} (格子{attack_horse_pos})",
                    "比赛结果": f"{result_color} {result_text}",
                    "实力对比": comparison
                })
            
            # 使用Streamlit的dataframe显示表格，添加样式
            df = pd.DataFrame(table_data)
            
            # 设置表格样式
            def color_rows(row):
                if "防守方胜" in row["比赛结果"]:
                    return ['background-color: #d4edda'] * len(row)
                elif "进攻方胜" in row["比赛结果"]:
                    return ['background-color: #f8d7da'] * len(row)
                else:
                    return ['background-color: #fff3cd'] * len(row)
            
            # 应用样式并显示表格
            styled_df = df.style.apply(color_rows, axis=1)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            # 显示其他最佳策略
            if len(best_strategies) > 1:
                with st.expander(f"查看其他 {len(best_strategies)-1} 种最佳策略"):
                    for idx, (order, wins, draws) in enumerate(best_strategies[1:], 2):
                        order_names = [st.session_state.defense_horse_names[i] for i in order]
                        order_positions = [st.session_state.horse_positions['defense'][i] for i in order]
                        order_info = [f"{name}(格子{pos})" for name, pos in zip(order_names, order_positions)]
                        st.markdown(f"**策略 {idx}:** {order_info} (胜:{wins} 平:{draws})")

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
        
        3. **设置双方战力对比**
           - 为每匹马选择一个格子位置（1~12）
           - **格子编号越小，位置越高，实力越强**
           - 相同格子中的马匹实力相当
           - 在更上方格子中的马实力更强
           - 使用下拉菜单为每匹马选择格子位置
        
        4. **设置进攻方出场顺序**
           - 为进攻方选择每场比赛的出赛马匹
           - 每匹马只能出场一次
        
        5. **计算防守策略**
           - 点击"计算最佳防守策略"按钮
           - 系统会自动计算出防守方的最佳出场顺序
        
        6. **分析结果**
           - 查看防守方的最佳出场顺序
           - 分析每场比赛的胜负情况
           - 查看比赛预测和统计信息
        
        ### 实力规则
        
        - **格子位置越靠上（编号越小），实力越强**
        - 相同格子中的马匹实力相等（会形成平局）
        - 防守方马格子位置 < 进攻方马格子位置 → 防守方胜
        - 防守方马格子位置 > 进攻方马格子位置 → 进攻方胜
        - 防守方马格子位置 = 进攻方马格子位置 → 平局
        
        **实力对比说明：**
        - "防守方更强 (格子2在上方)" 表示防守方马在格子2，进攻方马在更下方的格子
        - "进攻方更强 (格子1在上方)" 表示进攻方马在格子1，防守方马在更下方的格子
        
        **现在，请先设置马匹、战力对比和进攻方顺序，然后点击"计算最佳防守策略"按钮开始！**
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
