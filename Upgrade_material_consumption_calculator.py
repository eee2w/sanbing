import streamlit as st
import pandas as pd

# ============= Streamlit 网页应用 =============
st.set_page_config(page_title="神兵玉石升级计算器", layout="wide")
st.title("⚔️💎 神兵玉石材料兑换计算器-新春版")
st.info("""
1、点击左上角双箭头填写积分和材料数量  
2、填写神兵玉石当前等级和目标等级  
3、点击计算得到结果（简略版计算结果为上下加起来的总消耗）  
4、积分设为0可以计算当前资源够不够升级到目标等级  
""")

# --- 版本选择 ---
st.markdown("---")
version = st.radio("选择版本:", ["详细版 (逐项设置)", "简略版 (批量设置)"], horizontal=True)

st.markdown("---")

# --- 1. 用户输入区（放在侧边栏，手机浏览更友好）---
with st.sidebar:
    st.header("📝 请输入你的数据")
    
    # 全局积分 - 改为空值
    CURRENT_POINTS = st.number_input("当前积分", min_value=0, value=None, step=1, placeholder="请输入积分")
    
    st.subheader("神兵材料库存")
    CURRENT_WOOD = st.number_input("木头数量", min_value=0, value=None, step=1, placeholder="请输入数量")
    CURRENT_MITHRIL = st.number_input("精金数量", min_value=0, value=None, step=1, placeholder="请输入数量")
    CURRENT_LAPIS = st.number_input("青金石数量", min_value=0, value=None, step=1, placeholder="请输入数量")
    
    st.subheader("玉石材料库存")
    CURRENT_CARVING_KNIFE = st.number_input("琢玉刀数量", min_value=0, value=None, step=1, placeholder="请输入数量")
    CURRENT_UNPOLISHED_JADE = st.number_input("璞玉数量", min_value=0, value=None, step=1, placeholder="请输入数量")
    
    st.subheader("兑换比例（如无特殊需求请勿修改）")
    # 将所有兑换比例改为浮点数
    POINTS_PER_WOOD = st.number_input("木头兑换比例 (积分/个)", min_value=0.0, value=0.084, step=0.1, format="%.3f")
    POINTS_PER_MITHRIL = st.number_input("精金兑换比例 (积分/个)", min_value=0.0, value=1.67, step=0.1, format="%.2f")
    POINTS_PER_LAPIS = st.number_input("青金石兑换比例 (积分/个)", min_value=0.0, value=5.0, step=0.1, format="%.2f")
    POINTS_PER_CARVING_KNIFE = st.number_input("琢玉刀兑换比例 (积分/个)", min_value=0.0, value=25.0, step=0.1, format="%.2f")
    POINTS_PER_UNPOLISHED_JADE = st.number_input("璞玉兑换比例 (积分/个)", min_value=0.0, value=5.0, step=0.1, format="%.2f")

# --- 2. 根据版本选择不同的界面 ---
WEAPONS = {}
JADES = {}

