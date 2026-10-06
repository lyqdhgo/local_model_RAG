from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 得到模型对象，qwen3-max就是聊天模型
model = ChatOllama(model="qwen3:8b")

# 准备消息列表
messages = [
    SystemMessage(content="你是一个边塞诗人。"),
    HumanMessage(content="写一首唐诗"),
    AIMessage(content="好的，我来写一首边塞诗：\n\n《边塞行》\n\n烽火连三月，家书抵万金。\n百年征战地，风沙漫天心。\n将军策马去，戍边守国门。\n长城万里外，思乡泪满巾。"),
    HumanMessage(content="再写一首边塞诗")
]

# 调用stream流式执行
res = model.stream(input=messages)

# for循环迭代打印输出，通过.content来获取到内容
for chunk in res:
    print(chunk.content, end="", flush=True)
