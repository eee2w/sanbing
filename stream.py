import streamlit as st
import pandas as pd

# ============= Streamlit 网页应用 =============
st.set_page_config(page_title="神兵玉石升级计算器", layout="wide")
st.title("⚔️💎 神兵玉石升级计算器")
st.markdown("---")

# --- 1. 用户输入区（放在侧边栏，手机浏览更友好）---
with st.sidebar:
    st.header("📝 请输入你的数据")
    
    # 全局积分
    CURRENT_POINTS = st.number_input("当前积分", min_value=0, value=20347, step=1000)
    
    st.subheader("神兵材料库存")
    CURRENT_WOOD = st.number_input("木头数量", min_value=0, value=9859, step=100)
    CURRENT_MITHRIL = st.number_input("精金数量", min_value=0, value=904, step=10)
    CURRENT_LAPIS = st.number_input("青金石数量", min_value=0, value=231, step=5)
    
    st.subheader("玉石材料库存")
    CURRENT_CARVING_KNIFE = st.number_input("琢玉刀数量", min_value=0, value=295, step=10)
    CURRENT_UNPOLISHED_JADE = st.number_input("璞玉数量", min_value=0, value=492, step=10)
    
    st.subheader("兑换比例（如无特殊需求请勿修改）")
    POINTS_PER_WOOD = st.number_input("木头兑换比例 (积分/个)", min_value=0.0, value=0.1, step=0.1, format="%.2f")
    POINTS_PER_MITHRIL = st.number_input("精金兑换比例 (积分/个)", min_value=0, value=2, step=1)
    POINTS_PER_LAPIS = st.number_input("青金石兑换比例 (积分/个)", min_value=0, value=6, step=1)
    POINTS_PER_CARVING_KNIFE = st.number_input("琢玉刀兑换比例 (积分/个)", min_value=0, value=30, step=5)
    POINTS_PER_UNPOLISHED_JADE = st.number_input("璞玉兑换比例 (积分/个)", min_value=0, value=6, step=1)

# --- 2. 神兵等级选择（在主页面使用多列布局）---
st.header("⚔️ 神兵升级目标")

# 定义等级选项
weapon_level_options = ["未拥有"] + [f"绿色{i}级" for i in range(1, 6)] + [f"蓝色{i}级" for i in range(1, 6)] + [f"紫色{i}级" for i in range(1, 11)] + [f"红色{i}级" for i in range(1, 31)]

# 为6件神兵创建6列
weapon_cols = st.columns(6)
weapon_names = ["步兵上", "步兵下", "骑兵上", "骑兵下", "弓兵上", "弓兵下"]

WEAPONS = {}
for idx, weapon_name in enumerate(weapon_names):
    with weapon_cols[idx]:
        st.markdown(f"**{weapon_name}**")
        current_level = st.selectbox(f"当前等级", options=weapon_level_options, index=weapon_level_options.index("绿色1级") if "骑兵" in weapon_name or "弓兵" in weapon_name else weapon_level_options.index("紫色1级"), key=f"w_curr_{weapon_name}")
        target_level = st.selectbox(f"目标等级", options=weapon_level_options, index=weapon_level_options.index("绿色1级") if "骑兵" in weapon_name else (weapon_level_options.index("蓝色3级") if "弓兵" in weapon_name else weapon_level_options.index("紫色4级")), key=f"w_tar_{weapon_name}")
        WEAPONS[weapon_name] = {"current": current_level, "target": target_level}

st.markdown("---")

# --- 3. 玉石等级选择（使用折叠器节省空间）---
st.header("💎 玉石升级目标")
st.caption("24个玉石，请分别设置当前和目标等级（0级为未激活）")

# 定义玉石等级选项 (0-25级)
jade_level_options = list(range(0, 26))  # 0到25级

# 使用展开/折叠器来组织，避免页面过长
JADES = {}
jade_types = ["步兵上", "步兵下", "骑兵上", "骑兵下", "弓兵上", "弓兵下"]