if version == "详细版 (逐项设置)":
    # --- 详细版神兵等级选择 ---
    st.header("⚔️ 神兵升级目标")
    
    # 定义等级选项
    weapon_level_options = ["未拥有"] + [f"绿色{i}级" for i in range(1, 6)] + [f"蓝色{i}级" for i in range(1, 6)] + [f"紫色{i}级" for i in range(1, 11)] + [f"红色{i}级" for i in range(1, 31)]
    
    # 为6件神兵创建6列
    weapon_cols = st.columns(6)
    weapon_names = ["步兵上", "步兵下", "骑兵上", "骑兵下", "弓兵上", "弓兵下"]
    
    for idx, weapon_name in enumerate(weapon_names):
        with weapon_cols[idx]:
            st.markdown(f"**{weapon_name}**")
            # 将所有神兵的默认值都设为"未拥有"（索引0）
            current_default = 0  # "未拥有"的索引
            target_default = 0   # "未拥有"的索引
                
            current_level = st.selectbox("当前等级", options=weapon_level_options, index=current_default, key=f"w_curr_{weapon_name}")
            target_level = st.selectbox("目标等级", options=weapon_level_options, index=target_default, key=f"w_tar_{weapon_name}")
            WEAPONS[weapon_name] = {"current": current_level, "target": target_level}
    
    st.markdown("---")
    
    # --- 详细版玉石等级选择 ---
    st.header("💎 玉石升级目标")
    st.caption("24个玉石，请分别设置当前和目标等级（0级为未激活）")
    
    # 定义玉石等级选项 (0-25级)
    jade_level_options = list(range(0, 26))
    
    # 使用展开/折叠器来组织，避免页面过长
    jade_types = ["步兵上", "步兵下", "骑兵上", "骑兵下", "弓兵上", "弓兵下"]
    
    for jade_type in jade_types:
        with st.expander(f"{jade_type}玉石 (1-4号)", expanded=jade_type=="步兵上"):
            cols = st.columns(4)
            for i in range(1, 5):
                jade_name = f"{jade_type}{i}"
                with cols[i-1]:
                    st.markdown(f"**{jade_name}**")
                    # 将所有玉石的默认值都设为0（未激活）
                    default_current = 0  # 0级
                    default_target = 0   # 0级
                    
                    current = st.selectbox("当前", options=jade_level_options, index=default_current, key=f"j_curr_{jade_name}")
                    target = st.selectbox("目标", options=jade_level_options, index=default_target, key=f"j_tar_{jade_name}")
                    JADES[jade_name] = {"current": current, "target": target}

else:
    # --- 简略版神兵等级选择 ---
    st.header("⚔️ 神兵升级目标 (批量设置)")
    st.caption("每个兵种上下两件神兵使用相同等级")
    
    # 定义等级选项
    weapon_level_options = ["未拥有"] + [f"绿色{i}级" for i in range(1, 6)] + [f"蓝色{i}级" for i in range(1, 6)] + [f"紫色{i}级" for i in range(1, 11)] + [f"红色{i}级" for i in range(1, 31)]
    
    # 为3个兵种创建3列
    troop_cols = st.columns(3)
    troop_names = ["步兵", "骑兵", "弓兵"]
    
    troop_settings = {}
    
    for idx, troop_name in enumerate(troop_names):
        with troop_cols[idx]:
            st.markdown(f"**{troop_name}**")
            # 默认值设为"未拥有"
            current_default = 0
            target_default = 0
            
            current_level = st.selectbox(f"{troop_name}当前等级", options=weapon_level_options, index=current_default, key=f"t_curr_{troop_name}")
            target_level = st.selectbox(f"{troop_name}目标等级", options=weapon_level_options, index=target_default, key=f"t_tar_{troop_name}")
            troop_settings[troop_name] = {"current": current_level, "target": target_level}
    
    # 根据兵种设置生成详细的WEAPONS数据（上下相同）
    for troop_name, levels in troop_settings.items():
        WEAPONS[f"{troop_name}上"] = {"current": levels["current"], "target": levels["target"]}
        WEAPONS[f"{troop_name}下"] = {"current": levels["current"], "target": levels["target"]}
    
    st.markdown("---")
    
    # --- 简略版玉石等级选择（修改后）---
    st.header("💎 玉石升级目标 (批量设置)")
    st.caption("每个兵种只需设置一个玉石等级，该兵种上下共8个玉石都使用此等级")
    
    # 定义玉石等级选项 (0-25级)
    jade_level_options = list(range(0, 26))
    
    # 为3个兵种创建3列
    jade_troop_cols = st.columns(3)
    jade_troop_names = ["步兵玉石", "骑兵玉石", "弓兵玉石"]
    
    jade_troop_settings = {}
    
    for idx, jade_troop_name in enumerate(jade_troop_names):
        with jade_troop_cols[idx]:
            st.markdown(f"**{jade_troop_name}**")
            st.caption("设置一个等级，8个玉石通用")
            
            # 每个兵种只需设置一个当前等级和一个目标等级
            default_current = 0
            default_target = 0
            
            current = st.selectbox(f"当前等级", options=jade_level_options, index=default_current, key=f"jt_curr_{jade_troop_name}")
            target = st.selectbox(f"目标等级", options=jade_level_options, index=default_target, key=f"jt_tar_{jade_troop_name}")
            
            jade_troop_settings[jade_troop_name] = {"current": current, "target": target}
    
    # 根据兵种设置生成详细的JADES数据（每个兵种8个玉石使用相同等级）
    # 步兵玉石：步兵上1-4，步兵下1-4（共8个）
    # 骑兵玉石：骑兵上1-4，骑兵下1-4（共8个）
    # 弓兵玉石：弓兵上1-4，弓兵下1-4（共8个）
    
    troop_mapping = {
        "步兵玉石": "步兵",
        "骑兵玉石": "骑兵", 
        "弓兵玉石": "弓兵"
    }
    
    for jade_troop_name, jade_setting in jade_troop_settings.items():
        troop_prefix = troop_mapping[jade_troop_name]
        
        # 生成该兵种8个玉石的设置（上下各4个，共8个）
        # 上位置玉石 (1-4)
        for i in range(1, 5):
            jade_name = f"{troop_prefix}上{i}"
            JADES[jade_name] = {"current": jade_setting["current"], 
                                "target": jade_setting["target"]}
        
        # 下位置玉石 (1-4)
        for i in range(1, 5):
            jade_name = f"{troop_prefix}下{i}"
            JADES[jade_name] = {"current": jade_setting["current"], 
                                "target": jade_setting["target"]}

