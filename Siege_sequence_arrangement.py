import streamlit as st
from itertools import permutations
import pandas as pd

# 设置页面
st.set_page_config(
    page_title="田忌赛马策略计算器——1",
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

# 初始化实力等级
if 'attack_horse_levels' not in st.session_state:
    st.session_state.attack_horse_levels = list(range(st.session_state.num_horses))

if 'defense_horse_levels' not in st.session_state:
    st.session_state.defense_horse_levels = list(range(st.session_state.num_horses))

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
                # 初始化实力等级
                st.session_state.attack_horse_levels = list(range(st.session_state.num_horses))
                st.session_state.defense_horse_levels = list(range(st.session_state.num_horses))
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
                    # 更新实力等级
                    st.session_state.attack_horse_levels.pop(i)
                    st.session_state.defense_horse_levels.pop(i)
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
                # 更新实力等级
                st.session_state.attack_horse_levels.pop()
                st.session_state.defense_horse_levels.pop()
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
**使用方法：** 为每匹马指定一个实力等级（数字）。等级数字越小，实力越强。
实力等级相同的马匹实力相当。等级数字可以重复，表示实力相当。
""")

# 创建战力对比界面
st.markdown("### 设置马匹实力等级")

# 创建两列显示进攻方和防守方
col_attack_power, col_defense_power = st.columns(2)

with col_attack_power:
    st.markdown("**进攻方马匹实力等级:**")
    for i in range(st.session_state.num_horses):
        col_level = st.columns([3, 2])
        with col_level[0]:
            st.markdown(f"{st.session_state.attack_horse_names[i]}")
        with col_level[1]:
            # 实力等级选择器，数字越小实力越强
            level = st.selectbox(
                "实力等级",
                options=list(range(1, st.session_state.num_horses + 1)),
                index=st.session_state.attack_horse_levels[i],
                key=f"attack_level_{i}",
                label_visibility="collapsed"
            )
            if level != st.session_state.attack_horse_levels[i] + 1:
                st.session_state.attack_horse_levels[i] = level - 1

with col_defense_power:
    st.markdown("**防守方马匹实力等级:**")
    for i in range(st.session_state.num_horses):
        col_level = st.columns([3, 2])
        with col_level[0]:
            st.markdown(f"{st.session_state.defense_horse_names[i]}")
        with col_level[1]:
            level = st.selectbox(
                "实力等级",
                options=list(range(1, st.session_state.num_horses + 1)),
                index=st.session_state.defense_horse_levels[i],
                key=f"defense_level_{i}",
                label_visibility="collapsed"
            )
            if level != st.session_state.defense_horse_levels[i] + 1:
                st.session_state.defense_horse_levels[i] = level - 1

# 可视化战力对比
st.markdown("### 战力对比可视化")

# 创建可视化图表
def create_power_chart():
    # 收集所有马匹数据
    all_horses = []
    
    # 进攻方马匹
    for i in range(st.session_state.num_horses):
        all_horses.append({
            "马匹": st.session_state.attack_horse_names[i],
            "阵营": "进攻方",
            "实力等级": st.session_state.attack_horse_levels[i],
            "显示等级": st.session_state.attack_horse_levels[i] + 1  # 显示给用户的等级（1开始）
        })
    
    # 防守方马匹
    for i in range(st.session_state.num_horses):
        all_horses.append({
            "马匹": st.session_state.defense_horse_names[i],
            "阵营": "防守方",
            "实力等级": st.session_state.defense_horse_levels[i],
            "显示等级": st.session_state.defense_horse_levels[i] + 1
        })
    
    # 创建DataFrame
    df = pd.DataFrame(all_horses)
    
    # 按实力等级排序
    df = df.sort_values(by=["实力等级", "阵营"])
    
    # 创建文本可视化
    st.markdown("**战力排行榜 (从上到下，实力递减):**")
    
    # 获取唯一的实力等级并排序
    unique_levels = sorted(df["实力等级"].unique())
    
    for level in unique_levels:
        level_horses = df[df["实力等级"] == level]
        level_display = level + 1
        
        if len(level_horses) == 1:
            horse = level_horses.iloc[0]
            st.markdown(f"**第{level_display}层:** {horse['马匹']} ({horse['阵营']})")
        else:
            horse_names = [f"{row['马匹']} ({row['阵营']})" for _, row in level_horses.iterrows()]
            st.markdown(f"**第{level_display}层:** {', '.join(horse_names)} (实力相当)")
        
        # 添加分隔线（最后一层不添加）
        if level != unique_levels[-1]:
            st.markdown("---")

create_power_chart()

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
    horse_level = st.session_state.attack_horse_levels[horse_idx] + 1
    order_display.append(f"第{i+1}场: **{horse_name}** (等级{horse_level})")

st.markdown(" | ".join(order_display))

# 核心算法函数
def compare_horses(defense_idx, attack_idx):
    """比较两匹马的实力，使用用户设置的实力等级"""
    defense_level = st.session_state.defense_horse_levels[defense_idx]
    attack_level = st.session_state.attack_horse_levels[attack_idx]
    
    if defense_level < attack_level:  # 等级数字越小实力越强
        return "win"  # 防守方胜
    elif defense_level > attack_level:
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
            defense_order_names = []
            for idx in defense_order:
                horse_name = st.session_state.defense_horse_names[idx]
                horse_level = st.session_state.defense_horse_levels[idx] + 1
                defense_order_names.append(f"{horse_name} (等级{horse_level})")
            
            order_display = []
            for i, horse_info in enumerate(defense_order_names):
                order_display.append(f"第{i+1}场: **{horse_info}**")
            
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
            
            # 创建表格数据
            table_data = []
            
            for i in range(num_horses):
                defense_idx = defense_order[i]
                attack_idx = attack_order[i]
                
                defense_horse_name = st.session_state.defense_horse_names[defense_idx]
                defense_horse_level = st.session_state.defense_horse_levels[defense_idx] + 1
                
                attack_horse_name = st.session_state.attack_horse_names[attack_idx]
                attack_horse_level = st.session_state.attack_horse_levels[attack_idx] + 1
                
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
                if defense_horse_level < attack_horse_level:
                    comparison = f"防守方更强 (等级{defense_horse_level} > 等级{attack_horse_level})"
                elif defense_horse_level > attack_horse_level:
                    comparison = f"进攻方更强 (等级{defense_horse_level} < 等级{attack_horse_level})"
                else:
                    comparison = f"实力相等 (等级{defense_horse_level} = 等级{attack_horse_level})"
                
                table_data.append({
                    "场次": f"第{i+1}场",
                    "防守方马匹": f"{defense_horse_name} (等级{defense_horse_level})",
                    "进攻方马匹": f"{attack_horse_name} (等级{attack_horse_level})",
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
                        order_levels = [st.session_state.defense_horse_levels[i] + 1 for i in order]
                        order_with_levels = [f"{name}(等级{level})" for name, level in zip(order_names, order_levels)]
                        st.markdown(f"**策略 {idx}:** {order_with_levels} (胜:{wins} 平:{draws})")

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
           - 为每匹马指定实力等级（1到马匹数量）
           - **等级数字越小，实力越强**
           - 等级相同的马匹实力相当
           - 等级数字可以重复，表示实力相当
        
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
        
        - **等级数字越小，实力越强** (等级1最强)
        - 相同等级的马匹实力相等
        - 防守方马等级 < 进攻方马等级 → 防守方胜
        - 防守方马等级 > 进攻方马等级 → 进攻方胜
        - 防守方马等级 = 进攻方马等级 → 平局
        
        **实力对比说明：**
        - "防守方更强 (等级2 > 等级3)" 表示防守方马的等级2比进攻方马的等级3更高（实力更强）
        - "进攻方更强 (等级4 < 等级1)" 表示进攻方马的等级1比防守方马的等级4更高（实力更强）
        
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
