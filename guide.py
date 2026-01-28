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
        margin-bottom: 20px;
    }
    
    .app-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .app-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
    }
    
    .app-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 8px;
    }
    
    .app-description {
        font-size: 0.95rem;
        color: #666;
        margin-bottom: 15px;
        line-height: 1.5;
    }
    
    /* 完整链接显示样式 */
    .full-url {
        background-color: #f5f5f5;
        border-radius: 6px;
        padding: 10px 12px;
        margin: 15px 0;
        border: 1px solid #e0e0e0;
        word-break: break-all;
        font-size: 0.85rem;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        color: #333;
        user-select: text;
        -webkit-user-select: text;
        line-height: 1.4;
    }
    
    .url-hint {
        font-size: 0.8rem;
        color: #888;
        text-align: center;
        margin: 5px 0 10px 0;
        font-style: normal;
    }
    
    .app-link {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        text-align: center;
        width: 100%;
        border: none;
        cursor: pointer;
        margin-top: 5px;
    }
    
    .app-link:hover {
        background: #764ba2;
        color: white;
        text-decoration: none;
        transform: translateY(-1px);
    }
    
    .status-badge {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 500;
        margin-left: 8px;
        color: #666;
        vertical-align: middle;
    }
    
    .status-online {
        color: #10B981;
    }
    
    .status-dev {
        color: #F59E0B;
    }
    
    .wechat-tip {
        text-align: center;
        margin: 20px 0;
        padding: 12px;
        background-color: #fff8e1;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #333;
        border-left: 4px solid #ffc107;
        line-height: 1.6;
    }
    
    .footer-tip {
        text-align: center;
        margin-top: 30px;
        padding: 10px;
        font-size: 0.85rem;
        color: #666;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# 应用标题
st.markdown("""
<div class="header">
    <h1 style="margin:0;">🎮 游戏工具导航</h1>
</div>
""", unsafe_allow_html=True)

# 微信环境提示
st.markdown("""
<div class="wechat-tip">
    <strong>📱 微信内访问指引：</strong><br>
    1. 尝试点击下方"打开应用"按钮直接跳转<br>
    2. 如果无法跳转，<strong>长按下方链接</strong>选择"复制"<br>
    3. 粘贴到手机浏览器中打开
</div>
""", unsafe_allow_html=True)

# 应用信息
apps = [
    {
        "name": "资源计算器",
        "url": "https://azbapcbtjvkpq8esq5q8f2.streamlit.app/",
        "description": "计算包裹内资源总量",
        "icon": "📊",
        "status": "online"
    },
    {
        "name": "神兵玉石消耗计算",
        "url": "https://eu5fctgjsakgp8strse8ku.streamlit.app/",
        "description": "计算神兵玉石升级消耗以及活动积分兑换是否充足",
        "icon": "⚔️",
        "status": "online"
    },
    {
        "name": "积分兑换神兵玉石材料自动推荐",
        "url": "https://cenpecvplwojqgxvtn5y5n.streamlit.app/",
        "description": "智能推荐活动积分如何兑换神兵玉石材料",
        "icon": "📅",
        "status": "online"
    }
]

# 显示应用卡片
for app in apps:
    status_text = "（可使用）" if app["status"] == "online" else "（开发中）"
    status_class = "status-online" if app["status"] == "online" else "status-dev"
    
    card_html = f"""
    <div class="app-card">
        <div class="app-title">
            {app["icon"]} {app["name"]}
            <span class="status-badge {status_class}">{status_text}</span>
        </div>
        <div class="app-description">
            {app["description"]}
        </div>
        
        <!-- 完整链接显示区域 -->
        <div class="full-url">
            {app["url"]}
        </div>
        <div class="url-hint">
            长按上方链接可复制
        </div>
        
        <!-- 打开应用按钮 -->
        <a href="{app["url"]}" target="_blank" class="app-link">
            打开应用 →
        </a>
    </div>
    """
    
    html(card_html)

# 页脚说明
st.markdown("""
<div class="footer-tip">
    <strong>使用提示：</strong>电脑浏览器可直接点击"打开应用"按钮<br>
    手机微信内建议使用"长按链接复制 → 浏览器粘贴访问"的方式
</div>
""", unsafe_allow_html=True)
