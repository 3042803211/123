import requests
import json

DEEPSEEK_API_KEY = 'sk-b21b39b276404629973750bd8e09f890' # 请替换为您自己的DeepSeek API Key
API_URL = 'https://api.deepseek.com/chat/completions'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
}

def chat_with_deepseek():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    print("开始与 DeepSeek 对话 (输入 '退出', 'exit' 或 'quit' 来结束对话):")

    while True:
        user_input = input("你: ")
        if user_input.lower() in ['退出', 'exit', 'quit']:
            print("对话结束。")
            break

        messages.append({"role": "user", "content": user_input})

        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.7,
            "stream": False
        }

        print("正在向 DeepSeek API 发送请求...")

        try:
            resp = requests.post(url=API_URL, headers=headers, data=json.dumps(payload), timeout=30)
            resp.raise_for_status()
            response_data = resp.json()

            if response_data.get('choices') and len(response_data['choices']) > 0:
                assistant_message = response_data['choices'][0].get('message', {})
                assistant_content = assistant_message.get('content')
                if assistant_content:
                    print(f"DeepSeek: {assistant_content}")
                    messages.append({"role": "assistant", "content": assistant_content})
                else:
                    print("未能从API响应中提取到消息内容。")
                    print("完整响应:", json.dumps(response_data, indent=2, ensure_ascii=False))
                    # 如果没有有效回复，从历史记录中移除最后的用户消息，以便用户可以重试
                    if messages and messages[-1]["role"] == "user":
                        messages.pop()
            else:
                print("API响应中未找到 'choices' 或 'choices' 为空。")
                print("完整响应:", json.dumps(response_data, indent=2, ensure_ascii=False))
                if messages and messages[-1]["role"] == "user":
                    messages.pop()

        except requests.exceptions.Timeout:
            print("请求超时：无法连接到 DeepSeek API 服务。请稍后重试。")
            if messages and messages[-1]["role"] == "user":
                messages.pop()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP错误：{http_err} - 状态码：{resp.status_code}")
            try:
                error_details = resp.json()
                print("错误详情:", json.dumps(error_details, indent=2, ensure_ascii=False))
            except requests.exceptions.JSONDecodeError:
                print("错误详情 (非JSON格式):", resp.text)
            if messages and messages[-1]["role"] == "user":
                messages.pop()
        except requests.exceptions.RequestException as req_err:
            print(f"网络请求错误：{req_err}。请检查您的网络连接。")
            if messages and messages[-1]["role"] == "user":
                messages.pop()
        except requests.exceptions.JSONDecodeError:
            print("无法解析API响应为JSON格式。")
            if 'resp' in locals() and hasattr(resp, 'text'):
                print("原始响应文本:", resp.text)
            if messages and messages[-1]["role"] == "user":
                messages.pop()
        except Exception as e:
            print(f"处理过程中发生未知错误: {e}")
            if messages and messages[-1]["role"] == "user":
                messages.pop()

if __name__ == "__main__":
    chat_with_deepseek()