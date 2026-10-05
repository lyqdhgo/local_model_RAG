import os

from openai import OpenAI

api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise RuntimeError("请先设置 DASHSCOPE_API_KEY 环境变量。")

# 1.获取client对象
client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
# 2.调用模型
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": "好的，我是编程专家，并且话不多，我要问什么？"},
        {"role": "user", "content": "输出1-100的所有奇数"},
    ]
)
# 3.输出结果
print(response.choices[0].message.content)