import streamlit as st
from itertools import permutations
import pandas as pd

# ---------- 页面配置 ----------
st.set_page_config(
    page_title="守城车头卡秒顺序计算器",
    page_icon="🐎",
    layout="wide"
)

st.title("🐎 守城车头卡秒顺序计算器")
st.markdown("---")

# ---------- 辅助函数：获取默认显示名称 ----------
def get_attack_name(idx: int) -> str:
    """如果用户未输入，返回 'X号车头'"""
    name = st.session_state.attack_horse_names[idx]
    return name if name.strip() else f"{idx+1}号车头"

def get_defense_name(idx: int) -> str:
    name = st.session_state.defense_horse_names[idx]
    return name if name.strip() else f"{idx+1}号车头"

# ---------- 初始化会话状态 ----------
def init_default_state():
    """设置所有自定义变量为默认值（3匹马，名称为空字符串）"""
    if 'num_horses' not in st.session_state:
        st.session_state.num_horses = 3
    if 'attack_horse_names' not in st.session_state:
        st.session_state.attack_horse_names = [""] * 3   # 初始为空，显示时自动转为“1号车头”等
    if 'defense_horse_names' not in st.session_state:
        st.session_state.defense_horse_names = [""] * 3
    if 'attack_order' not in st.session_state:
        st.session_state.attack_order = [0, 1, 2]
    
    total_slots = st.session_state.num_horses * 2
    if 'slot_selections' not in st.session_state:
        st.session_state.slot_selections = {
            'attack': [None] * total_slots,
            'defense': [None] * total_slots
        }

init_default_state()

# ---------- 回调函数：格子选择变化时的冲突处理 ----------
def on_slot_change(side: str, slot_idx: int):
    widget_key = f"{side}_slot_{slot_idx}"
    new_val = st.session_state[widget_key]
    total_slots = st.session_state.num_horses * 2

    internal_val = None if new_val == "空" else new_val

    if internal_val is not None:
        for other_idx in range(total_slots):
            if other_idx == slot_idx:
                continue
            other_widget_key = f"{side}_slot_{other_idx}"
            other_val = st.session_state.get(other_widget_key)
            if other_val == internal_val:
                st.session_state[other_widget_key] = "空"
                st.session_state.slot_selections[side][other_idx] = None

    st.session_state.slot_selections[side][slot_idx] = internal_val

    if 'calculate_clicked' in st.session_state:
        del st.session_state.calculate_clicked

# ---------- 左侧：进攻方设置（紧凑按钮）----------
col1, col2 = st.columns(2)
with col1:
    st.subheader("🐓 进攻方设置")
    for i in range(st.session_state.num_horses):
        cols = st.columns([1, 4])          # 只保留两列：标签 + 输入框
        with cols[0]:
            st.markdown(f"**{i+1}号车头:**")   # 标签改为“1号车头”等
        with cols[1]:
            # 输入框初始值为空字符串，用户可立即输入
            new_name = st.text_input(
                f"进攻方车头{i+1}名称",
                value=st.session_state.attack_horse_names[i],
                key=f"attack_name_{i}",
                label_visibility="collapsed",
                placeholder=f"输入{i+1}号车头名称（留空则默认）"
            )
            if new_name != st.session_state.attack_horse_names[i]:
                st.session_state.attack_horse_names[i] = new_name
                if 'calculate_clicked' in st.session_state:
                    del st.session_state.calculate_clicked

    # ---------- 添加/删除按钮（紧凑并排）----------
    col_btn1, col_btn2, _ = st.columns([0.2, 0.2, 0.6])  # 两个小列放按钮，剩余空间留白
    with col_btn1:
        if st.button("添加", key="add_attack"):
            if st.session_state.num_horses < 6:
                st.session_state.num_horses += 1
                # 新增马匹名称初始为空
                st.session_state.attack_horse_names.append("")
                st.session_state.defense_horse_names.append("")
                st.session_state.attack_order = list(range(st.session_state.num_horses))
                total_slots = st.session_state.num_horses * 2
                st.session_state.slot_selections = {
                    'attack': [None] * total_slots,
                    'defense': [None] * total_slots
                }
                for j in range(total_slots):
                    st.session_state[f"attack_slot_{j}"] = "空"
                    st.session_state[f"defense_slot_{j}"] = "空"
                if 'calculate_clicked' in st.session_state:
                    del st.session_state.calculate_clicked
                st.rerun()
            else:
                st.warning("最多只能有6匹马！")
    with col_btn2:
        if st.button("删除", key="remove_defense_global"):
            if st.session_state.num_horses > 2:
                st.session_state.num_horses -= 1
                st.session_state.attack_horse_names.pop()
                st.session_state.defense_horse_names.pop()
                st.session_state.attack_order = [x for x in st.session_state.attack_order if x < st.session_state.num_horses]
                total_slots = st.session_state.num_horses * 2
                st.session_state.slot_selections = {
                    'attack': [None] * total_slots,
                    'defense': [None] * total_slots
                }
                for j in range(total_slots):
                    st.session_state[f"attack_slot_{j}"] = "空"
                    st.session_state[f"defense_slot_{j}"] = "空"
                if 'calculate_clicked' in st.session_state:
                    del st.session_state.calculate_clicked
                st.rerun()
            else:
                st.warning("至少需要2匹马！")