st.markdown("---")

# --- 新增：额外兑换部分 ---
st.header("🛍️ 额外兑换部分")

# 初始化session_state用于存储额外兑换项目
if 'extra_items' not in st.session_state:
    st.session_state.extra_items = [{'name': '', 'points_per': 0.0, 'times': 0}]

# 显示所有额外兑换项目
for i, item in enumerate(st.session_state.extra_items):
    cols = st.columns([3, 2, 2, 1])
    with cols[0]:
        st.session_state.extra_items[i]['name'] = st.text_input(
            "物品名称", 
            value=item['name'],
            placeholder="如：皮肤、金箱子等",
            key=f"extra_name_{i}"
        )
    with cols[1]:
        st.session_state.extra_items[i]['points_per'] = st.number_input(
            "单次兑换积分", 
            min_value=0.0, 
            value=float(item['points_per']),
            step=1.0,
            format="%.1f",
            key=f"extra_points_{i}"
        )
    with cols[2]:
        st.session_state.extra_items[i]['times'] = st.number_input(
            "兑换次数", 
            min_value=0, 
            value=int(item['times']),
            step=1,
            key=f"extra_times_{i}"
        )
    with cols[3]:
        if i > 0:  # 第一个项目不显示删除按钮
            if st.button("❌", key=f"delete_{i}", help="删除此项"):
                del st.session_state.extra_items[i]
                st.rerun()

# 添加新项目的按钮
if st.button("➕ 添加兑换项目", type="secondary", use_container_width=False):
    st.session_state.extra_items.append({'name': '', 'points_per': 0.0, 'times': 0})
    st.rerun()

# 计算额外兑换的总积分
extra_points_total = sum(item['points_per'] * item['times'] for item in st.session_state.extra_items)

st.markdown("---")

# --- 3. 核心数据与计算器类（已修改以包含额外兑换）---
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

