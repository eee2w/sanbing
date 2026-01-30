import streamlit as st
import pandas as pd

# ============= Streamlit 网页应用 =============
#材料自动兑换计算-Material Exchange Auto-Recommendation
st.set_page_config(page_title="神兵玉石自动升级计算器", layout="wide")
st.title("⚔️💎 神兵玉石自动升级计算器")
st.info("""
1、点击左上角双箭头填写积分和材料数量  
2、选择步兵比弓兵神兵玉石高多少级（默认神兵5级玉石2级）  
3、设置玉石等级是神兵等级百分比（默认40%）  
4、选择目前步兵弓兵上下神兵玉石等级  
5、点击计算得到结果  
""")
st.markdown("---")

# --- 版本选择 ---
version = st.radio("选择版本:", ["详细版 (分别设置上下)", "简略版 (统一设置)"], horizontal=True)

if version == "详细版 (分别设置上下)":
    st.info("详细版：设置每一个神兵玉石等级")
else:
    st.info("""
    简略版：每个兵种的神兵上下相同，玉石8个相同。计算结果为上下全部加起来的总消耗
    """)

st.markdown("---")

# --- 1. 用户输入区（放在侧边栏）---
with st.sidebar:
    st.header("📝 资源与等级设置")
    
    # 全局积分
    CURRENT_POINTS = st.number_input("当前积分", min_value=0, value=0, step=1)
    
    st.subheader("神兵材料库存")
    CURRENT_WOOD = st.number_input("木头数量", min_value=0, value=0, step=1)
    CURRENT_MITHRIL = st.number_input("精金数量", min_value=0, value=0, step=1)
    CURRENT_LAPIS = st.number_input("青金石数量", min_value=0, value=0, step=1)
    
    st.subheader("玉石材料库存")
    CURRENT_CARVING_KNIFE = st.number_input("琢玉刀数量", min_value=0, value=0, step=1)
    CURRENT_UNPOLISHED_JADE = st.number_input("璞玉数量", min_value=0, value=0, step=1)
    
    st.subheader("兑换比例")
    POINTS_PER_WOOD = st.number_input("木头兑换比例", min_value=0.0, value=0.1, step=0.1, format="%.2f")
    POINTS_PER_MITHRIL = st.number_input("精金兑换比例", min_value=0.0, value=2.0, step=0.1, format="%.2f")
    POINTS_PER_LAPIS = st.number_input("青金石兑换比例", min_value=0.0, value=6.0, step=0.1, format="%.2f")
    POINTS_PER_CARVING_KNIFE = st.number_input("琢玉刀兑换比例", min_value=0.0, value=30.0, step=1.0, format="%.2f")
    POINTS_PER_UNPOLISHED_JADE = st.number_input("璞玉兑换比例", min_value=0.0, value=6.0, step=0.1, format="%.2f")
    
    st.subheader("等级差设置")
    st.caption("步兵等级比弓兵高多少级？")
    
    col1, col2 = st.columns(2)
    with col1:
        WEAPON_LEVEL_DIFF = st.number_input(
            "神兵等级差", 
            min_value=0, 
            max_value=10, 
            value=5, 
            step=1,
            help="步兵神兵比弓兵神兵高的级数"
        )
    with col2:
        JADE_LEVEL_DIFF = st.number_input(
            "玉石等级差", 
            min_value=0, 
            max_value=10, 
            value=2, 
            step=1,
            help="步兵玉石比弓兵玉石高的级数"
        )
    
    st.subheader("神兵玉石平衡设置")
    JADE_PERCENTAGE = st.number_input(
        "玉石等级是神兵等级的百分比", 
        min_value=10, 
        max_value=100, 
        value=40, 
        step=1,
        format="%d",
        help="玉石等级需要达到神兵最低等级的百分比（使用最低等级计算）"
    )
    st.caption(f"当前设置：玉石等级需要达到神兵最低等级的{JADE_PERCENTAGE}%")

st.markdown("---")

# --- 2. 当前等级输入（根据版本显示不同界面）---
WEAPONS = {}  # 存储神兵数据
JADES = {}    # 存储玉石数据

