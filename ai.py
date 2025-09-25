import streamlit as st
import requests
import json

# 页面配置
st.set_page_config(
    page_title="Hapince出海AI助手",
    page_icon="🤖",
    layout="centered"
)

# API配置
API_KEY = "sk-66ad592305bc4407943b07398917d4c9"
MODEL_NAME = "qwen-turbo"
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 5px 18px;
        margin: 8px 0 8px auto;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 0 2px 10px rgba(0,123,255,0.3);
    }
    
    .ai-message {
        background: white;
        color: #333;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 5px;
        margin: 8px auto 8px 0;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
    }
    
    .input-container {
        position: sticky;
        bottom: 0;
        background: white;
        padding: 1rem 0;
        border-top: 1px solid #e9ecef;
    }
    
    .stTextArea textarea {
        border-radius: 15px !important;
        border: 2px solid #dee2e6 !important;
        padding: 12px 16px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #007bff !important;
        box-shadow: 0 0 0 0.2rem rgba(0,123,255,0.25) !important;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #007bff, #0056b3);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,123,255,0.4);
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# 主标题
st.markdown("""
<div class="main-header">
    <h1>🌍 Hapince - 企业出海专家级AI助手</h1>
    <p>专业的企业出海服务解决方案</p>
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