class UpgradeCalculator:
    def __init__(self):
        # 神兵相关 - 处理None值
        self.current_points = CURRENT_POINTS if CURRENT_POINTS is not None else 0
        self.points_per_wood = POINTS_PER_WOOD
        self.points_per_mithril = POINTS_PER_MITHRIL
        self.points_per_lapis = POINTS_PER_LAPIS
        self.current_wood = CURRENT_WOOD if CURRENT_WOOD is not None else 0
        self.current_mithril = CURRENT_MITHRIL if CURRENT_MITHRIL is not None else 0
        self.current_lapis = CURRENT_LAPIS if CURRENT_LAPIS is not None else 0
        self.weapons = WEAPONS
        self.weapon_upgrade_costs = WEAPON_UPGRADE_COSTS
        
        # 玉石相关 - 处理None值
        self.points_per_carving_knife = POINTS_PER_CARVING_KNIFE
        self.points_per_unpolished_jade = POINTS_PER_UNPOLISHED_JADE
        self.current_carving_knife = CURRENT_CARVING_KNIFE if CURRENT_CARVING_KNIFE is not None else 0
        self.current_unpolished_jade = CURRENT_UNPOLISHED_JADE if CURRENT_UNPOLISHED_JADE is not None else 0
        self.jades = JADES
        self.jade_upgrade_costs = JADE_UPGRADE_COSTS
        
        # 额外兑换部分
        self.extra_items = st.session_state.extra_items
        
    def level_str_to_number(self, level_str):
        level_str = level_str.strip()
        if level_str == "未拥有": return 0
        if "绿色" in level_str:
            level_num = int(level_str.replace("绿色", "").replace("级", ""))
            if 1 <= level_num <= 5: return level_num
        elif "蓝色" in level_str:
            level_num = int(level_str.replace("蓝色", "").replace("级", ""))
            if 1 <= level_num <= 5: return level_num + 5
        elif "紫色" in level_str:
            level_num = int(level_str.replace("紫色", "").replace("级", ""))
            if 1 <= level_num <= 10: return level_num + 10
        elif "红色" in level_str:
            level_num = int(level_str.replace("红色", "").replace("级", ""))
            if 1 <= level_num <= 30: return level_num + 20
        raise ValueError(f"无效的等级格式: {level_str}")
    
    def level_number_to_str(self, level_num):
        if level_num == 0: return "未拥有"
        elif 1 <= level_num <= 5: return f"绿色{level_num}级"
        elif 6 <= level_num <= 10: return f"蓝色{level_num-5}级"
        elif 11 <= level_num <= 20: return f"紫色{level_num-10}级"
        elif 21 <= level_num <= 50: return f"红色{level_num-20}级"
        else: return "未知等级"
    
    def calculate_weapon_upgrade(self, current_level_str, target_level_str):
        current_level = self.level_str_to_number(current_level_str)
        target_level = self.level_str_to_number(target_level_str)
        
        if target_level <= current_level:
            return {
                "current_level": current_level_str,
                "target_level": target_level_str,
                "total_wood_needed": 0,
                "total_mithril_needed": 0,
                "total_lapis_needed": 0,
                "levels_upgraded": 0,
                "need_upgrade": False
            }
        
        total_wood_needed = total_mithril_needed = total_lapis_needed = 0
        for level in range(current_level, target_level):
            cost_wood, cost_mithril, cost_lapis = self.weapon_upgrade_costs[level]
            total_wood_needed += cost_wood
            total_mithril_needed += cost_mithril
            total_lapis_needed += cost_lapis
        
        return {
            "current_level": current_level_str,
            "target_level": target_level_str,
            "total_wood_needed": total_wood_needed,
            "total_mithril_needed": total_mithril_needed,
            "total_lapis_needed": total_lapis_needed,
            "levels_upgraded": target_level - current_level,
            "need_upgrade": True
        }
    
    def calculate_jade_upgrade(self, current_level, target_level):
        if target_level <= current_level:
            return {
                "current_level": current_level,
                "target_level": target_level,
                "total_knife_needed": 0,
                "total_jade_needed": 0,
                "levels_upgraded": 0,
                "need_upgrade": False
            }
        
        total_knife_needed = total_jade_needed = 0
        for level in range(current_level, target_level):
            cost_knife, cost_jade = self.jade_upgrade_costs[level]
            total_knife_needed += cost_knife
            total_jade_needed += cost_jade
        
        return {
            "current_level": current_level,
            "target_level": target_level,
            "total_knife_needed": total_knife_needed,
            "total_jade_needed": total_jade_needed,
            "levels_upgraded": target_level - current_level,
            "need_upgrade": True
        }
    
    def calculate_extra_items(self):
        """计算额外兑换项目的总积分消耗"""
        extra_points_needed = 0
        extra_items_details = []
        
        for item in self.extra_items:
            if item['name'] and item['points_per'] > 0 and item['times'] > 0:
                item_total = item['points_per'] * item['times']
                extra_points_needed += item_total
                extra_items_details.append({
                    'name': item['name'],
                    'points_per': item['points_per'],
                    'times': item['times'],
                    'total': item_total
                })
        
        return {
            'extra_points_needed': extra_points_needed,
            'extra_items_details': extra_items_details
        }
    
    def calculate_all_upgrades(self):
        # 计算额外兑换部分
        extra_results = self.calculate_extra_items()
        extra_points_needed = extra_results['extra_points_needed']
        
        # 神兵升级计算
        weapon_results = {}
        weapon_wood_needed = weapon_mithril_needed = weapon_lapis_needed = 0
        
        for weapon_name, levels in self.weapons.items():
            result = self.calculate_weapon_upgrade(levels["current"], levels["target"])
            weapon_results[weapon_name] = result
            weapon_wood_needed += result["total_wood_needed"]
            weapon_mithril_needed += result["total_mithril_needed"]
            weapon_lapis_needed += result["total_lapis_needed"]
        
        # 玉石升级计算
        jade_results = {}
        jade_knife_needed = jade_jade_needed = 0
        
        for jade_name, levels in self.jades.items():
            result = self.calculate_jade_upgrade(levels["current"], levels["target"])
            jade_results[jade_name] = result
            jade_knife_needed += result["total_knife_needed"]
            jade_jade_needed += result["total_jade_needed"]
        
        # 计算需要购买的材料
        wood_need_buy = max(0, weapon_wood_needed - self.current_wood)
        mithril_need_buy = max(0, weapon_mithril_needed - self.current_mithril)
        lapis_need_buy = max(0, weapon_lapis_needed - self.current_lapis)
        knife_need_buy = max(0, jade_knife_needed - self.current_carving_knife)
        jade_need_buy = max(0, jade_jade_needed - self.current_unpolished_jade)
        
        # 计算所需总积分（包括额外兑换）
        total_points_needed = (
            wood_need_buy * self.points_per_wood +
            mithril_need_buy * self.points_per_mithril +
            lapis_need_buy * self.points_per_lapis +
            knife_need_buy * self.points_per_carving_knife +
            jade_need_buy * self.points_per_unpolished_jade +
            extra_points_needed  # 添加额外兑换积分
        )
        
        # 计算升级后剩余材料
        wood_left_after = max(0, self.current_wood - weapon_wood_needed)
        mithril_left_after = max(0, self.current_mithril - weapon_mithril_needed)
        lapis_left_after = max(0, self.current_lapis - weapon_lapis_needed)
        knife_left_after = max(0, self.current_carving_knife - jade_knife_needed)
        jade_left_after = max(0, self.current_unpolished_jade - jade_jade_needed)
        
        # 检查积分是否足够
        points_shortage = max(0, total_points_needed - self.current_points)
        
        return {
            "weapon_results": weapon_results,
            "jade_results": jade_results,
            "extra_results": extra_results,
            "weapon_wood_needed": weapon_wood_needed,
            "weapon_mithril_needed": weapon_mithril_needed,
            "weapon_lapis_needed": weapon_lapis_needed,
            "jade_knife_needed": jade_knife_needed,
            "jade_jade_needed": jade_jade_needed,
            "extra_points_needed": extra_points_needed,
            "wood_need_buy": wood_need_buy,
            "mithril_need_buy": mithril_need_buy,
            "lapis_need_buy": lapis_need_buy,
            "knife_need_buy": knife_need_buy,
            "jade_need_buy": jade_need_buy,
            "total_points_needed": total_points_needed,
            "current_points": self.current_points,
            "points_shortage": points_shortage,
            "can_upgrade": total_points_needed <= self.current_points,
            "points_left_after": self.current_points - total_points_needed,
            "wood_left_after": wood_left_after,
            "mithril_left_after": mithril_left_after,
            "lapis_left_after": lapis_left_after,
            "knife_left_after": knife_left_after,
            "jade_left_after": jade_left_after
        }

