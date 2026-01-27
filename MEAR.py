import streamlit as st
import pandas as pd

# ============= Streamlit 网页应用 =============
st.set_page_config(page_title="神兵玉石自动升级计算器", layout="wide")
st.title("⚔️💎 神兵玉石自动升级计算器")
st.caption("📝 提示：点击左上角双箭头图标填写积分和材料数量")
st.markdown("---")

# --- 版本说明 ---
st.info("""
**功能说明**：
1. 填写当前积分和材料库存
2. 设置当前步/弓神兵玉石等级
3. 设置等级差（默认：神兵高5级，玉石高3级）
4. 系统自动计算在当前资源下，步兵和弓兵能升到的最高等级
5. 忽略骑兵的神兵和玉石
""")

st.markdown("---")

# --- 1. 用户输入区（放在侧边栏）---
with st.sidebar:
    st.header("📝 资源与等级设置")
    
    # 全局积分
    CURRENT_POINTS = st.number_input("当前积分", min_value=0, value=10000, step=100)
    
    st.subheader("神兵材料库存")
    CURRENT_WOOD = st.number_input("木头数量", min_value=0, value=1000, step=10)
    CURRENT_MITHRIL = st.number_input("精金数量", min_value=0, value=500, step=5)
    CURRENT_LAPIS = st.number_input("青金石数量", min_value=0, value=100, step=1)
    
    st.subheader("玉石材料库存")
    CURRENT_CARVING_KNIFE = st.number_input("琢玉刀数量", min_value=0, value=200, step=10)
    CURRENT_UNPOLISHED_JADE = st.number_input("璞玉数量", min_value=0, value=300, step=10)
    
    st.subheader("兑换比例")
    POINTS_PER_WOOD = st.number_input("木头兑换比例", min_value=0.0, value=0.1, step=0.1, format="%.2f")
    POINTS_PER_MITHRIL = st.number_input("精金兑换比例", min_value=0.0, value=2.0, step=0.1, format="%.2f")
    POINTS_PER_LAPIS = st.number_input("青金石兑换比例", min_value=0.0, value=6.0, step=0.1, format="%.2f")
    POINTS_PER_CARVING_KNIFE = st.number_input("琢玉刀兑换比例", min_value=0.0, value=30.0, step=1.0, format="%.2f")
    POINTS_PER_UNPOLISHED_JADE = st.number_input("璞玉兑换比例", min_value=0.0, value=6.0, step=0.1, format="%.2f")
    
    st.markdown("---")
    
    st.subheader("等级差设置")
    st.caption("步兵等级比弓兵高多少级？")
    WEAPON_LEVEL_DIFF = st.slider("神兵等级差", min_value=0, max_value=10, value=5, step=1)
    JADE_LEVEL_DIFF = st.slider("玉石等级差", min_value=0, max_value=10, value=3, step=1)

st.markdown("---")

# --- 2. 当前等级输入 ---
st.header("🎯 当前等级设置")
st.caption("设置步兵和弓兵神兵、玉石的当前等级")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("步兵神兵")
    # 定义等级选项
    weapon_level_options = ["未拥有"] + [f"绿色{i}级" for i in range(1, 6)] + [f"蓝色{i}级" for i in range(1, 6)] + [f"紫色{i}级" for i in range(1, 11)] + [f"红色{i}级" for i in range(1, 31)]
    current_foot_weapon = st.selectbox("当前等级", options=weapon_level_options, index=weapon_level_options.index("绿色1级"), key="curr_foot_weapon")

with col2:
    st.subheader("弓兵神兵")
    current_archer_weapon = st.selectbox("当前等级", options=weapon_level_options, index=weapon_level_options.index("未拥有"), key="curr_archer_weapon")

with col3:
    st.subheader("步兵玉石")
    jade_level_options = list(range(0, 26))
    current_foot_jade = st.selectbox("当前等级", options=jade_level_options, index=0, key="curr_foot_jade")

with col4:
    st.subheader("弓兵玉石")
    current_archer_jade = st.selectbox("当前等级", options=jade_level_options, index=0, key="curr_archer_jade")

st.markdown("---")

