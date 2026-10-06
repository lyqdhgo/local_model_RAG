from langchain_ollama import OllamaEmbeddings
# 创建模型对象 不传model默认用的是 text-embeddings-v1
model = OllamaEmbeddings(model="qwen3-embedding:4b")

# 不用invoke stream
# embed_query、embed_documents
print('单次嵌入:', model.embed_query("我喜欢你")) # 单次
print('批量嵌入:', model.embed_documents(["我喜欢你", "我稀饭你", "晚上吃啥"])) # 批量