if version == "详细版 (分别设置上下)":
    st.header("🎯 当前等级设置 - 详细版")
    st.caption("分别设置步兵和弓兵的神兵上下、玉石上下各4个")
    
    # 定义等级选项
    weapon_level_options = ["未拥有"] + [f"绿色{i}级" for i in range(1, 6)] + [f"蓝色{i}级" for i in range(1, 6)] + [f"紫色{i}级" for i in range(1, 11)] + [f"红色{i}级" for i in range(1, 31)]
    jade_level_options = list(range(0, 26))
    
    # --- 神兵设置 ---
    st.subheader("⚔️ 神兵设置")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**步兵神兵**")
        foot_weapon_up = st.selectbox("步兵上", options=weapon_level_options, 
                                      index=weapon_level_options.index("未拥有"), key="foot_weapon_up")
        foot_weapon_down = st.selectbox("步兵下", options=weapon_level_options, 
                                        index=weapon_level_options.index("未拥有"), key="foot_weapon_down")
        
        # 存储到WEAPONS字典
        WEAPONS["步兵上"] = {"current": foot_weapon_up, "type": "foot"}
        WEAPONS["步兵下"] = {"current": foot_weapon_down, "type": "foot"}
    
    with col2:
        st.markdown("**弓兵神兵**")
        archer_weapon_up = st.selectbox("弓兵上", options=weapon_level_options, 
                                        index=weapon_level_options.index("未拥有"), key="archer_weapon_up")
        archer_weapon_down = st.selectbox("弓兵下", options=weapon_level_options, 
                                          index=weapon_level_options.index("未拥有"), key="archer_weapon_down")
        
        # 存储到WEAPONS字典
        WEAPONS["弓兵上"] = {"current": archer_weapon_up, "type": "archer"}
        WEAPONS["弓兵下"] = {"current": archer_weapon_down, "type": "archer"}
    
    st.markdown("---")
    
    # --- 玉石设置 ---
    st.subheader("💎 玉石设置")
    st.caption("每个兵种的玉石上下各4个，共8个")
    
    # 步兵玉石
    with st.expander("步兵玉石 (上下各4个，共8个)", expanded=True):
        st.markdown("**步兵玉石 - 上位置 (1-4号)**")
        foot_jade_up_cols = st.columns(4)
        foot_jade_up_levels = []
        for i in range(4):
            with foot_jade_up_cols[i]:
                level = st.selectbox(f"上{i+1}", options=jade_level_options, index=0, 
                                    key=f"foot_jade_up_{i}")
                foot_jade_up_levels.append(level)
                JADES[f"步兵上{i+1}"] = {"current": level, "type": "foot"}
        
        st.markdown("**步兵玉石 - 下位置 (1-4号)**")
        foot_jade_down_cols = st.columns(4)
        foot_jade_down_levels = []
        for i in range(4):
            with foot_jade_down_cols[i]:
                level = st.selectbox(f"下{i+1}", options=jade_level_options, index=0, 
                                    key=f"foot_jade_down_{i}")
                foot_jade_down_levels.append(level)
                JADES[f"步兵下{i+1}"] = {"current": level, "type": "foot"}
    
    # 弓兵玉石
    with st.expander("弓兵玉石 (上下各4个，共8个)", expanded=False):
        st.markdown("**弓兵玉石 - 上位置 (1-4号)**")
        archer_jade_up_cols = st.columns(4)
        archer_jade_up_levels = []
        for i in range(4):
            with archer_jade_up_cols[i]:
                level = st.selectbox(f"上{i+1}", options=jade_level_options, index=0, 
                                    key=f"archer_jade_up_{i}")
                archer_jade_up_levels.append(level)
                JADES[f"弓兵上{i+1}"] = {"current": level, "type": "archer"}
        
        st.markdown("**弓兵玉石 - 下位置 (1-4号)**")
        archer_jade_down_cols = st.columns(4)
        archer_jade_down_levels = []
        for i in range(4):
            with archer_jade_down_cols[i]:
                level = st.selectbox(f"下{i+1}", options=jade_level_options, index=0, 
                                    key=f"archer_jade_down_{i}")
                archer_jade_down_levels.append(level)
                JADES[f"弓兵下{i+1}"] = {"current": level, "type": "archer"}