# --- 3. 核心数据与计算器类 ---
WEAPON_UPGRADE_COSTS = [
    [1000, 50, 0], [1500, 75, 0], [2000, 100, 0], [2500, 125, 0], [3000, 150, 0],
    [3500, 175, 0], [4000, 200, 0], [4500, 225, 0], [5000, 250, 0], [5500, 275, 0],
    [6000, 300, 150], [6500, 325, 160], [7000, 350, 170], [7500, 375, 180], [8000, 400, 180],
    [8500, 425, 190], [9000, 450, 200], [9500, 475, 200], [10000, 500, 210], [10500, 525, 220],
    [11000, 550, 220], [12000, 600, 230], [13000, 650, 250], [14000, 700, 260], [15000, 750, 270],
    [16000, 800, 280], [17000, 850, 290], [18000, 900, 300], [19000, 950, 300], [20000, 1000, 310],
    [21000, 1050, 320], [22000, 1100, 320], [23000, 1150, 320], [24000, 1200, 320], [25000, 1250, 330],
    [26000, 1300, 330], [27000, 1350, 340], [28000, 1400, 350], [29000, 1450, 360], [30000, 1500, 360],
    [31000, 1550, 360], [32000, 1600, 370], [33000, 1650, 380], [34000, 1700, 390], [35000, 1750, 390],
    [36000, 1800, 400], [37000, 1850, 410], [38000, 1900, 420], [39000, 1950, 430], [40000, 2000, 440]
]

JADE_UPGRADE_COSTS = [
    [2, 10], [4, 12], [6, 14], [8, 16], [10, 18],
    [12, 20], [16, 24], [20, 28], [30, 32], [40, 36],
    [60, 50], [100, 60], [140, 70], [180, 80], [220, 90],
    [240, 100], [240, 140], [260, 180], [260, 220], [280, 260],
    [300, 300], [320, 340], [340, 380], [360, 420], [380, 460]
]

