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
        {"role": "user", "content": "输出1-10的所有奇数"},
    ],
    stream=True # 开启流式输出
)
# 3.输出结果
for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(
            content,
            end="",
            flush=True  # 立刻刷新缓存区
        )