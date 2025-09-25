import streamlit as st
import requests
import json
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="千问AI助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #4CAF50;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .assistant-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    
    .sidebar .stSelectbox > label {
        font-weight: bold;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #ff6b6b, #ee5a52);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 主标题
st.markdown("""
<div class="main-header">
    <h1>🤖 千问AI智能助手</h1>
    <p>基于阿里通义千问大模型的智能对话系统</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置设置")
    
    # API密钥输入
    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="请输入您的千问API密钥",
        help="请到阿里云控制台获取API密钥"
    )
    
    # 模型选择
    model_name = st.selectbox(
        "选择模型",
        options=[
            "qwen-turbo",
            "qwen-plus",
            "qwen-max",
            "qwen-max-longcontext"
        ],
        index=0,
        help="不同模型有不同的性能和价格"
    )
    
    # 参数调整
    st.subheader("🎛️ 生成参数")
    
    temperature = st.slider(
        "Temperature (创造性)",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="较高的值会让回答更有创意，较低的值会更准确"
    )
    
    max_tokens = st.slider(
        "最大输出长度",
        min_value=100,
        max_value=2000,
        value=1000,
        step=100,
        help="控制AI回答的最大长度"
    )
    
    top_p = st.slider(
        "Top P (多样性)",
        min_value=0.1,
        max_value=1.0,
        value=0.8,
        step=0.1,
        help="控制输出的多样性"
    )
    
    # 清除对话按钮
    if st.button("🗑️ 清除对话历史"):
        st.session_state.messages = []
        st.rerun()

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# API调用函数
def call_qianwen_api(messages, api_key, model, temperature, max_tokens, top_p):
    """调用千问API"""
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "input": {
            "messages": messages
        },
        "parameters": {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "result_format": "message"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API调用失败: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"JSON解析失败: {str(e)}")
        return None

# 显示统计信息
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-container">
        <h3>{len(st.session_state.messages)}</h3>
        <p>对话消息数</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-container">
        <h3>{model_name}</h3>
        <p>当前模型</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-container">
        <h3>{st.session_state.total_tokens}</h3>
        <p>总Token使用</p>
    </div>
    """, unsafe_allow_html=True)

# 显示对话历史
st.subheader("💬 对话历史")

chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 您:</strong><br>
                {content}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 千问:</strong><br>
                {content}
            </div>
            """, unsafe_allow_html=True)

# 用户输入区域
st.subheader("✍️ 发送消息")

user_input = st.text_area(
    "请输入您的问题:",
    height=100,
    placeholder="请输入您想要咨询的问题...",
    key="user_input"
)

# 发送按钮
col1, col2 = st.columns([1, 4])

with col1:
    send_button = st.button("🚀 发送", type="primary")

with col2:
    if not api_key:
        st.warning("⚠️ 请先在侧边栏输入API密钥")

# 处理发送逻辑
if send_button and user_input.strip():
    if not api_key:
        st.error("❌ 请先输入API密钥！")
    else:
        # 添加用户消息到历史
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input.strip()
        })
        
        # 显示加载状态
        with st.spinner("🤖 千问正在思考中..."):
            # 调用API
            response = call_qianwen_api(
                st.session_state.messages,
                api_key,
                model_name,
                temperature,
                max_tokens,
                top_p
            )
            
            if response and response.get("output"):
                # 获取AI回复
                ai_message = response["output"]["choices"][0]["message"]["content"]
                
                # 添加AI回复到历史
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_message
                })
                
                # 更新token统计
                usage = response.get("usage", {})
                if usage:
                    st.session_state.total_tokens += usage.get("total_tokens", 0)
                
                # 清空输入框
                st.session_state.user_input = ""
                
                # 重新运行以显示新消息
                st.rerun()
            else:
                st.error("❌ API调用失败，请检查您的API密钥和网络连接")

# 底部信息
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>💡 <strong>使用提示:</strong></p>
    <ul style="list-style: none; padding: 0;">
        <li>• 确保您的API密钥有效且有足够的配额</li>
        <li>• 可以通过侧边栏调整模型参数来获得不同效果</li>
        <li>• Temperature越高回答越有创意，越低越准确</li>
        <li>• 对话历史会保存在当前会话中</li>
    </ul>
    <br>
    <p><em>基于Streamlit构建 | Powered by 阿里通义千问</em></p>
</div>
""", unsafe_allow_html=True)

# 运行说明（注释形式）
"""
运行说明:
1. 安装依赖: pip install streamlit requests
2. 保存此文件为 app.py
3. 运行命令: streamlit run app.py
4. 在浏览器中打开 http://localhost:8501

环境变量方式（推荐）:
可以通过环境变量设置API密钥，避免在代码中硬编码:
export QIANWEN_API_KEY="your-api-key-here"

然后在代码中使用:
import os
api_key = os.getenv('QIANWEN_API_KEY', '')
"""