for jade_type in jade_types:
    with st.expander(f"{jade_type}玉石 (1-4号)", expanded=jade_type=="步兵上"):  # 默认展开步兵
        cols = st.columns(4)
        for i in range(1, 5):
            jade_name = f"{jade_type}{i}"
            with cols[i-1]:
                st.markdown(f"**{jade_name}**")
                # 设置默认值：步兵玉石默认2->5，骑兵1->1，弓兵1->3
                default_current = 2 if "步兵" in jade_type else (1 if "骑兵" in jade_type else (2 if i==1 and "弓兵上" in jade_type else 1))
                default_target = 5 if "步兵" in jade_type else (1 if "骑兵" in jade_type else 3)
                
                current = st.selectbox("当前", options=jade_level_options, index=default_current, key=f"j_curr_{jade_name}")
                target = st.selectbox("目标", options=jade_level_options, index=default_target, key=f"j_tar_{jade_name}")
                JADES[jade_name] = {"current": current, "target": target}

st.markdown("---")

# --- 4. 原计算器核心逻辑（基本无需修改）---
WEAPON_UPGRADE_COSTS = [
    # 绿色等级 1-5
    [1000, 50, 0],     # 绿色1级
    [1500, 75, 0],     # 绿色2级
    [2000, 100, 0],    # 绿色3级
    [2500, 125, 0],    # 绿色4级
    [3000, 150, 0],    # 绿色5级
    
    # 蓝色等级 6-10
    [3500, 175, 0],    # 蓝色1级
    [4000, 200, 0],    # 蓝色2级
    [4500, 225, 0],    # 蓝色3级
    [5000, 250, 0],    # 蓝色4级
    [5500, 275, 0],    # 蓝色5级
    
    # 紫色等级 11-20
    [6000, 300, 150],  # 紫色1级
    [6500, 325, 160],  # 紫色2级
    [7000, 350, 170],  # 紫色3级
    [7500, 375, 180],  # 紫色4级
    [8000, 400, 180],  # 紫色5级
    [8500, 425, 190],  # 紫色6级
    [9000, 450, 200],  # 紫色7级
    [9500, 475, 200],  # 紫色8级
    [10000, 500, 210], # 紫色9级
    [10500, 525, 220], # 紫色10级
    
    # 红色等级 21-50
    [11000, 550, 220],   # 红色1级
    [12000, 600, 230],   # 红色2级
    [13000, 650, 250],   # 红色3级
    [14000, 700, 260],   # 红色4级
    [15000, 750, 270],   # 红色5级
    [16000, 800, 280],   # 红色6级
    [17000, 850, 290],   # 红色7级
    [18000, 900, 300],   # 红色8级
    [19000, 950, 300],   # 红色9级
    [20000, 1000, 310],  # 红色10级
    [21000, 1050, 320],  # 红色11级
    [22000, 1100, 320],  # 红色12级
    [23000, 1150, 320],  # 红色13级
    [24000, 1200, 320],  # 红色14级
    [25000, 1250, 330],  # 红色15级
    [26000, 1300, 330],  # 红色16级
    [27000, 1350, 340],  # 红色17级
    [28000, 1400, 350],  # 红色18级
    [29000, 1450, 360],  # 红色19级
    [30000, 1500, 360],  # 红色20级
    [31000, 1550, 360],  # 红色21级
    [32000, 1600, 370],  # 红色22级
    [33000, 1650, 380],  # 红色23级
    [34000, 1700, 390],  # 红色24级
    [35000, 1750, 390],  # 红色25级
    [36000, 1800, 400],  # 红色26级
    [37000, 1850, 410],  # 红色27级
    [38000, 1900, 420],  # 红色28级
    [39000, 1950, 430],  # 红色29级
    [40000, 2000, 440],  # 红色30级
]  # 【重要】请将你原代码中 WEAPON_UPGRADE_COSTS 的完整列表（第46-95行）复制粘贴到这里