else:
    st.header("🎯 当前等级设置 - 简略版")
    st.caption("每个兵种的神兵上下相同，玉石8个相同")
    
    # 定义等级选项
    weapon_level_options = ["未拥有"] + [f"绿色{i}级" for i in range(1, 6)] + [f"蓝色{i}级" for i in range(1, 6)] + [f"紫色{i}级" for i in range(1, 11)] + [f"红色{i}级" for i in range(1, 31)]
    jade_level_options = list(range(0, 26))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("步兵")
        foot_weapon = st.selectbox("神兵等级", options=weapon_level_options, 
                                  index=weapon_level_options.index("未拥有"), key="foot_weapon_simple")
        foot_jade = st.selectbox("玉石等级", options=jade_level_options, index=0, 
                                key="foot_jade_simple")
        
        # 存储神兵数据（上下相同）
        WEAPONS["步兵上"] = {"current": foot_weapon, "type": "foot"}
        WEAPONS["步兵下"] = {"current": foot_weapon, "type": "foot"}
        
        # 存储玉石数据（8个相同）
        for i in range(1, 5):
            JADES[f"步兵上{i}"] = {"current": foot_jade, "type": "foot"}
            JADES[f"步兵下{i}"] = {"current": foot_jade, "type": "foot"}
    
    with col2:
        st.subheader("弓兵")
        archer_weapon = st.selectbox("神兵等级", options=weapon_level_options, 
                                    index=weapon_level_options.index("未拥有"), key="archer_weapon_simple")
        archer_jade = st.selectbox("玉石等级", options=jade_level_options, index=0, 
                                  key="archer_jade_simple")
        
        # 存储神兵数据（上下相同）
        WEAPONS["弓兵上"] = {"current": archer_weapon, "type": "archer"}
        WEAPONS["弓兵下"] = {"current": archer_weapon, "type": "archer"}
        
        # 存储玉石数据（8个相同）
        for i in range(1, 5):
            JADES[f"弓兵上{i}"] = {"current": archer_jade, "type": "archer"}
            JADES[f"弓兵下{i}"] = {"current": archer_jade, "type": "archer"}

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
    def __init__(self, version_type, weapons, jades):
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
        
        # 当前等级数据
        self.weapons = weapons
        self.jades = jades
        
        # 等级差
        self.weapon_level_diff = WEAPON_LEVEL_DIFF
        self.jade_level_diff = JADE_LEVEL_DIFF
        
        # 玉石百分比设置
        self.jade_percentage = JADE_PERCENTAGE / 100.0  # 转换为小数
        
        # 版本类型
        self.version_type = version_type
        
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
    
    def get_min_levels(self, weapon_nums, jade_nums):
        """获取每个兵种的神兵和玉石最低等级"""
        # 步兵神兵最低等级
        foot_weapon_keys = [k for k in weapon_nums.keys() if "步兵" in k]
        foot_weapon_levels = [weapon_nums[k] for k in foot_weapon_keys]
        foot_weapon_min = min(foot_weapon_levels) if foot_weapon_levels else 0
        
        # 弓兵神兵最低等级
        archer_weapon_keys = [k for k in weapon_nums.keys() if "弓兵" in k]
        archer_weapon_levels = [weapon_nums[k] for k in archer_weapon_keys]
        archer_weapon_min = min(archer_weapon_levels) if archer_weapon_levels else 0
        
        # 步兵玉石最低等级
        foot_jade_keys = [k for k in jade_nums.keys() if "步兵" in k]
        foot_jade_levels = [jade_nums[k] for k in foot_jade_keys]
        foot_jade_min = min(foot_jade_levels) if foot_jade_levels else 0
        
        # 弓兵玉石最低等级
        archer_jade_keys = [k for k in jade_nums.keys() if "弓兵" in k]
        archer_jade_levels = [jade_nums[k] for k in archer_jade_keys]
        archer_jade_min = min(archer_jade_levels) if archer_jade_levels else 0
        
        return {
            "foot_weapon_min": foot_weapon_min,
            "archer_weapon_min": archer_weapon_min,
            "foot_jade_min": foot_jade_min,
            "archer_jade_min": archer_jade_min
        }
    
    def calculate_normalized_levels(self, min_levels):
        """计算归一化等级"""
        # 步兵神兵归一化等级 = 步兵神兵最低等级
        foot_weapon_norm = min_levels["foot_weapon_min"]
        
        # 弓兵神兵归一化等级 = 弓兵神兵最低等级 + 神兵等级差
        archer_weapon_norm = min_levels["archer_weapon_min"] + self.weapon_level_diff
        
        # 步兵玉石归一化等级 = 步兵玉石最低等级 / 百分比
        if self.jade_percentage > 0:
            foot_jade_norm = min_levels["foot_jade_min"] / self.jade_percentage
        else:
            foot_jade_norm = float('inf')  # 避免除以0
            
        # 弓兵玉石归一化等级 = (弓兵玉石最低等级 + 玉石等级差) / 百分比
        if self.jade_percentage > 0:
            archer_jade_norm = (min_levels["archer_jade_min"] + self.jade_level_diff) / self.jade_percentage
        else:
            archer_jade_norm = float('inf')
        
        return {
            "foot_weapon_norm": foot_weapon_norm,
            "archer_weapon_norm": archer_weapon_norm,
            "foot_jade_norm": foot_jade_norm,
            "archer_jade_norm": archer_jade_norm
        }
    
    def find_item_to_upgrade(self, weapon_nums, jade_nums, normalized_levels):
        """根据归一化等级找出需要升级的项目"""
        # 找到归一化等级最小的项目
        min_norm = float('inf')
        upgrade_type = None  # 'foot_weapon', 'archer_weapon', 'foot_jade', 'archer_jade'
        
        for norm_type, norm_value in normalized_levels.items():
            if norm_value < min_norm:
                min_norm = norm_value
                upgrade_type = norm_type
        
        # 根据项目类型找到具体要升级的物品
        item_name = None
        is_weapon = False
        
        if upgrade_type == "foot_weapon":
            # 找到步兵中等级最低的神兵
            foot_weapon_keys = [k for k in weapon_nums.keys() if "步兵" in k]
            min_level = min([weapon_nums[k] for k in foot_weapon_keys])
            for k in foot_weapon_keys:
                if weapon_nums[k] == min_level:
                    item_name = k
                    break
            is_weapon = True
            
        elif upgrade_type == "archer_weapon":
            # 找到弓兵中等级最低的神兵
            archer_weapon_keys = [k for k in weapon_nums.keys() if "弓兵" in k]
            min_level = min([weapon_nums[k] for k in archer_weapon_keys])
            for k in archer_weapon_keys:
                if weapon_nums[k] == min_level:
                    item_name = k
                    break
            is_weapon = True
            
        elif upgrade_type == "foot_jade":
            # 找到步兵中等级最低的玉石
            foot_jade_keys = [k for k in jade_nums.keys() if "步兵" in k]
            min_level = min([jade_nums[k] for k in foot_jade_keys])
            for k in foot_jade_keys:
                if jade_nums[k] == min_level:
                    item_name = k
                    break
            is_weapon = False
            
        elif upgrade_type == "archer_jade":
            # 找到弓兵中等级最低的玉石
            archer_jade_keys = [k for k in jade_nums.keys() if "弓兵" in k]
            min_level = min([jade_nums[k] for k in archer_jade_keys])
            for k in archer_jade_keys:
                if jade_nums[k] == min_level:
                    item_name = k
                    break
            is_weapon = False
        
        return item_name, is_weapon, upgrade_type
    
    def check_and_use_resources(self, cost, current_resources, points_left, is_weapon=True):
        """检查并消耗资源，如果库存不足则使用积分兑换"""
        if is_weapon:
            # 神兵材料
            wood_needed = cost.get("wood", 0)
            mithril_needed = cost.get("mithril", 0)
            lapis_needed = cost.get("lapis", 0)
            
            # 计算需要兑换的材料
            wood_deficit = max(0, wood_needed - current_resources.get("wood", 0))
            mithril_deficit = max(0, mithril_needed - current_resources.get("mithril", 0))
            lapis_deficit = max(0, lapis_needed - current_resources.get("lapis", 0))
            
            # 计算所需积分
            points_needed = (
                wood_deficit * self.points_per_wood +
                mithril_deficit * self.points_per_mithril +
                lapis_deficit * self.points_per_lapis
            )
            
            # 检查积分是否足够
            if points_left < points_needed:
                return False, current_resources, points_left, points_needed
            
            # 消耗资源
            current_resources["wood"] = max(0, current_resources.get("wood", 0) - wood_needed)
            current_resources["mithril"] = max(0, current_resources.get("mithril", 0) - mithril_needed)
            current_resources["lapis"] = max(0, current_resources.get("lapis", 0) - lapis_needed)
            
            # 扣除积分
            points_left -= points_needed
            
            return True, current_resources, points_left, points_needed
        else:
            # 玉石材料
            knife_needed = cost.get("knife", 0)
            jade_needed = cost.get("jade", 0)
            
            # 计算需要兑换的材料
            knife_deficit = max(0, knife_needed - current_resources.get("knife", 0))
            jade_deficit = max(0, jade_needed - current_resources.get("jade", 0))
            
            # 计算所需积分
            points_needed = (
                knife_deficit * self.points_per_carving_knife +
                jade_deficit * self.points_per_unpolished_jade
            )
            
            # 检查积分是否足够
            if points_left < points_needed:
                return False, current_resources, points_left, points_needed
            
            # 消耗资源
            current_resources["knife"] = max(0, current_resources.get("knife", 0) - knife_needed)
            current_resources["jade"] = max(0, current_resources.get("jade", 0) - jade_needed)
            
            # 扣除积分
            points_left -= points_needed
            
            return True, current_resources, points_left, points_needed
    
    def find_max_levels(self):
        """按照新逻辑寻找在当前资源下能达到的最高等级"""
        # 初始化结果
        result = {
            "upgraded": False,
            "weapon_targets": {},
            "jade_targets": {},
            "points_needed": 0,
            "materials_to_buy": {},
            "materials_used": {},
            "materials_needed": {},
            "points_left": self.current_points
        }
        
        # 将当前等级转换为数字并存储
        weapon_current_nums = {}
        for weapon_name, weapon_info in self.weapons.items():
            weapon_current_nums[weapon_name] = self.level_str_to_number(weapon_info["current"])
        
        jade_current_nums = {}
        for jade_name, jade_info in self.jades.items():
            jade_current_nums[jade_name] = jade_info["current"]
        
        # 目标等级初始化为当前等级
        weapon_target_nums = weapon_current_nums.copy()
        jade_target_nums = jade_current_nums.copy()
        
        # 尝试升级
        upgraded = False
        
        # 初始化当前资源
        current_resources = {
            "wood": self.current_wood,
            "mithril": self.current_mithril,
            "lapis": self.current_lapis,
            "knife": self.current_carving_knife,
            "jade": self.current_unpolished_jade
        }
        
        points_left = self.current_points
        total_points_used = 0  # 总共使用的积分
        
        # 记录升级历史（用于调试）
        upgrade_history = []
        
        # 开始循环升级
        continue_upgrading = True
        while continue_upgrading:
            # 获取最低等级
            min_levels = self.get_min_levels(weapon_target_nums, jade_target_nums)
            
            # 计算归一化等级
            normalized_levels = self.calculate_normalized_levels(min_levels)
            
            # 找出需要升级的项目
            item_name, is_weapon, upgrade_type = self.find_item_to_upgrade(
                weapon_target_nums, jade_target_nums, normalized_levels
            )
            
            if item_name is None:
                # 没有找到可升级的项目
                continue_upgrading = False
                break
            
            # 获取当前等级和目标等级
            if is_weapon:
                current_num = weapon_target_nums[item_name]
                target_num = current_num + 1
                
                # 检查是否达到最大等级
                if current_num >= len(self.weapon_upgrade_costs):
                    # 标记这个项目已达到最大等级，需要重新选择
                    # 暂时给一个很大的归一化值，使其不会被选中
                    normalized_levels[upgrade_type] = float('inf')
                    continue
                
                # 计算升级成本
                cost = self.calculate_upgrade_cost(current_num, target_num, "weapon")
            else:
                current_num = jade_target_nums[item_name]
                target_num = current_num + 1
                
                # 检查是否达到最大等级
                if current_num >= len(self.jade_upgrade_costs):
                    # 标记这个项目已达到最大等级，需要重新选择
                    normalized_levels[upgrade_type] = float('inf')
                    continue
                
                # 计算升级成本
                cost = self.calculate_upgrade_cost(current_num, target_num, "jade")
            
            # 检查并消耗资源
            can_upgrade, current_resources, points_left, points_needed = self.check_and_use_resources(
                cost, current_resources, points_left, is_weapon=is_weapon
            )
            
            if can_upgrade:
                # 记录升级
                upgrade_history.append({
                    "item": item_name,
                    "type": "weapon" if is_weapon else "jade",
                    "from_level": current_num,
                    "to_level": target_num,
                    "cost": cost,
                    "points_needed": points_needed
                })
                
                # 更新目标等级
                if is_weapon:
                    weapon_target_nums[item_name] = target_num
                else:
                    jade_target_nums[item_name] = target_num
                
                upgraded = True
                total_points_used += points_needed
            else:
                # 资源不足，停止升级
                continue_upgrading = False
        
        if not upgraded:
            return result
        
        # 计算总消耗
        total_wood_needed = 0
        total_mithril_needed = 0
        total_lapis_needed = 0
        total_knife_needed = 0
        total_jade_needed = 0
        
        # 神兵消耗
        for weapon_name, current_num in weapon_current_nums.items():
            target_num = weapon_target_nums[weapon_name]
            cost = self.calculate_upgrade_cost(current_num, target_num, "weapon")
            total_wood_needed += cost["wood"]
            total_mithril_needed += cost["mithril"]
            total_lapis_needed += cost["lapis"]
        
        # 玉石消耗
        for jade_name, current_num in jade_current_nums.items():
            target_num = jade_target_nums[jade_name]
            cost = self.calculate_upgrade_cost(current_num, target_num, "jade")
            total_knife_needed += cost["knife"]
            total_jade_needed += cost["jade"]
        
        # 合并所有材料需求
        total_materials_needed = {
            "wood": total_wood_needed,
            "mithril": total_mithril_needed,
            "lapis": total_lapis_needed,
            "knife": total_knife_needed,
            "jade": total_jade_needed
        }
        
        # 计算需要购买的材料
        materials_to_buy = {
            "wood_need_buy": max(0, total_wood_needed - self.current_wood),
            "mithril_need_buy": max(0, total_mithril_needed - self.current_mithril),
            "lapis_need_buy": max(0, total_lapis_needed - self.current_lapis),
            "knife_need_buy": max(0, total_knife_needed - self.current_carving_knife),
            "jade_need_buy": max(0, total_jade_needed - self.current_unpolished_jade)
        }
        
        # 计算升级后剩余材料
        materials_used = {
            "wood": min(self.current_wood, total_materials_needed.get("wood", 0)),
            "mithril": min(self.current_mithril, total_materials_needed.get("mithril", 0)),
            "lapis": min(self.current_lapis, total_materials_needed.get("lapis", 0)),
            "knife": min(self.current_carving_knife, total_materials_needed.get("knife", 0)),
            "jade": min(self.current_unpolished_jade, total_materials_needed.get("jade", 0))
        }
        
        # 计算剩余积分
        points_left = self.current_points - total_points_used
        
        # 计算玉石百分比实际值
        min_levels_final = self.get_min_levels(weapon_target_nums, jade_target_nums)
        foot_actual_percentage = (min_levels_final["foot_jade_min"] / min_levels_final["foot_weapon_min"] * 100) if min_levels_final["foot_weapon_min"] > 0 else 0
        archer_actual_percentage = (min_levels_final["archer_jade_min"] / min_levels_final["archer_weapon_min"] * 100) if min_levels_final["archer_weapon_min"] > 0 else 0
        
        # 计算最终的归一化等级（用于显示）
        final_normalized_levels = self.calculate_normalized_levels(min_levels_final)
        
        result = {
            "upgraded": True,
            "weapon_targets": weapon_target_nums,
            "jade_targets": jade_target_nums,
            "weapon_currents": weapon_current_nums,
            "jade_currents": jade_current_nums,
            "points_needed": total_points_used,
            "materials_to_buy": materials_to_buy,
            "materials_used": materials_used,
            "materials_needed": total_materials_needed,
            "points_left": points_left,
            "foot_weapon_min": min_levels_final["foot_weapon_min"],
            "archer_weapon_min": min_levels_final["archer_weapon_min"],
            "foot_jade_min": min_levels_final["foot_jade_min"],
            "archer_jade_min": min_levels_final["archer_jade_min"],
            "foot_actual_percentage": foot_actual_percentage,
            "archer_actual_percentage": archer_actual_percentage,
            "normalized_levels": final_normalized_levels,
            "upgrade_history": upgrade_history
        }
        
        return result

