import streamlit as st
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
        margin-bottom: 30px;
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
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 500;
        margin-left: 8px;
        vertical-align: middle;
    }
    
    .status-online {
        background: #10B981;
        color: white;
    }
    
    .status-online::before {
        content: "🟢";
        margin-right: 4px;
        font-size: 0.6rem;
    }
    
    .status-dev {
        background: #F59E0B;
        color: white;
    }
    
    .status-dev::before {
        content: "🟡";
        margin-right: 4px;
        font-size: 0.6rem;
    }
</style>
""", unsafe_allow_html=True)

# 应用标题
st.markdown("""
<div class="header">
    <h1 style="margin:0;">🎮 游戏工具导航</h1>
</div>
""", unsafe_allow_html=True)

# 您的3个应用信息（请替换为您的实际链接）
apps = [
    {
        "name": "资源计算器",
        "url": "https://your-resource-calculator.streamlit.app",  # 替换为您的实际链接
        "description": "智能计算游戏资源分配，优化资源包使用策略",
        "icon": "📊",
        "status": "online"
    },
    {
        "name": "战力分析器",  # 第二个应用的名字
        "url": "https://your-second-app.streamlit.app",  # 替换为您的实际链接
        "description": "分析角色战力，提供装备搭配建议",
        "icon": "⚔️",
        "status": "online"
    },
    {
        "name": "活动规划器",  # 第三个应用的名字
        "url": "https://your-third-app.streamlit.app",  # 替换为您的实际链接
        "description": "规划游戏活动参与，计算最优时间安排",
        "icon": "📅",
        "status": "dev"
    }
]

# 显示应用卡片
for i, app in enumerate(apps):
    # 状态标签
    if app["status"] == "online":
        status_text = "在线"
        status_class = "status-online"
    else:
        status_text = "开发中"
        status_class = "status-dev"
    
    # 创建卡片HTML
    card_html = f"""
    <div class="app-card">
        <div class="app-title">
            {app["icon"]} {app["name"]}
            <span class="status-badge {status_class}">{status_text}</span>
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