# --- 4. 计算并展示结果 ---
st.header("📊 计算结果（注意兑换1次得到的材料数量不一定是1个）")

# 显示当前版本信息
st.info(f"当前使用: **{version}** - {'所有项目单独设置' if version == '详细版 (逐项设置)' else '按兵种批量设置'}")

if st.button("🚀 开始计算", type="primary", use_container_width=True):
    with st.spinner("正在计算升级需求..."):
        # 初始化计算器，传入用户输入的动态值
        calculator = UpgradeCalculator()
        # 处理None值，确保计算正确
        calculator.current_points = CURRENT_POINTS if CURRENT_POINTS is not None else 0
        calculator.current_wood = CURRENT_WOOD if CURRENT_WOOD is not None else 0
        calculator.current_mithril = CURRENT_MITHRIL if CURRENT_MITHRIL is not None else 0
        calculator.current_lapis = CURRENT_LAPIS if CURRENT_LAPIS is not None else 0
        calculator.current_carving_knife = CURRENT_CARVING_KNIFE if CURRENT_CARVING_KNIFE is not None else 0
        calculator.current_unpolished_jade = CURRENT_UNPOLISHED_JADE if CURRENT_UNPOLISHED_JADE is not None else 0
        calculator.points_per_wood = POINTS_PER_WOOD
        calculator.points_per_mithril = POINTS_PER_MITHRIL
        calculator.points_per_lapis = POINTS_PER_LAPIS
        calculator.points_per_carving_knife = POINTS_PER_CARVING_KNIFE
        calculator.points_per_unpolished_jade = POINTS_PER_UNPOLISHED_JADE
        calculator.weapons = WEAPONS
        calculator.jades = JADES
        
        # 执行计算
        results = calculator.calculate_all_upgrades()
        
    # --- 展示结果 ---
    st.success("计算完成！")
    
    # 结果总览卡片
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("所需总积分", f"{results['total_points_needed']:.1f}")
    with col2:
        st.metric("当前积分", f"{results['current_points']}")
    with col3:
        status = "充足 ✅" if results['can_upgrade'] else f"不足 ❌ (差{results['points_shortage']:.1f})"
        st.metric("积分状态", status)
    
    # 材料需求
    with st.expander("📦 详细材料需求与剩余情况", expanded=True):
        tab1, tab2, tab3 = st.tabs(["神兵材料", "玉石材料", "额外兑换"])
        with tab1:
            c1, c2, c3 = st.columns(3)
            c1.metric("木头需求/剩余", f"{results['weapon_wood_needed']} / {results['wood_left_after']}")
            c2.metric("精金需求/剩余", f"{results['weapon_mithril_needed']} / {results['mithril_left_after']}")
            c3.metric("青金石需求/剩余", f"{results['weapon_lapis_needed']} / {results['lapis_left_after']}")
        with tab2:
            c1, c2 = st.columns(2)
            c1.metric("琢玉刀需求/剩余", f"{results['jade_knife_needed']} / {results['knife_left_after']}")
            c2.metric("璞玉需求/剩余", f"{results['jade_jade_needed']} / {results['jade_left_after']}")
        with tab3:
            if results['extra_points_needed'] > 0:
                st.metric("额外兑换总积分", f"{results['extra_points_needed']:.1f}")
                extra_df = pd.DataFrame(results['extra_results']['extra_items_details'])
                st.dataframe(extra_df, use_container_width=True)
            else:
                st.info("无额外兑换项目")
    
    # 需要购买的材料
    if any([results['wood_need_buy'], results['mithril_need_buy'], results['lapis_need_buy'], 
            results['knife_need_buy'], results['jade_need_buy']]):
        st.warning("🛒 需要兑换的材料")
        need_buy_cols = st.columns(5)
        materials = [
            ("木头", results['wood_need_buy'], "🪵"),
            ("精金", results['mithril_need_buy'], "⚙️"),
            ("青金石", results['lapis_need_buy'], "🔷"),
            ("琢玉刀", results['knife_need_buy'], "🔪"),
            ("璞玉", results['jade_need_buy'], "💎")
        ]
        for idx, (name, amount, icon) in enumerate(materials):
            if amount > 0:
                need_buy_cols[idx].metric(f"{icon} {name}", f"{amount}个")
    
    # 额外兑换详情
    if results['extra_points_needed'] > 0:
        with st.expander("🛍️ 额外兑换详情"):
            extra_data = []
            for item in results['extra_results']['extra_items_details']:
                extra_data.append({
                    "物品名称": item['name'],
                    "单次积分": f"{item['points_per']:.1f}",
                    "兑换次数": item['times'],
                    "小计积分": f"{item['total']:.1f}"
                })
            if extra_data:
                st.dataframe(pd.DataFrame(extra_data), use_container_width=True)
    
    # 神兵升级详情表格
    with st.expander("⚔️ 神兵升级详情"):
        weapon_data = []
        for name, info in results['weapon_results'].items():
            if info['need_upgrade']:
                weapon_data.append({
                    "神兵": name,
                    "当前等级": info['current_level'],
                    "目标等级": info['target_level'],
                    "升级级数": info['levels_upgraded'],
                    "需木头": info['total_wood_needed'],
                    "需精金": info['total_mithril_needed'],
                    "需青金石": info['total_lapis_needed']
                })
        if weapon_data:
            st.dataframe(pd.DataFrame(weapon_data), use_container_width=True)
            # 简略版额外显示兵种汇总信息
            if version == "简略版 (批量设置)":
                st.info("💡 简略版说明: 每个兵种的上下两件神兵设置相同，消耗已自动×2")
        else:
            st.info("所有神兵均无需升级")
    
    # 玉石升级详情表格
    with st.expander("💎 玉石升级详情"):
        jade_data = []
        for name, info in results['jade_results'].items():
            if info['need_upgrade'] and info['levels_upgraded'] > 0:
                jade_data.append({
                    "玉石": name,
                    "当前等级": info['current_level'],
                    "目标等级": info['target_level'],
                    "升级级数": info['levels_upgraded'],
                    "需琢玉刀": info['total_knife_needed'],
                    "需璞玉": info['total_jade_needed']
                })
        if jade_data:
            st.dataframe(pd.DataFrame(jade_data), use_container_width=True)
            # 简略版额外显示兵种汇总信息
            if version == "简略版 (批量设置)":
                st.info("💡 简略版说明: 每个兵种只需设置一个玉石等级，该兵种上下共8个玉石都使用此等级，消耗已自动×8")
        else:
            st.info("所有玉石均无需升级")

st.markdown("---")
st.caption("提示: 在侧边栏修改数据后，点击上方'开始计算'按钮更新结果。切换版本后，当前设置会被重置。")