# --- 4. 计算并展示结果 ---
st.header("🚀 自动升级计算")

if st.button("开始自动计算最佳升级方案", type="primary", use_container_width=True):
    with st.spinner("正在计算最佳升级方案..."):
        calculator = AutoUpgradeCalculator(version, WEAPONS, JADES)
        result = calculator.find_max_levels()
    
    if not result["upgraded"]:
        st.warning("当前积分和材料无法进行任何升级！请检查您的资源或降低等级差设置。")
    else:
        st.success("计算完成！")
        
        # 显示结果总览
        st.subheader("🎯 最佳升级方案")
        
        # 显示归一化等级信息
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**步兵神兵归一化等级**: {result.get('normalized_levels', {}).get('foot_weapon_norm', 0):.2f}")
            st.info(f"**弓兵神兵归一化等级**: {result.get('normalized_levels', {}).get('archer_weapon_norm', 0):.2f}")
        with col2:
            st.info(f"**步兵玉石归一化等级**: {result.get('normalized_levels', {}).get('foot_jade_norm', 0):.2f}")
            st.info(f"**弓兵玉石归一化等级**: {result.get('normalized_levels', {}).get('archer_jade_norm', 0):.2f}")
        
        # 显示玉石百分比信息
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**步兵玉石百分比**: {result.get('foot_actual_percentage', 0):.1f}% (目标: {JADE_PERCENTAGE}%)")
        with col2:
            st.info(f"**弓兵玉石百分比**: {result.get('archer_actual_percentage', 0):.1f}% (目标: {JADE_PERCENTAGE}%)")
        
        if version == "详细版 (分别设置上下)":
            # 详细版显示方式
            cols = st.columns(4)
            
            with cols[0]:
                st.metric("步兵神兵上", 
                         f"{calculator.level_number_to_str(result['weapon_targets']['步兵上'])}",
                         f"升级{result['weapon_targets']['步兵上'] - result['weapon_currents']['步兵上']}级")
            
            with cols[1]:
                st.metric("步兵神兵下", 
                         f"{calculator.level_number_to_str(result['weapon_targets']['步兵下'])}",
                         f"升级{result['weapon_targets']['步兵下'] - result['weapon_currents']['步兵下']}级")
            
            with cols[2]:
                st.metric("弓兵神兵上", 
                         f"{calculator.level_number_to_str(result['weapon_targets']['弓兵上'])}",
                         f"升级{result['weapon_targets']['弓兵上'] - result['weapon_currents']['弓兵上']}级")
            
            with cols[3]:
                st.metric("弓兵神兵下", 
                         f"{calculator.level_number_to_str(result['weapon_targets']['弓兵下'])}",
                         f"升级{result['weapon_targets']['弓兵下'] - result['weapon_currents']['弓兵下']}级")
            
            # 玉石结果
            st.subheader("💎 玉石升级结果")
            
            # 步兵玉石
            st.markdown("**步兵玉石**")
            foot_jade_cols = st.columns(8)
            for i in range(1, 5):
                with foot_jade_cols[i-1]:
                    st.metric(f"上{i}", 
                             f"{result['jade_targets'][f'步兵上{i}']}级",
                             f"+{result['jade_targets'][f'步兵上{i}'] - result['jade_currents'][f'步兵上{i}']}")
            
            for i in range(1, 5):
                with foot_jade_cols[i+3]:
                    st.metric(f"下{i}", 
                             f"{result['jade_targets'][f'步兵下{i}']}级",
                             f"+{result['jade_targets'][f'步兵下{i}'] - result['jade_currents'][f'步兵下{i}']}")
            
            # 弓兵玉石
            st.markdown("**弓兵玉石**")
            archer_jade_cols = st.columns(8)
            for i in range(1, 5):
                with archer_jade_cols[i-1]:
                    st.metric(f"上{i}", 
                             f"{result['jade_targets'][f'弓兵上{i}']}级",
                             f"+{result['jade_targets'][f'弓兵上{i}'] - result['jade_currents'][f'弓兵上{i}']}")
            
            for i in range(1, 5):
                with archer_jade_cols[i+3]:
                    st.metric(f"下{i}", 
                             f"{result['jade_targets'][f'弓兵下{i}']}级",
                             f"+{result['jade_targets'][f'弓兵下{i}'] - result['jade_currents'][f'弓兵下{i}']}")
        
        else:
            # 简略版显示方式
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("步兵神兵", 
                         f"{calculator.level_number_to_str(result['weapon_targets']['步兵上'])}",
                         f"升级{result['weapon_targets']['步兵上'] - result['weapon_currents']['步兵上']}级")
                
                st.markdown("**步兵玉石** (8个相同)")
                st.metric("玉石等级", 
                         f"{result['jade_targets']['步兵上1']}级",
                         f"升级{result['jade_targets']['步兵上1'] - result['jade_currents']['步兵上1']}级")
            
            with col2:
                st.metric("弓兵神兵", 
                         f"{calculator.level_number_to_str(result['weapon_targets']['弓兵上'])}",
                         f"升级{result['weapon_targets']['弓兵上'] - result['weapon_currents']['弓兵上']}级")
                
                st.markdown("**弓兵玉石** (8个相同)")
                st.metric("玉石等级", 
                         f"{result['jade_targets']['弓兵上1']}级",
                         f"升级{result['jade_targets']['弓兵上1'] - result['jade_currents']['弓兵上1']}级")
        
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
        
        with st.expander("查看升级详情表格", expanded=False):
            # 神兵升级详情
            st.write("**神兵升级详情:**")
            weapon_data = []
            for weapon_name in ["步兵上", "步兵下", "弓兵上", "弓兵下"]:
                current_level = WEAPONS[weapon_name]["current"]
                target_level = calculator.level_number_to_str(result['weapon_targets'][weapon_name])
                upgrade_levels = result['weapon_targets'][weapon_name] - result['weapon_currents'][weapon_name]
                
                weapon_data.append({
                    "神兵": weapon_name,
                    "当前等级": current_level,
                    "目标等级": target_level,
                    "升级级数": upgrade_levels
                })
            st.dataframe(pd.DataFrame(weapon_data), use_container_width=True)
            
            # 玉石升级详情
            st.write("**玉石升级详情:**")
            jade_data = []
            for jade_name in sorted(JADES.keys()):
                if jade_name in result['jade_targets']:
                    current_level = JADES[jade_name]["current"]
                    target_level = result['jade_targets'][jade_name]
                    upgrade_levels = target_level - current_level
                    
                    jade_data.append({
                        "玉石": jade_name,
                        "当前等级": current_level,
                        "目标等级": target_level,
                        "升级级数": upgrade_levels
                    })
            st.dataframe(pd.DataFrame(jade_data), use_container_width=True)
            
            # 玉石百分比详情
            st.write("**玉石百分比详情:**")
            percentage_data = []
            percentage_data.append({
                "兵种": "步兵",
                "神兵最低等级": result.get('foot_weapon_min', 0),
                "玉石最低等级": result.get('foot_jade_min', 0),
                "实际百分比": f"{result.get('foot_actual_percentage', 0):.1f}%",
                "目标百分比": f"{JADE_PERCENTAGE}%"
            })
            percentage_data.append({
                "兵种": "弓兵",
                "神兵最低等级": result.get('archer_weapon_min', 0),
                "玉石最低等级": result.get('archer_jade_min', 0),
                "实际百分比": f"{result.get('archer_actual_percentage', 0):.1f}%",
                "目标百分比": f"{JADE_PERCENTAGE}%"
            })
            st.dataframe(pd.DataFrame(percentage_data), use_container_width=True)
            
            # 升级顺序详情（可选）
            if 'upgrade_history' in result and result['upgrade_history']:
                st.write("**升级顺序详情:**")
                history_data = []
                for i, upgrade in enumerate(result['upgrade_history']):
                    history_data.append({
                        "序号": i+1,
                        "升级项目": upgrade['item'],
                        "类型": "神兵" if upgrade['type'] == 'weapon' else "玉石",
                        "从等级": upgrade['from_level'],
                        "到等级": upgrade['to_level'],
                        "消耗积分": f"{upgrade['points_needed']:.1f}"
                    })
                st.dataframe(pd.DataFrame(history_data), use_container_width=True)

st.markdown("---")
st.caption("提示：修改侧边栏的设置后，点击上方按钮重新计算。切换版本后，当前设置会被重置。")
