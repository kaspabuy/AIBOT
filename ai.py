import streamlit as st
import requests
import json

# 页面配置
st.set_page_config(
    page_title="千问AI助手",
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
    <h1>🤖 千问AI助手</h1>
    <p>您的智能对话伙伴</p>
</div>
""", unsafe_allow_html=True)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

# API调用函数
def call_qianwen_api(messages):
    """调用千问API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL_NAME,
        "input": {
            "messages": messages
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
                    🤖 {message["content"]}
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # 显示欢迎信息
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #666;">
        <h3>👋 欢迎使用千问AI助手！</h3>
        <p>我是您的智能对话伙伴，可以帮您解答问题、提供建议、进行创意讨论等。</p>
        <p style="margin-top: 2rem;">💭 <em>请在下方输入框中输入您想问的问题...</em></p>
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
            placeholder="请输入您的问题...",
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
    with st.spinner("🤖 AI正在思考中..."):
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
    <p>基于阿里通义千问 • Powered by Streamlit</p>
</div>
""", unsafe_allow_html=True)