# ---------- 右侧：防守方设置 ----------
with col2:
    st.subheader("🛡️ 防守方设置")
    for i in range(st.session_state.num_horses):
        cols = st.columns([1, 4])
        with cols[0]:
            st.markdown(f"**{i+1}号车头:**")
        with cols[1]:
            new_name = st.text_input(
                f"防守方车头{i+1}名称",
                value=st.session_state.defense_horse_names[i],
                key=f"defense_name_{i}",
                label_visibility="collapsed",
                placeholder=f"输入{i+1}号车头名称（留空则默认）"
            )
            if new_name != st.session_state.defense_horse_names[i]:
                st.session_state.defense_horse_names[i] = new_name
                if 'calculate_clicked' in st.session_state:
                    del st.session_state.calculate_clicked

# ---------- 双方战力对比 ----------
st.markdown("---")
st.subheader("📊 双方战力对比")
st.markdown("越靠上面战力越强，左边进攻右边防守")  

total_slots = st.session_state.num_horses * 2
available_options = ["空"] + list(range(st.session_state.num_horses))

col_attack_power, col_defense_power = st.columns(2)

# ----- 进攻方格子选择 -----
with col_attack_power:
    for slot_idx in range(total_slots):
        current = st.session_state.slot_selections['attack'][slot_idx]
        default_index = 0 if current is None else current + 1

        st.selectbox(
            f"格子{slot_idx+1}",
            options=available_options,
            index=default_index,
            format_func=lambda x: "空" if x == "空" else get_attack_name(x),  # 使用默认名称
            key=f"attack_slot_{slot_idx}",
            on_change=lambda s='attack', idx=slot_idx: on_slot_change(s, idx),
            label_visibility="collapsed"
        )

# ----- 防守方格子选择 -----
with col_defense_power:
    for slot_idx in range(total_slots):
        current = st.session_state.slot_selections['defense'][slot_idx]
        default_index = 0 if current is None else current + 1

        st.selectbox(
            f"格子{slot_idx+1}",
            options=available_options,
            index=default_index,
            format_func=lambda x: "空" if x == "空" else get_defense_name(x),
            key=f"defense_slot_{slot_idx}",
            on_change=lambda s='defense', idx=slot_idx: on_slot_change(s, idx),
            label_visibility="collapsed"
        )

# ---------- 进攻方出场顺序设置 ----------
st.markdown("---")
st.subheader("🎯 进攻方出场顺序设置")

