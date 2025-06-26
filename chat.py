import json
import streamlit as st
from openai import OpenAI
# 假设 common.py 已存在 get_llm_response 方法，否则需补充
from common import get_llm_response

def get_answer(question: str, api_vendor, base_url, api_key, model_name):
    try:
        client = OpenAI(base_url=base_url, api_key=api_key)
        memory = []
        for role, content in st.session_state['messages']:
            if role == 'human':
                memory.append({'role': 'user', 'content': content})
            else:
                memory.append({'role': 'assistant', 'content': content})
        if api_vendor == 'DeepSeek':
            return get_llm_response(client, model=model_name, user_prompt=question, memory=memory, stream=True)
        else:
            return get_llm_response(client, model=model_name, user_prompt=question, memory=memory)
    except Exception as e:
        return f'小🐖暂时无法提供回复，错误信息：{e}'

st.set_page_config(page_title="小🐖聊天机器人", page_icon="🤖", layout="wide")

# 设置页面样式
st.markdown("""
<style>
    /* 整体背景 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* 侧边栏样式 */
    .css-1d391kg, .css-1p05t8e {
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* 聊天消息样式 */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* 用户消息样式 */
    .stChatMessage.user {
        background: linear-gradient(135deg, #007AFF 0%, #5B5BFF 100%);
        color: white;
    }
    
    /* AI消息样式 */
    .stChatMessage.assistant {
        background: linear-gradient(135deg, #E8E8E8 0%, #FFFFFF 100%);
    }
    
    /* 输入框样式 */
    .stChatInput {
        border-radius: 20px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        padding: 10px 20px;
        background: rgba(255, 255, 255, 0.9);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* 按钮样式 */
    .stButton>button {
        border-radius: 20px;
        padding: 10px 25px;
        background: linear-gradient(135deg, #007AFF 0%, #5B5BFF 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* 标题样式 */
    h2 {
        color: #2C3E50;
        font-weight: 600;
        text-align: center;
        margin: 20px 0;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    api_vendor = st.radio(label='请选择服务提供商: ', options=['OpenAI', 'DeepSeek'])
    if api_vendor == 'OpenAI':
        base_url = 'https://twapi.openai-hk.com/v1/'
        model_options = ['gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-4o', 'gpt-4.1-mini', 'gpt-4.1']
    elif api_vendor == 'DeepSeek':
        base_url = 'https://api.deepseek.com'
        model_options = ['deepseek-chat', 'deep-reasoner']
    else:
        base_url = ''
        model_options = []
    model_name = st.selectbox(label='请选择要使用的模型: ', options=model_options)
    api_key = st.text_input(label='请输入你的key', type='password')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [('ai', '你好，我是你的AI助手，我叫小🐖。')]

st.write('## 小🐖聊天机器人')

for role, content in st.session_state['messages']:
    st.chat_message(role).write(content)

user_input = st.chat_input(placeholder='请输入')
if user_input:
    st.session_state['messages'].append(('human', user_input))
    st.chat_message('human').write(user_input)
    with st.spinner('小🐖正在思考，请耐心等待……'):
        if api_vendor == 'DeepSeek':
            stream = get_answer(user_input, api_vendor, base_url, api_key, model_name)
            st.session_state['messages'].append(('ai', ''))
            msg = st.chat_message('ai')
            text = ''
            for chunk in st.write_stream(stream):
                text += chunk
            st.session_state['messages'][-1] = ('ai', text)
        else:
            answer = get_answer(user_input, api_vendor, base_url, api_key, model_name)
            st.session_state['messages'].append(('ai', answer))
            st.chat_message('ai').write(answer)