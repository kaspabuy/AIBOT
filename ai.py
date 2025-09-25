import streamlit as st
import requests
import json

# 页面配置
st.set_page_config(
    page_title="Hapince - 企业出海专家级AI助手",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# API配置
API_KEY = "sk-66ad592305bc4407943b07398917d4c9"
MODEL_NAME = "qwen-turbo"
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# 自定义CSS样式
st.markdown("""
<style>
    .st-emotion-cache-zy6yx3 {
        width: 100%;
        padding: 0 1rem 10rem;
        max-width: initial;
        min-width: auto;
    }
    
    /* 全局样式重置 */
    .main .block-container {
        padding: 1rem 2rem;
        max-width: none;
    }
    
    /* 响应式容器 */
    .chat-app-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0;
    }
    
    /* 主标题样式 */
    .main-header {
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }
    
    .main-header h1 {
        font-size: clamp(1.8rem, 4vw, 3rem);
        font-weight: 700;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: clamp(1rem, 2vw, 1.2rem);
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* 聊天容器样式 */
    .chat-container {
        background: linear-gradient(145deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 2rem 0;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.8);
    }
    
    /* PC端聊天区域 */
    @media (min-width: 768px) {
        .chat-messages {
            max-height: 600px;
            overflow-y: auto;
            padding: 1rem;
        }
        
        .chat-input-section {
            position: sticky;
            bottom: 0;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 20px;
            margin-top: 1rem;
            box-shadow: 0 -5px 20px rgba(0,0,0,0.1);
        }
    }
    
    /* 移动端适配 */
    @media (max-width: 767px) {
        .main .block-container {
            padding: 0.5rem 1rem;
        }
        
        .chat-messages {
            max-height: 400px;
            overflow-y: auto;
            padding: 0.5rem;
        }
        
        .chat-input-section {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 1rem;
            box-shadow: 0 -5px 20px rgba(0,0,0,0.15);
            z-index: 999;
        }
        
        .main-header {
            margin-bottom: 1rem;
            padding: 1.5rem 1rem;
        }
        
        body {
            padding-bottom: 120px;
        }
    }
    
    /* 消息气泡样式 */
    .user-message {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 25px 25px 8px 25px;
        margin: 1rem 0 1rem auto;
        word-wrap: break-word;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
        font-size: 1rem;
        line-height: 1.5;
        position: relative;
        animation: slideInRight 0.3s ease-out;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        color: #1e293b;
        padding: 1rem 1.5rem;
        border-radius: 25px 25px 25px 8px;
        margin: 1rem auto 1rem 0;
        word-wrap: break-word;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(148, 163, 184, 0.2);
        font-size: 1rem;
        line-height: 1.5;
        position: relative;
        animation: slideInLeft 0.3s ease-out;
    }
    
    /* 动画效果 */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* 输入区域样式 */
    .input-row {
        display: flex;
        gap: 1rem;
        align-items: flex-end;
        width: 100%;
    }
    
    .input-area {
        flex: 1;
        min-width: 0;
    }
    
    .send-button {
        flex-shrink: 0;
        width: 120px;
    }
    
    .stTextArea textarea {
        border-radius: 20px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 1rem 1.5rem !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
        resize: none !important;
        transition: all 0.3s ease !important;
        background: rgba(255, 255, 255, 0.9) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        background: white !important;
    }
    
    /* 发送按钮样式 */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3) !important;
        height: 60px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
        background: linear-gradient(135deg, #4338ca, #6d28d9) !important;
    }
    
    /* 欢迎页面样式 */
    .welcome-section {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin: 2rem 0;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .service-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
        text-align: left;
    }
    
    .service-card {
        background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .service-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* 清除按钮样式 */
    .clear-button button {
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 0.5rem 1.5rem !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .clear-button button:hover {
        background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
        transform: translateY(-2px) !important;
    }
    
    /* 滚动条美化 */
    .chat-messages::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: rgba(148, 163, 184, 0.1);
        border-radius: 4px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #94a3b8, #64748b);
        border-radius: 4px;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    
    /* 响应式字体 */
    @media (max-width: 480px) {
        .user-message, .ai-message {
            max-width: 90%;
            font-size: 0.9rem;
            padding: 0.8rem 1.2rem;
        }
        
        .service-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .welcome-section {
            padding: 2rem 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# 主容器
with st.container():
    st.markdown('<div class="chat-app-container">', unsafe_allow_html=True)
    
    # 主标题
    st.markdown("""
    <div class="main-header">
        <h1>🌍 Hapince - 企业出海专家级AI助手</h1>
        <p>专业的企业出海服务解决方案，助力中国企业走向世界</p>
    </div>
    """, unsafe_allow_html=True)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

# 系统提示词设置
SYSTEM_PROMPT = """你的名字是Hapince，你是一名专业的企业出海服务专家。

你的专业领域包括：
- 海外市场分析与拓展策略
- 跨境贸易与合规指导
- 国际业务流程优化
- 海外投资与并购咨询
- 跨文化商务沟通
- 国际税务与法律法规
- 数字化出海解决方案
- 供应链全球化管理

请遵循以下原则为企业提供专业的出海服务：
1. 提供准确、实用的出海建议和解决方案
2. 结合具体案例和市场数据支持观点
3. 考虑不同国家和地区的法规差异
4. 保持专业、友善的咨询顾问语调
5. 针对企业实际情况提供定制化建议
6. 适当使用专业术语但确保客户理解
7. 主动询问企业具体需求以提供精准服务

作为Hapince，你致力于帮助中国企业成功走向国际市场，实现全球化发展目标。"""

# API调用函数
def call_qianwen_api(messages):
    """调用千问API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 在消息前添加系统提示
    system_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    
    data = {
        "model": MODEL_NAME,
        "input": {
            "messages": system_messages
        },
        "parameters": {
            "temperature": 0.7,
            "max_tokens": 1500,
            "top_p": 0.8,
            "result_format": "message"
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"请求失败: {str(e)}")
        return None

# 显示对话历史
if st.session_state.messages:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
                <div class="user-message">
                    {message["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="ai-message">
                    🌍 <strong>Hapince:</strong> {message["content"]}
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # 显示欢迎信息
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #666;">
        <h3>👋 您好！我是Hapince</h3>
        <p>我是一名专业的企业出海服务专家，拥有丰富的国际化业务经验。</p>
        <p style="margin: 1.5rem 0;">我可以为您的企业提供：</p>
        <div style="text-align: left; max-width: 500px; margin: 0 auto;">
            <p>🌐 <strong>海外市场分析</strong> - 目标市场调研与进入策略</p>
            <p>📋 <strong>合规指导</strong> - 国际法规与税务咨询</p>
            <p>🤝 <strong>商务拓展</strong> - 跨文化沟通与合作伙伴对接</p>
            <p>💼 <strong>投资咨询</strong> - 海外投资与并购建议</p>
            <p>🔗 <strong>供应链优化</strong> - 全球化运营管理</p>
        </div>
        <p style="margin-top: 2rem;">💭 <em>请告诉我您企业出海的具体需求，我将为您提供专业的解决方案...</em></p>
    </div>
    """, unsafe_allow_html=True)

# 用户输入区域
st.markdown('<div class="input-container">', unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_area(
            "",
            height=80,
            placeholder="请输入您的企业出海相关问题...",
            key="user_input_text",
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("")  # 添加一些空白以对齐按钮
        send_button = st.form_submit_button("💬 发送")

st.markdown('</div>', unsafe_allow_html=True)

# 处理发送逻辑
if send_button and user_input and user_input.strip():
    # 添加用户消息
    st.session_state.messages.append({
        "role": "user",
        "content": user_input.strip()
    })
    
    # 显示思考状态
    with st.spinner("🌍 Hapince正在为您分析企业出海方案..."):
        # 调用API
        response = call_qianwen_api(st.session_state.messages)
        
        if response and response.get("output"):
            # 获取AI回复
            ai_message = response["output"]["choices"][0]["message"]["content"]
            
            # 添加AI回复
            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_message
            })
            
            # 刷新页面显示新消息
            st.rerun()
        else:
            st.error("❌ AI暂时无法回复，请稍后重试")

# 底部清除按钮
if st.session_state.messages:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🗑️ 清除对话历史", key="clear_chat"):
            st.session_state.messages = []
            st.rerun()

# 页面底部信息
st.markdown("""
<div style="text-align: center; color: #999; padding: 2rem 0; font-size: 14px;">
    <p>🌍 Hapince - 专业企业出海服务 • Powered by 阿里通义千问</p>
</div>
""", unsafe_allow_html=True)