class AutoUpgradeCalculator:
    def __init__(self):
        # 当前资源
        self.current_points = CURRENT_POINTS
        self.current_wood = CURRENT_WOOD
        self.current_mithril = CURRENT_MITHRIL
        self.current_lapis = CURRENT_LAPIS
        self.current_carving_knife = CURRENT_CARVING_KNIFE
        self.current_unpolished_jade = CURRENT_UNPOLISHED_JADE
        
        # 兑换比例
        self.points_per_wood = POINTS_PER_WOOD
        self.points_per_mithril = POINTS_PER_MITHRIL
        self.points_per_lapis = POINTS_PER_LAPIS
        self.points_per_carving_knife = POINTS_PER_CARVING_KNIFE
        self.points_per_unpolished_jade = POINTS_PER_UNPOLISHED_JADE
        
        # 当前等级
        self.current_foot_weapon = current_foot_weapon
        self.current_archer_weapon = current_archer_weapon
        self.current_foot_jade = current_foot_jade
        self.current_archer_jade = current_archer_jade
        
        # 等级差
        self.weapon_level_diff = WEAPON_LEVEL_DIFF
        self.jade_level_diff = JADE_LEVEL_DIFF
        
        # 消耗表
        self.weapon_upgrade_costs = WEAPON_UPGRADE_COSTS
        self.jade_upgrade_costs = JADE_UPGRADE_COSTS
    
    def level_str_to_number(self, level_str):
        """将颜色等级字符串转换为数字等级"""
        level_str = level_str.strip()
        
        if level_str == "未拥有":
            return 0
        
        if "绿色" in level_str:
            level_num = int(level_str.replace("绿色", "").replace("级", ""))
            if 1 <= level_num <= 5:
                return level_num
        elif "蓝色" in level_str:
            level_num = int(level_str.replace("蓝色", "").replace("级", ""))
            if 1 <= level_num <= 5:
                return level_num + 5
        elif "紫色" in level_str:
            level_num = int(level_str.replace("紫色", "").replace("级", ""))
            if 1 <= level_num <= 10:
                return level_num + 10
        elif "红色" in level_str:
            level_num = int(level_str.replace("红色", "").replace("级", ""))
            if 1 <= level_num <= 30:
                return level_num + 20
        
        return 0
    
    def level_number_to_str(self, level_num):
        """将数字等级转换为颜色等级字符串"""
        if level_num == 0:
            return "未拥有"
        elif 1 <= level_num <= 5:
            return f"绿色{level_num}级"
        elif 6 <= level_num <= 10:
            return f"蓝色{level_num-5}级"
        elif 11 <= level_num <= 20:
            return f"紫色{level_num-10}级"
        elif 21 <= level_num <= 50:
            return f"红色{level_num-20}级"
        else:
            return "未知等级"
    
    def calculate_upgrade_cost(self, current_level, target_level, cost_type="weapon"):
        """计算从当前等级升级到目标等级所需材料"""
        if target_level <= current_level:
            if cost_type == "weapon":
                return {"wood": 0, "mithril": 0, "lapis": 0}
            else:
                return {"knife": 0, "jade": 0}
        
        total_cost = {"wood": 0, "mithril": 0, "lapis": 0} if cost_type == "weapon" else {"knife": 0, "jade": 0}
        
        for level in range(current_level, target_level):
            if cost_type == "weapon" and level < len(self.weapon_upgrade_costs):
                cost_wood, cost_mithril, cost_lapis = self.weapon_upgrade_costs[level]
                total_cost["wood"] += cost_wood
                total_cost["mithril"] += cost_mithril
                total_cost["lapis"] += cost_lapis
            elif cost_type == "jade" and level < len(self.jade_upgrade_costs):
                cost_knife, cost_jade = self.jade_upgrade_costs[level]
                total_cost["knife"] += cost_knife
                total_cost["jade"] += cost_jade
        
        return total_cost
    
    def calculate_required_points(self, materials_needed):
        """计算需要兑换的材料所需的积分"""
        points_needed = 0
        
        # 神兵材料
        wood_needed = max(0, materials_needed.get("wood", 0) - self.current_wood)
        mithril_needed = max(0, materials_needed.get("mithril", 0) - self.current_mithril)
        lapis_needed = max(0, materials_needed.get("lapis", 0) - self.current_lapis)
        
        # 玉石材料
        knife_needed = max(0, materials_needed.get("knife", 0) - self.current_carving_knife)
        jade_needed = max(0, materials_needed.get("jade", 0) - self.current_unpolished_jade)
        
        points_needed = (
            wood_needed * self.points_per_wood +
            mithril_needed * self.points_per_mithril +
            lapis_needed * self.points_per_lapis +
            knife_needed * self.points_per_carving_knife +
            jade_needed * self.points_per_unpolished_jade
        )
        
        return points_needed, {
            "wood_need_buy": wood_needed,
            "mithril_need_buy": mithril_needed,
            "lapis_need_buy": lapis_needed,
            "knife_need_buy": knife_needed,
            "jade_need_buy": jade_needed
        }
    
    def find_max_levels(self):
        """寻找在当前资源下能达到的最高等级"""
        # 将当前等级转换为数字
        current_foot_weapon_num = self.level_str_to_number(self.current_foot_weapon)
        current_archer_weapon_num = self.level_str_to_number(self.current_archer_weapon)
        current_foot_jade_num = self.current_foot_jade
        current_archer_jade_num = self.current_archer_jade
        
        best_result = {
            "foot_weapon_target": current_foot_weapon_num,
            "archer_weapon_target": current_archer_weapon_num,
            "foot_jade_target": current_foot_jade_num,
            "archer_jade_target": current_archer_jade_num,
            "points_needed": 0,
            "materials_to_buy": {},
            "materials_used": {},
            "points_left": self.current_points
        }
        
        # 遍历可能的步兵神兵等级（从当前等级到50级）
        for foot_weapon_target in range(current_foot_weapon_num, 51):
            # 根据等级差计算弓兵神兵目标等级
            archer_weapon_target = foot_weapon_target - self.weapon_level_diff
            
            # 弓兵等级不能低于当前等级
            if archer_weapon_target < current_archer_weapon_num:
                archer_weapon_target = current_archer_weapon_num
            
            # 遍历可能的步兵玉石等级（从当前等级到25级）
            for foot_jade_target in range(current_foot_jade_num, 26):
                # 根据等级差计算弓兵玉石目标等级
                archer_jade_target = foot_jade_target - self.jade_level_diff
                
                # 弓兵等级不能低于当前等级
                if archer_jade_target < current_archer_jade_num:
                    archer_jade_target = current_archer_jade_num
                
                # 计算神兵升级所需材料（注意：步兵和弓兵各2件神兵）
                foot_weapon_cost = self.calculate_upgrade_cost(current_foot_weapon_num, foot_weapon_target, "weapon")
                archer_weapon_cost = self.calculate_upgrade_cost(current_archer_weapon_num, archer_weapon_target, "weapon")
                
                # 总神兵材料需求（乘以2，因为上下两件）
                weapon_materials = {
                    "wood": (foot_weapon_cost["wood"] + archer_weapon_cost["wood"]) * 2,
                    "mithril": (foot_weapon_cost["mithril"] + archer_weapon_cost["mithril"]) * 2,
                    "lapis": (foot_weapon_cost["lapis"] + archer_weapon_cost["lapis"]) * 2
                }
                
                # 计算玉石升级所需材料（注意：步兵和弓兵各8个玉石）
                foot_jade_cost = self.calculate_upgrade_cost(current_foot_jade_num, foot_jade_target, "jade")
                archer_jade_cost = self.calculate_upgrade_cost(current_archer_jade_num, archer_jade_target, "jade")
                
                # 总玉石材料需求（乘以8，因为每个兵种8个玉石）
                jade_materials = {
                    "knife": (foot_jade_cost["knife"] + archer_jade_cost["knife"]) * 8,
                    "jade": (foot_jade_cost["jade"] + archer_jade_cost["jade"]) * 8
                }
                
                # 合并所有材料需求
                total_materials_needed = {**weapon_materials, **jade_materials}
                
                # 计算所需积分
                points_needed, materials_to_buy = self.calculate_required_points(total_materials_needed)
                
                # 检查积分是否足够
                if points_needed <= self.current_points:
                    # 计算剩余积分
                    points_left = self.current_points - points_needed
                    
                    # 计算实际使用的材料
                    materials_used = {
                        "wood": min(self.current_wood, total_materials_needed.get("wood", 0)),
                        "mithril": min(self.current_mithril, total_materials_needed.get("mithril", 0)),
                        "lapis": min(self.current_lapis, total_materials_needed.get("lapis", 0)),
                        "knife": min(self.current_carving_knife, total_materials_needed.get("knife", 0)),
                        "jade": min(self.current_unpolished_jade, total_materials_needed.get("jade", 0))
                    }
                    
                    # 如果这个组合比之前的好，就更新最佳结果
                    # 优先考虑步兵神兵等级，然后是步兵玉石等级
                    if (foot_weapon_target > best_result["foot_weapon_target"] or
                        (foot_weapon_target == best_result["foot_weapon_target"] and 
                         foot_jade_target > best_result["foot_jade_target"])):
                        
                        best_result = {
                            "foot_weapon_target": foot_weapon_target,
                            "archer_weapon_target": archer_weapon_target,
                            "foot_jade_target": foot_jade_target,
                            "archer_jade_target": archer_jade_target,
                            "points_needed": points_needed,
                            "materials_to_buy": materials_to_buy,
                            "materials_used": materials_used,
                            "materials_needed": total_materials_needed,
                            "points_left": points_left
                        }
                else:
                    # 如果积分不够，停止增加步兵玉石等级
                    break
            
            # 如果连最小的玉石升级都不行，停止增加步兵神兵等级
            if foot_weapon_target > current_foot_weapon_num and best_result["foot_weapon_target"] < foot_weapon_target:
                # 检查是否至少有一个玉石等级组合是可行的
                if best_result["foot_weapon_target"] == current_foot_weapon_num and best_result["foot_jade_target"] == current_foot_jade_num:
                    # 当前神兵等级下没有任何可行的玉石组合，停止
                    break
        
        return best_result