JADE_UPGRADE_COSTS = [
    [2, 10],         # 1级
    [4, 12],        # 2级
    [6, 14],        # 3级
    [8, 16],        # 4级
    [10, 18],        # 5级
    [12, 20],        # 6级
    [16, 24],        # 7级
    [20, 28],        # 8级
    [30, 32],        # 9级
    [40, 36],       # 10级
    [60, 50],       # 11级
    [100, 60],       # 12级
    [140, 70],       # 13级
    [180, 80],       # 14级
    [220, 90],      # 15级
    [240, 100],      # 16级
    [240, 140],      # 17级
    [260, 180],      # 18级
    [260, 220],      # 19级
    [280, 260],      # 20级
    [300, 300],      # 21级
    [320, 340],      # 22级
    [340, 380],      # 23级
    [360, 420],      # 24级
    [380, 460],      # 25级
]    # 【重要】请将你原代码中 JADE_UPGRADE_COSTS 的完整列表（第98-123行）复制粘贴到这里

class UpgradeCalculator:
    def __init__(self):
        # 神兵相关
        self.current_points = CURRENT_POINTS
        self.points_per_wood = POINTS_PER_WOOD
        self.points_per_mithril = POINTS_PER_MITHRIL
        self.points_per_lapis = POINTS_PER_LAPIS
        self.current_wood = CURRENT_WOOD
        self.current_mithril = CURRENT_MITHRIL
        self.current_lapis = CURRENT_LAPIS
        self.weapons = WEAPONS
        self.weapon_upgrade_costs = WEAPON_UPGRADE_COSTS
        
        # 玉石相关
        self.points_per_carving_knife = POINTS_PER_CARVING_KNIFE
        self.points_per_unpolished_jade = POINTS_PER_UNPOLISHED_JADE
        self.current_carving_knife = CURRENT_CARVING_KNIFE
        self.current_unpolished_jade = CURRENT_UNPOLISHED_JADE
        self.jades = JADES
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
        
        raise ValueError(f"无效的等级格式: {level_str}")
    
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
    
    def calculate_weapon_upgrade(self, current_level_str, target_level_str):
        """计算单个神兵升级所需材料"""
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
        
        total_wood_needed = 0
        total_mithril_needed = 0
        total_lapis_needed = 0
        
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
        """计算单个玉石升级所需材料"""
        if target_level <= current_level:
            return {
                "current_level": current_level,
                "target_level": target_level,
                "total_knife_needed": 0,
                "total_jade_needed": 0,
                "levels_upgraded": 0,
                "need_upgrade": False
            }
    
        total_knife_needed = 0
        total_jade_needed = 0
    
        # 修复：使用 level 而不是 level-1 作为索引
        for level in range(current_level, target_level):
            cost_knife, cost_jade = self.jade_upgrade_costs[level]  # 修改这里
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
    
    def calculate_all_upgrades(self):
        """计算所有神兵和玉石升级需求"""
        # 神兵升级计算
        weapon_results = {}
        weapon_wood_needed = 0
        weapon_mithril_needed = 0
        weapon_lapis_needed = 0
        
        for weapon_name, levels in self.weapons.items():
            result = self.calculate_weapon_upgrade(levels["current"], levels["target"])
            weapon_results[weapon_name] = result
            
            weapon_wood_needed += result["total_wood_needed"]
            weapon_mithril_needed += result["total_mithril_needed"]
            weapon_lapis_needed += result["total_lapis_needed"]
        
        # 玉石升级计算
        jade_results = {}
        jade_knife_needed = 0
        jade_jade_needed = 0
        
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
        
        # 计算所需总积分
        total_points_needed = (
            wood_need_buy * self.points_per_wood +
            mithril_need_buy * self.points_per_mithril +
            lapis_need_buy * self.points_per_lapis +
            knife_need_buy * self.points_per_carving_knife +
            jade_need_buy * self.points_per_unpolished_jade
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
            "weapon_wood_needed": weapon_wood_needed,
            "weapon_mithril_needed": weapon_mithril_needed,
            "weapon_lapis_needed": weapon_lapis_needed,
            "jade_knife_needed": jade_knife_needed,
            "jade_jade_needed": jade_jade_needed,
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
    
    def print_results(self, results):
        """打印结果"""
        print("=" * 70)
        print("神兵与玉石升级计算器 - 结果汇总")
        print("=" * 70)
        
        print(f"\n📊 全局信息:")
        print(f"  当前积分: {self.current_points}")
        
        print(f"\n📦 材料库存:")
        print(f"  神兵材料: 木头×{self.current_wood}, 精金×{self.current_mithril}, 青金石×{self.current_lapis}")
        print(f"  玉石材料: 琢玉刀×{self.current_carving_knife}, 璞玉×{self.current_unpolished_jade}")
        
        print(f"\n💰 兑换比例:")
        print(f"  神兵: 木头{self.points_per_wood:.2f}积分/个, 精金{self.points_per_mithril}积分/个, 青金石{self.points_per_lapis}积分/个")
        print(f"  玉石: 琢玉刀{self.points_per_carving_knife}积分/个, 璞玉{self.points_per_unpolished_jade}积分/个")
        
        # 神兵升级详情
        print(f"\n⚔️ 神兵升级详情:")
        print("-" * 60)
        
        upgrading_weapons = [w for w, r in results["weapon_results"].items() if r["need_upgrade"]]
        if upgrading_weapons:
            for weapon_name, weapon_result in results["weapon_results"].items():
                if weapon_result['need_upgrade']:
                    current_target = f"{weapon_result['current_level']} → {weapon_result['target_level']}"
                    wood_needed = weapon_result['total_wood_needed']
                    mithril_needed = weapon_result['total_mithril_needed']
                    lapis_needed = weapon_result['total_lapis_needed']
                    
                    print(f"{weapon_name}: {current_target}")
                    print(f"  升级{weapon_result['levels_upgraded']}级，需要: 木头×{wood_needed}, 精金×{mithril_needed}, 青金石×{lapis_needed}")
        else:
            print("所有神兵均无需升级")
        
        # 玉石升级详情
        print(f"\n💎 玉石升级详情 (仅显示需要升级的):")
        print("-" * 60)
        
        upgrading_jades = [j for j, r in results["jade_results"].items() if r["need_upgrade"]]
        if upgrading_jades:
            for jade_name, jade_result in results["jade_results"].items():
                if jade_result['need_upgrade'] and jade_result['levels_upgraded'] > 0:
                    current_target = f"{jade_result['current_level']}级 → {jade_result['target_level']}级"
                    knife_needed = jade_result['total_knife_needed']
                    jade_needed = jade_result['total_jade_needed']
                    
                    print(f"{jade_name}: {current_target}")
                    print(f"  升级{jade_result['levels_upgraded']}级，需要: 琢玉刀×{knife_needed}, 璞玉×{jade_needed}")
        else:
            print("所有玉石均无需升级")
        
        print("-" * 60)
        
        # 材料需求汇总
        print(f"\n📋 材料需求汇总:")
        print(f"  神兵材料: 木头×{results['weapon_wood_needed']}, 精金×{results['weapon_mithril_needed']}, 青金石×{results['weapon_lapis_needed']}")
        print(f"  玉石材料: 琢玉刀×{results['jade_knife_needed']}, 璞玉×{results['jade_jade_needed']}")
        
        print(f"\n🛒 需要兑换的材料:")
        print(f"  神兵材料:")
        print(f"    木头: {results['wood_need_buy']} 个")
        print(f"    精金: {results['mithril_need_buy']} 个")
        print(f"    青金石: {results['lapis_need_buy']} 个")
        print(f"  玉石材料:")
        print(f"    琢玉刀: {results['knife_need_buy']} 个")
        print(f"    璞玉: {results['jade_need_buy']} 个")
        
        print(f"\n💰 积分需求:")
        print(f"  需要兑换积分: {results['total_points_needed']:.1f}")
        print(f"  当前可用积分: {results['current_points']}")
        print(f"  兑换后剩余积分: {results['points_left_after']:.1f}")
        
        print(f"\n📊 升级后材料剩余:")
        print(f"  神兵材料: 木头×{results['wood_left_after']}, 精金×{results['mithril_left_after']}, 青金石×{results['lapis_left_after']}")
        print(f"  玉石材料: 琢玉刀×{results['knife_left_after']}, 璞玉×{results['jade_left_after']}")
        
        print(f"\n{'='*30} 状态 {'='*30}")
        if results['can_upgrade']:
            print("✅ 积分充足，可以完成所有升级！")
        else:
            print(f"⚠️ 积分不足！还差 {results['points_shortage']:.1f} 积分")
        
        print(f"\n📈 统计信息:")
        print(f"  需要升级的神兵数量: {len(upgrading_weapons)} 个")
        print(f"  需要升级的玉石数量: {len(upgrading_jades)} 个")
        
        print("=" * 70)
    
    def run(self):
        """运行计算器"""
        results = self.calculate_all_upgrades()
        self.print_results(results)  

    # 【重要】将你原代码中从第125行 class UpgradeCalculator: 开始，一直到 def run(self): 方法结束（约第398行）的整个类定义，完整地复制粘贴到这里
    # 注意：只需要复制类定义本身，最后的运行代码 if __name__ == "__main__": 不需要
    
# --- 5. 计算并展示结果 ---
    st.header("📊 计算结果")

if st.button("🚀 开始计算", type="primary", use_container_width=True):
    with st.spinner("正在计算升级需求..."):
        # 初始化计算器，传入用户输入的动态值
        calculator = UpgradeCalculator()
        # （重要）这里需要根据上面的用户输入，更新计算器实例中的变量
        calculator.current_points = CURRENT_POINTS
        calculator.current_wood = CURRENT_WOOD
        calculator.current_mithril = CURRENT_MITHRIL
        calculator.current_lapis = CURRENT_LAPIS
        calculator.current_carving_knife = CURRENT_CARVING_KNIFE
        calculator.current_unpolished_jade = CURRENT_UNPOLISHED_JADE
        calculator.points_per_wood = POINTS_PER_WOOD
        calculator.points_per_mithril = POINTS_PER_MITHRIL
        calculator.points_per_lapis = POINTS_PER_LAPIS
        calculator.points_per_carving_knife = POINTS_PER_CARVING_KNIFE
        calculator.points_per_unpolished_jade = POINTS_PER_UNPOLISHED_JADE
        calculator.weapons = WEAPONS
        calculator.jades = JADES
        
        # 执行计算
        results = calculator.calculate_all_upgrades()
        
    # --- 展示结果，使用Streamlit组件美化 ---
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
        tab1, tab2 = st.tabs(["神兵材料", "玉石材料"])
        with tab1:
            c1, c2, c3 = st.columns(3)
            c1.metric("木头需求/剩余", f"{results['weapon_wood_needed']} / {results['wood_left_after']}")
            c2.metric("精金需求/剩余", f"{results['weapon_mithril_needed']} / {results['mithril_left_after']}")
            c3.metric("青金石需求/剩余", f"{results['weapon_lapis_needed']} / {results['lapis_left_after']}")
        with tab2:
            c1, c2 = st.columns(2)
            c1.metric("琢玉刀需求/剩余", f"{results['jade_knife_needed']} / {results['knife_left_after']}")
            c2.metric("璞玉需求/剩余", f"{results['jade_jade_needed']} / {results['jade_left_after']}")
    
    # 需要购买的材料
    if any([results['wood_need_buy'], results['mithril_need_buy'], results['lapis_need_buy'], results['knife_need_buy'], results['jade_need_buy']]):
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
        else:
            st.info("所有玉石均无需升级")
            
st.markdown("---")
st.caption("提示：在侧边栏修改数据后，点击上方'开始计算'按钮更新结果。")
