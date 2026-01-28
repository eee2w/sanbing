import streamlit as st
from streamlit.components.v1 import html

# 设置页面配置
st.set_page_config(
    page_title="游戏工具导航",
    page_icon="🎮",
    layout="centered"
)

# 注入关键的JavaScript代码，用于复制链接和显示提示
copy_js = """
<script>
function copyToClipboard(url, appName) {
    // 创建临时输入框
    var tempInput = document.createElement("input");
    tempInput.value = url;
    document.body.appendChild(tempInput);
    
    // 选中并复制
    tempInput.select();
    tempInput.setSelectionRange(0, 99999); // 移动设备兼容
    document.execCommand("copy");
    
    // 移除临时元素
    document.body.removeChild(tempInput);
    
    // 显示复制成功的提示
    alert("✓ 已复制【" + appName + "】链接！\\n\\n请粘贴到手机浏览器中打开。");
}
</script>
"""

st.markdown(copy_js, unsafe_allow_html=True)

# 自定义CSS样式 - 恢复链接样式并添加复制按钮样式
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
        margin-bottom: 5px;
    }
    
    .app-description {
        font-size: 0.95rem;
        color: #666;
        margin-bottom: 20px;
        line-height: 1.5;
    }
    
    .link-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        margin-top: 10px;
    }
    
    /* 恢复原始链接样式 - 蓝色带下划线 */
    .original-link {
        color: #0066cc !important;
        text-decoration: underline !important;
        font-size: 0.9rem;
        word-break: break-all;
        flex-grow: 1;
        padding: 5px 0;
        cursor: pointer;
    }
    
    .original-link:hover {
        color: #004499 !important;
        text-decoration: underline !important;
    }
    
    /* 复制按钮样式 */
    .copy-btn {
        background: #10B981;
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 5px;
        font-size: 0.85rem;
        font-weight: 500;
        cursor: pointer;
        white-space: nowrap;
        transition: background 0.2s;
    }
    
    .copy-btn:hover {
        background: #0da271;
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
    
    .feedback-note {
        text-align: center;
        margin-top: 40px;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 10px;
        font-size: 0.9rem;
        color: #666;
        border-left: 4px solid #667eea;
        line-height: 1.6;
    }
    
    .wechat-tip {
        color: #d9534f;
        font-weight: bold;
        margin-top: 5px;
    }
    
    /* 操作指引样式 */
    .instructions {
        background-color: #e8f4fd;
        border-radius: 8px;
        padding: 12px 15px;
        margin: 25px 0;
        border-left: 4px solid #2196F3;
    }
</style>
""", unsafe_allow_html=True)

# 应用标题
st.markdown("""
<div class="header">
    <h1 style="margin:0;">🎮 游戏工具导航</h1>
</div>
""", unsafe_allow_html=True)

# 微信环境下的操作指引
st.markdown("""
<div class="instructions">
    <strong>📱 微信内访问指引：</strong><br>
    1. 点击下方<b>"复制链接"</b>按钮<br>
    2. 在弹出提示后，<b>打开手机浏览器</b>（如Safari/Chrome）<br>
    3. 在地址栏<b>粘贴链接</b>并访问
</div>
""", unsafe_allow_html=True)

# 您的应用信息列表
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
    # 状态标签
    status_text = "（可使用）" if app["status"] == "online" else "（开发中）"
    status_class = "status-online" if app["status"] == "online" else "status-dev"
    
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
        
        <div class="link-container">
            <!-- 显示链接文本（恢复蓝色下划线样式） -->
            <div class="original-link" onclick="copyToClipboard('{app["url"]}', '{app["name"]}')">
                {app["url"]}
            </div>
            
            <!-- 复制链接按钮 -->
            <button class="copy-btn" onclick="copyToClipboard('{app["url"]}', '{app["name"]}')">
                复制链接
            </button>
        </div>
    </div>
    """
    # 渲染卡片
    html(card_html)

# 添加管理员反馈提示
st.markdown("""
<div class="feedback-note">
    <strong>💡 提示：</strong> 遇到问题或需要功能改进，请找管理员反馈<br>
    <span class="wechat-tip">⚠️ 微信限制：部分微信版本无法直接打开外部链接，请使用上方"复制链接"功能。</span>
</div>
""", unsafe_allow_html=True)
