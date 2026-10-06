# langchain_ollama
from langchain_ollama import OllamaLLM

model = OllamaLLM(model="qwen3:8b")

res = model.invoke(input="你是谁呀能做什么？有那些技能")

print(res)