new_attack_order = []
for i in range(st.session_state.num_horses):
    col_order = st.columns([1, 4])
    with col_order[0]:
        st.markdown(f"**第{i+1}场:**")
    with col_order[1]:
        available_horses = [h for h in range(st.session_state.num_horses) if h not in new_attack_order]
        if st.session_state.attack_order[i] not in available_horses and available_horses:
            st.session_state.attack_order[i] = available_horses[0]
            st.rerun()
        selected_horse = st.selectbox(
            f"选择第{i+1}场比赛的马匹",
            options=available_horses,
            index=available_horses.index(st.session_state.attack_order[i]) if st.session_state.attack_order[i] in available_horses else 0,
            format_func=lambda x: get_attack_name(x),   # 使用默认名称
            key=f"attack_order_{i}",
            label_visibility="collapsed"
        )
        if selected_horse != st.session_state.attack_order[i]:
            st.session_state.attack_order[i] = selected_horse
            if 'calculate_clicked' in st.session_state:
                del st.session_state.calculate_clicked
        new_attack_order.append(selected_horse)

if len(set(st.session_state.attack_order)) != len(st.session_state.attack_order):
    st.error("每匹马只能出场一次！请重新选择。")
    st.session_state.attack_order = list(range(st.session_state.num_horses))
    st.rerun()

# ---------- 核心算法函数 ----------
def get_horse_position(side, horse_idx):
    total_slots = st.session_state.num_horses * 2
    for slot_idx in range(total_slots):
        if st.session_state.slot_selections[side][slot_idx] == horse_idx:
            return slot_idx + 1
    return None

def compare_horses(defense_idx, attack_idx):
    total_slots = st.session_state.num_horses * 2
    defense_pos = get_horse_position('defense', defense_idx)
    attack_pos = get_horse_position('attack', attack_idx)

    if defense_pos is None:
        defense_pos = total_slots + 1
    if attack_pos is None:
        attack_pos = total_slots + 1

    if defense_pos < attack_pos:
        return "win"
    elif defense_pos > attack_pos:
        return "lose"
    else:
        return "draw"

def find_best_strategies(attack_order, num_horses):
    defense_horses = list(range(num_horses))
    best_strategies = []
    max_wins = -1
    best_advantage = -float('inf')

    for defense_order in permutations(defense_horses):
        wins = 0
        draws = 0
        advantage_sum = 0

        for i in range(num_horses):
            d_idx = defense_order[i]
            a_idx = attack_order[i]
            result = compare_horses(d_idx, a_idx)
            if result == "win":
                wins += 1
                d_pos = get_horse_position('defense', d_idx)
                a_pos = get_horse_position('attack', a_idx)
                advantage_sum += a_pos - d_pos
            elif result == "draw":
                draws += 1

        if wins > max_wins:
            max_wins = wins
            best_advantage = advantage_sum
            best_strategies = [(list(defense_order), wins, draws, advantage_sum)]
        elif wins == max_wins:
            if advantage_sum > best_advantage:
                best_advantage = advantage_sum
                best_strategies = [(list(defense_order), wins, draws, advantage_sum)]
            elif advantage_sum == best_advantage:
                best_strategies.append((list(defense_order), wins, draws, advantage_sum))

    return best_strategies, max_wins

# ---------- 计算按钮 ----------
st.markdown("---")
col_btn1, _ = st.columns([1, 3])
with col_btn1:
    if st.button("🚀 计算最佳防守策略", type="primary", use_container_width=True):
        attack_missing = sum(1 for i in range(st.session_state.num_horses) if get_horse_position('attack', i) is None)
        defense_missing = sum(1 for i in range(st.session_state.num_horses) if get_horse_position('defense', i) is None)
        if attack_missing > 0 or defense_missing > 0:
            st.error(f"请先为所有马匹分配格子！进攻方还有 {attack_missing} 匹未分配，防守方还有 {defense_missing} 匹未分配。")
        else:
            st.session_state.calculate_clicked = True

