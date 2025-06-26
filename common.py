'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2025-06-25 21:29:40
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2025-06-26 10:05:15
FilePath: \实训\common.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
def get_llm_response(client, model, user_prompt, memory=None, stream=False):
    """
    通用大模型回复函数，支持流式和非流式调用。
    :param client: OpenAI 客户端实例
    :param model: 模型名称
    :param user_prompt: 用户输入
    :param memory: 对话历史（messages 格式）
    :param stream: 是否流式返回
    :return: 回复内容或生成器
    """
    messages = memory if memory else []
    messages.append({'role': 'user', 'content': user_prompt})
    if stream:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        def stream_generator():
            for chunk in response:
                delta = getattr(chunk.choices[0].delta, 'content', None)
                if delta:
                    yield delta
        return stream_generator()
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content.strip()