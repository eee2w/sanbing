import streamlit as st
import webbrowser
from streamlit.components.v1 import html

# 设置页面配置
st.set_page_config(
    page_title="游戏工具导航",
    page_icon="🎮",
    layout="centered"
)

# 自定义CSS样式
st.markdown("""
<style>
    .header {
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 30px;
        color: white;
    }
    
    .app-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .app-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    
    .app-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    
    .app-description {
        font-size: 0.95rem;
        color: #666;
        margin-bottom: 15px;
    }
    
    .app-link {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
        transition: background 0.3s ease;
    }
    
    .app-link:hover {
        background: #764ba2;
        color: white;
        text-decoration: none;
    }
    
    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-left: 10px;
    }
    
    .status-online {
        background: #10B981;
        color: white;
    }
    
    .status-offline {
        background: #EF4444;
        color: white;
    }
    
    .status-dev {
        background: #F59E0B;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 应用标题
st.markdown("""
<div class="header">
    <h1 style="margin:0;">🎮 游戏工具导航</h1>
    <p style="margin:5px 0 0 0; opacity:0.9;">一站式访问您的游戏工具</p>
</div>
""", unsafe_allow_html=True)

# 您的3个应用信息（请替换为您的实际链接）
apps = [
    {
        "name": "资源计算器",
        "url": "https://azbapcbtjvkpq8esq5q8f2.streamlit.app/",  # 替换为您的实际链接
        "description": "计算包裹内资源数量",
        "icon": "📊",
        "status": "online"  # online, offline, dev
    },
    {
        "name": "神兵玉石材料消耗计算",  # 第二个应用的名字
        "url": "https://eu5fctgjsakgp8strse8ku.streamlit.app/",  # 替换为您的实际链接
        "description": "计算神兵玉石升级消耗以及活动积分兑换是否充足",
        "icon": "⚔️",
        "status": "online"
    },
    {
        "name": "活动兑换神兵玉石自动推荐",  # 第三个应用的名字
        "url": "https://cenpecvplwojqgxvtn5y5n.streamlit.app/",  # 替换为您的实际链接
        "description": "智能推荐如何使用活动积分兑换神兵玉石材料",
        "icon": "📅",
        "status": "online"
    }
]

# 显示应用卡片
st.markdown("### 🚀 可用工具")
st.markdown("点击下方工具卡片在新标签页中打开应用")

for i, app in enumerate(apps):
    # 状态标签
    if app["status"] == "online":
        status_badge = '<span class="status-badge status-online">在线</span>'
    elif app["status"] == "dev":
        status_badge = '<span class="status-badge status-dev">开发中</span>'
    else:
        status_badge = '<span class="status-badge status-offline">离线</span>'
    
    # 创建卡片HTML
    card_html = f"""
    <div class="app-card">
        <div class="app-title">
            {app["icon"]} {app["name"]}
            {status_badge}
        </div>
        <div class="app-description">
            {app["description"]}
        </div>
        <a href="{app["url"]}" target="_blank" class="app-link">
            打开应用 →
        </a>
    </div>
    """
    
    # 渲染卡片
    html(card_html, height=150)

# 使用说明
st.markdown("---")
st.markdown("### 📖 使用说明")
st.info("""
1. 点击上方卡片中的"打开应用"按钮
2. 应用将在新标签页中打开
3. 每个应用都可以独立使用
4. 返回此页面可切换到其他工具
""")

# 快速链接（可选）
st.markdown("---")
st.markdown("### ⚡ 快速访问")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(f"{apps[0]['icon']} {apps[0]['name']}", use_container_width=True):
        webbrowser.open_new_tab(apps[0]["url"])
with col2:
    if st.button(f"{apps[1]['icon']} {apps[1]['name']}", use_container_width=True):
        webbrowser.open_new_tab(apps[1]["url"])
with col3:
    if st.button(f"{apps[2]['icon']} {apps[2]['name']}", use_container_width=True):
        webbrowser.open_new_tab(apps[2]["url"])

# 应用介绍（折叠部分）
st.markdown("---")
st.markdown("### ℹ️ 应用详细介绍")

with st.expander("📊 资源计算器"):
    st.markdown("""
    **主要功能：**
    - 计算游戏资源的4:4:2:1比例
    - 优化资源包使用策略
    - 显示大数值资源（支持亿级别）
    - 分析资源过剩情况
    
    **使用场景：**
    - 资源分配规划
    - 资源包使用优化
    - 长期资源储备计划
    """)
    
    # 显示示例图片或描述
    st.image("https://via.placeholder.com/600x200/667eea/ffffff?text=资源计算器界面示例", 
             caption="资源计算器界面示意图", use_column_width=True)

with st.expander("⚔️ 战力分析器"):
    st.markdown("""
    **主要功能：**
    - 分析角色综合战力
    - 装备搭配建议
    - 战力对比分析
    - 提升方案推荐
    
    **使用场景：**
    - 角色战力评估
    - 装备优化选择
    - 战力提升规划
    """)

with st.expander("📅 活动规划器"):
    st.markdown("""
    **主要功能：**
    - 游戏活动时间规划
    - 资源投入计算
    - 收益最大化分析
    - 提醒功能
    
    **使用场景：**
    - 活动参与规划
    - 时间管理优化
    - 资源投入决策
    """)

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9em;">
    <p>游戏工具导航 v1.0 | 最后更新: 2024年1月</p>
    <p>❤️ 为游戏玩家提供便利的工具集合</p>
</div>
""", unsafe_allow_html=True)
