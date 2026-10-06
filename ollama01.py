from openai import OpenAI

client = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1",
)
completion = client.chat.completions.create(
    model="qwen3:8b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁，什么模型，能做什么？"},
    ],
    stream=True
)
for chunk in completion:
    content = chunk.choices[0].delta.content
    if content is not None:
        print(content, end="", flush=True)