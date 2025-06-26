import json
from dotenv import load_dotenv
import openai
import os

PROMPT_TEMPLATE = """你是一位数据分析助手，你的回应内容取决于用户的请求内容，请按照下面的步骤处理用户请求：
1. 思考阶段 (Thought) ：先分析用户请求类型（文字回答/表格/图表），并验证数据类型是否匹配。
2. 行动阶段 (Action) ：根据分析结果选择以下严格对应的格式。
   - 纯文字回答:
     {"answer": "不超过50个字符的明确答案"}

   - 表格数据：
     {"table":{"columns":["列名1", "列名2", ...], "data":[["第一行值1", "值2", ...], ["第二行值1", "值2", ...]]}}

   - 柱状图
     {"bar":{"columns": ["A", "B", "C", ...], "data":[35, 42, 29, ...]}}

   - 折线图
     {"line":{"columns": ["A", "B", "C", ...], "data": [35, 42, 29, ...]}}
     
3. 格式校验要求
   - 字符串值必须使用英文双引号
   - 数值类型不得添加引号
   - 确保数组闭合无遗漏
   错误案例：{'columns':['Product', 'Sales'], data:[[A001, 200]]}
   正确案例：{"columns":["product", "sales"], "data":[["A001", 200]]}

注意：响应数据的"output"中不要有换行符、制表符以及其他格式符号。

当前用户请求如下：\n"""

def dataframe_agent(df, query):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=api_key, base_url="https://api.openai-hk.com/v1")
    prompt = PROMPT_TEMPLATE + query
    messages = [
        {"role": "system", "content": "你是一位数据分析助手。"},
        {"role": "user", "content": prompt}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            max_tokens=8192
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as err:
        print(err)
        return {"answer": "暂时无法提供分析结果，请稍后重试！"}