# ---------- 显示计算结果 ----------
if st.session_state.get('calculate_clicked', False):
    num_horses = st.session_state.num_horses
    attack_order = st.session_state.attack_order

    with st.spinner("正在计算最佳防守策略..."):
        best_strategies, max_wins = find_best_strategies(attack_order, num_horses)

        st.markdown("---")
        st.subheader("🏆 计算结果")

        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.metric("最佳策略数量", len(best_strategies))
        with col_stat2:
            st.metric("最大胜场数", f"{max_wins}/{num_horses}")
        with col_stat3:
            win_rate = (max_wins / num_horses) * 100
            st.metric("胜率", f"{win_rate:.1f}%")

        st.markdown("### 📈 比赛预测")
        if max_wins > num_horses / 2:
            st.success(f"✅ **防守方可以赢得比赛！** (胜场数: {max_wins}/{num_horses})")
        elif max_wins == num_horses / 2 and num_horses % 2 == 0:
            st.warning(f"⚠️ **比赛可能平局** (胜场数: {max_wins}/{num_horses})")
        else:
            st.error(f"❌ **防守方难以赢得比赛** (胜场数: {max_wins}/{num_horses})")

        st.markdown("### 🛡️ 最佳防守策略")
        if best_strategies:
            defense_order, wins, draws, _ = best_strategies[0]
            losses = num_horses - wins - draws

            st.markdown("**防守方出场顺序:**")
            defense_order_info = []
            for i, idx in enumerate(defense_order):
                horse_name = get_defense_name(idx)   # 只显示名称，不带格子
                defense_order_info.append(f"第{i+1}场: **{horse_name}**")
            st.markdown(" | ".join(defense_order_info))

            col_win, col_draw, col_lose = st.columns(3)
            with col_win:
                st.markdown(f"**{wins}** 胜")
            with col_draw:
                st.markdown(f"**{draws}** 平")
            with col_lose:
                st.markdown(f"**{losses}** 负")

            st.markdown("#### 📋 详细对战分析")
            table_data = []
            for i in range(num_horses):
                d_idx = defense_order[i]
                a_idx = attack_order[i]
                d_name = get_defense_name(d_idx)      # 只显示名称
                a_name = get_attack_name(a_idx)       # 只显示名称
                result = compare_horses(d_idx, a_idx)

                if result == "win":
                    result_text = "防守方胜"
                    result_color = "🟢"
                elif result == "lose":
                    result_text = "进攻方胜"
                    result_color = "🔴"
                else:
                    result_text = "平局"
                    result_color = "🟡"

                table_data.append({
                    "场次": f"第{i+1}场",
                    "防守方马匹": d_name,
                    "进攻方马匹": a_name,
                    "比赛结果": f"{result_color} {result_text}"
                })

            df = pd.DataFrame(table_data)
            def color_rows(row):
                if "防守方胜" in row["比赛结果"]:
                    return ['background-color: #d4edda'] * len(row)
                elif "进攻方胜" in row["比赛结果"]:
                    return ['background-color: #f8d7da'] * len(row)
                else:
                    return ['background-color: #fff3cd'] * len(row)

            styled_df = df.style.apply(color_rows, axis=1)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

            if len(best_strategies) > 1:
                with st.expander(f"查看其他 {len(best_strategies)-1} 种最佳策略"):
                    for idx, (order, w, d, adv) in enumerate(best_strategies[1:], 2):
                        order_names = [get_defense_name(i) for i in order]   # 只显示名称
                        order_info = [f"{name}" for name in order_names]
                        st.markdown(f"**策略 {idx}:** {order_info} (胜:{w} 平:{d} 优势:{adv})")

# ---------- 页脚 ----------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.9em; padding: 20px 0;">
        <p>田忌赛马策略计算器 | 基于Streamlit开发</p>
        <p>车头数量: 2-6匹 | 算法: 暴力搜索（全排列）</p>
        <p>✅ 策略优化：优先最大胜场 → 其次最大实力优势</p>
    </div>
    """,
    unsafe_allow_html=True
)