# --- 4. 计算并展示结果 ---
st.header("🚀 自动升级计算")

if st.button("开始自动计算最佳升级方案", type="primary", use_container_width=True):
    with st.spinner("正在计算最佳升级方案..."):
        calculator = AutoUpgradeCalculator()
        result = calculator.find_max_levels()
    
    st.success("计算完成！")
    
    # 显示结果总览
    st.subheader("🎯 最佳升级方案")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("步兵神兵", 
                 f"{calculator.level_number_to_str(result['foot_weapon_target'])}",
                 f"升级{result['foot_weapon_target'] - calculator.level_str_to_number(current_foot_weapon)}级")
    
    with col2:
        st.metric("弓兵神兵", 
                 f"{calculator.level_number_to_str(result['archer_weapon_target'])}",
                 f"升级{result['archer_weapon_target'] - calculator.level_str_to_number(current_archer_weapon)}级")
    
    with col3:
        st.metric("步兵玉石", 
                 f"{result['foot_jade_target']}级",
                 f"升级{result['foot_jade_target'] - current_foot_jade}级")
    
    with col4:
        st.metric("弓兵玉石", 
                 f"{result['archer_jade_target']}级",
                 f"升级{result['archer_jade_target'] - current_archer_jade}级")
    
    st.markdown("---")
    
    # 积分使用情况
    st.subheader("💰 积分使用情况")
    
    points_col1, points_col2, points_col3 = st.columns(3)
    
    with points_col1:
        st.metric("当前积分", f"{CURRENT_POINTS}")
    
    with points_col2:
        st.metric("升级所需积分", f"{result['points_needed']:.1f}")
    
    with points_col3:
        st.metric("升级后剩余积分", f"{result['points_left']:.1f}")
    
    # 材料使用情况
    st.subheader("📦 材料使用情况")
    
    with st.expander("详细材料消耗", expanded=True):
        tab1, tab2 = st.tabs(["神兵材料", "玉石材料"])
        
        with tab1:
            mat1, mat2, mat3 = st.columns(3)
            with mat1:
                st.metric("木头", 
                         f"需要: {result['materials_needed'].get('wood', 0)}",
                         f"使用库存: {result['materials_used'].get('wood', 0)}")
            with mat2:
                st.metric("精金", 
                         f"需要: {result['materials_needed'].get('mithril', 0)}",
                         f"使用库存: {result['materials_used'].get('mithril', 0)}")
            with mat3:
                st.metric("青金石", 
                         f"需要: {result['materials_needed'].get('lapis', 0)}",
                         f"使用库存: {result['materials_used'].get('lapis', 0)}")
        
        with tab2:
            mat4, mat5 = st.columns(2)
            with mat4:
                st.metric("琢玉刀", 
                         f"需要: {result['materials_needed'].get('knife', 0)}",
                         f"使用库存: {result['materials_used'].get('knife', 0)}")
            with mat5:
                st.metric("璞玉", 
                         f"需要: {result['materials_needed'].get('jade', 0)}",
                         f"使用库存: {result['materials_used'].get('jade', 0)}")
    
    # 需要兑换的材料
    if any([result['materials_to_buy'].get('wood_need_buy', 0) > 0,
            result['materials_to_buy'].get('mithril_need_buy', 0) > 0,
            result['materials_to_buy'].get('lapis_need_buy', 0) > 0,
            result['materials_to_buy'].get('knife_need_buy', 0) > 0,
            result['materials_to_buy'].get('jade_need_buy', 0) > 0]):
        
        st.subheader("🛒 需要兑换的材料")
        
        buy_cols = st.columns(5)
        buy_materials = [
            ("木头", result['materials_to_buy'].get('wood_need_buy', 0), "🪵"),
            ("精金", result['materials_to_buy'].get('mithril_need_buy', 0), "⚙️"),
            ("青金石", result['materials_to_buy'].get('lapis_need_buy', 0), "🔷"),
            ("琢玉刀", result['materials_to_buy'].get('knife_need_buy', 0), "🔪"),
            ("璞玉", result['materials_to_buy'].get('jade_need_buy', 0), "💎")
        ]
        
        for idx, (name, amount, icon) in enumerate(buy_materials):
            if amount > 0:
                buy_cols[idx].metric(f"{icon} {name}", f"{amount}个")
    
    # 升级详情
    st.subheader("📋 升级详情")
    
    with st.expander("查看升级路径", expanded=False):
        # 神兵升级详情
        st.write("**神兵升级详情:**")
        weapon_data = {
            "兵种": ["步兵", "弓兵"],
            "当前等级": [current_foot_weapon, current_archer_weapon],
            "目标等级": [
                calculator.level_number_to_str(result['foot_weapon_target']),
                calculator.level_number_to_str(result['archer_weapon_target'])
            ],
            "升级级数": [
                result['foot_weapon_target'] - calculator.level_str_to_number(current_foot_weapon),
                result['archer_weapon_target'] - calculator.level_str_to_number(current_archer_weapon)
            ]
        }
        st.dataframe(pd.DataFrame(weapon_data), use_container_width=True)
        
        # 玉石升级详情
        st.write("**玉石升级详情:**")
        jade_data = {
            "兵种": ["步兵", "弓兵"],
            "当前等级": [current_foot_jade, current_archer_jade],
            "目标等级": [result['foot_jade_target'], result['archer_jade_target']],
            "升级级数": [
                result['foot_jade_target'] - current_foot_jade,
                result['archer_jade_target'] - current_archer_jade
            ]
        }
        st.dataframe(pd.DataFrame(jade_data), use_container_width=True)
    
    st.markdown("---")
    st.info(f"""
    **计算说明**:
    1. 保持步兵神兵比弓兵神兵高 **{WEAPON_LEVEL_DIFF}** 级
    2. 保持步兵玉石比弓兵玉石高 **{JADE_LEVEL_DIFF}** 级
    3. 系统在满足等级差的前提下，最大化步兵的等级
    4. 忽略骑兵的神兵和玉石
    """)

st.markdown("---")
st.caption("提示：修改侧边栏的设置后，点击上方按钮重新计算。")
