<div align="center">

# local_model_RAG

**学习 LangChain / 本地大模型（Ollama）/ OpenAI 接口时写下的一堆练习脚本**

一堆平铺在根目录、每个都能单独 `python xxx.py` 跑一遍的入门 demo —— 不是框架，不是生产项目。

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-langchain--core%20%7C%20community%20%7C%20ollama-1C3C3C?logo=langchain&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-qwen3%3A8b-000000?logo=ollama&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI%20SDK-compatible-412991?logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-3DA639)

[这个仓库是什么](#这个仓库是什么) · [学习地图](#学习地图) · [环境准备](#环境准备) · [怎么跑](#怎么跑) · [目录速查](#目录速查) · [已知问题](#已知问题与注意事项)

</div>

---

## 这个仓库是什么

这是**个人学习笔记式的练习脚本集合**。

作者在学 LangChain、本地大模型（Ollama）、以及 OpenAI 风格接口的过程中，把每个知识点单独写成一个 `.py` 文件丢在根目录：一个脚本只演示一件事，很多脚本之间是"同一段代码换个模型后端 / 换个调用方式"的对照版本（比如 `langchainMessage.py` 和 `langchainOllamaMessage.py`、`openai02.py` 和 `openaiStream.py`）。

所以请把它当成**可以逐个复制去跑的示例集**，而不是一个项目：

- ❌ 没有包结构，没有 `__init__.py`，全部是扁平脚本
- ❌ 没有 `requirements.txt` / `pyproject.toml`，依赖靠手动装
- ❌ 没有测试、没有异常处理、没有日志，多数脚本就是把结果 `print` 出来
- ❌ 部分脚本是半成品或有笔误（见 [已知问题](#已知问题与注意事项)）
- ✅ 但每个脚本都足够短，适合当"某个 API 到底怎么写"的速查

---

## 学习地图

### 一、Prompt 工程（模板 / Few-shot）

| 脚本 | 演示内容 |
| --- | --- |
| [langchainPromptTemplate.py](langchainPromptTemplate.py) | 最小 `PromptTemplate`：`from_template` + `.format()` 注入变量，再把字符串交给 `Tongyi(model="qwen-max")` |
| [langchainPropTemplateChain.py](langchainPropTemplateChain.py) | 与上一个同一个模板，但改成 LCEL 链 `prompt_template \| model` 后 `chain.invoke({...})` |
| [langchainPromptFewshot.py](langchainPromptFewshot.py) | `FewShotPromptTemplate` 的 5 个核心参数（`example_prompt` / `examples` / `prefix` / `suffix` / `input_variables`），做"反义词"问答，`Tongyi(model="qwen-max")` |
| [langchainPromptCompre](langchainPromptCompre) | 只用 `PromptTemplate`，对比 `.format()` 返回 `str` 和 `.invoke()` 返回 `StringPromptValue`（**该文件没有 `.py` 后缀**，见已知问题） |
| [proptFewshot.py](proptFewshot.py) | 用原生 OpenAI SDK 手搓 few-shot：把示例以 `user`/`assistant` 消息对追加进 `messages`，做金融文本四分类，`qwen3-max` |
| [promptOptmize.py](promptOptmize.py) | 同样是手搓 few-shot，任务是判断两个句子是否匹配，示例按 `"是"` / `"不是"` 分组循环注入，`qwen3-max` |

### 二、消息与链（Message / Chain）

| 脚本 | 演示内容 |
| --- | --- |
| [chain.py](chain.py) | `ChatPromptTemplate.from_messages` 里的 `("system", ...)`、`MessagesPlaceholder("history")`、`("human", ...)` 三段式，然后 `chat_prompt_template \| model` 组成链后 `invoke({"history": ...})` |
| [ChatPromptTemplate.py](ChatPromptTemplate.py) | 同一套模板 + 同一份 `history_data`，但不组链：先 `.invoke().to_string()` 打印出拼好的整段文本，再把这段字符串喂给模型 |
| [langchainMessage.py](langchainMessage.py) | 显式构造 `SystemMessage` / `HumanMessage` / `AIMessage` 对象列表，用 `ChatTongyi(model="qwen3-max").stream()` 流式输出 |
| [langchainMessageSimple.py](langchainMessageSimple.py) | 同样的对话内容，消息改用 `("system" / "human" / "ai", str)` 元组简写，后端换成 `ChatOllama(model="qwen3:8b")` |
| [langchainOllamaMessage.py](langchainOllamaMessage.py) | Message 对象写法 + Ollama 后端，即 `langchainMessage.py` 的本地模型版本 |

### 三、模型接入（模型对象怎么创建）

| 脚本 | 演示内容 |
| --- | --- |
| [langchLLM.py](langchLLM.py) | `langchain_community.llms.tongyi.Tongyi`（LLM 类）最简 `invoke`，注释里解释了为什么用 `qwen-max` 而不是 `qwen3-max` |
| [langchainOllama.py](langchainOllama.py) | `langchain_ollama.OllamaLLM(model="qwen3:8b")` 最简 `invoke` |
| [openai02.py](openai02.py) | 原生 `openai.OpenAI` + DashScope 兼容模式 `base_url`，`qwen-plus`，`system`/`assistant`/`user` 三条消息，非流式 |
| [ollama01.py](ollama01.py) | 原生 OpenAI SDK 指向本地 `http://localhost:11434/v1`，`api_key="ollama"`（占位值），`qwen3:8b` 流式 |

### 四、流式输出（Streaming）

| 脚本 | 演示内容 |
| --- | --- |
| [langchainStream.py](langchainStream.py) | 纯 LLM 的 `model.stream()` 逐 chunk 打印；注释里保留了 `Tongyi(model="qwen-max")` 版本，实际执行的是 `OllamaLLM(model="qwen3:8b")` |
| [openaiStream.py](openaiStream.py) | `client.chat.completions.create(..., stream=True)` 后遍历 `chunk.choices[0].delta.content` |
| [openaiHistoryMessage.py](openaiHistoryMessage.py) | 多轮对话历史（小明 2 条狗 / 小红 3 只猫 → 一共几个宠物）+ `stream=True`，`qwen3-max` |

### 五、向量与相似度（Embedding / 余弦距离）

| 脚本 | 演示内容 |
| --- | --- |
| [langchainEmbedding.py](langchainEmbedding.py) | `DashScopeEmbeddings` 的两种用法：`embed_query()` 单条、`embed_documents()` 批量 |
| [langchainOllamaEmbedding.py](langchainOllamaEmbedding.py) | `OllamaEmbeddings(model="qwen3-embedding:4b")` 的 `embed_query()` / `embed_documents()` |
| [cosineDistance.py](cosineDistance.py) | 不依赖任何模型：手写 `get_dot()` 点积、`get_norm()` 模长、`cosine_similarity()`，对 A/B/C/D 四个二维向量两两算相似度，文件头有大段公式注释 |

### 六、结构化输出 / JSON

| 脚本 | 演示内容 |
| --- | --- |
| [json07.py](json07.py) | 纯标准库 `json`：`json.dumps(..., ensure_ascii=False)` 保证中文正常显示，`json.loads()` 反序列化成 dict / list |
| [jsonExtract.py](jsonExtract.py) | 信息抽取：用 few-shot（示例消息对）从股市句子中抽出 `日期 / 股票名称 / 开盘价 / 收盘价 / 成交量`，schema 用 list 变量声明，`qwen3-max`。文件里写了**两遍**几乎相同的流程（先用硬编码消息、再用 `examples_data` 循环拼），第二遍有 bug |

---

## 环境准备

### 1. Python 依赖

仓库里**没有依赖清单**，下面这份是根据各脚本真实 `import` 逆推出来的：

```bash
pip install langchain-core langchain-community langchain-ollama openai dashscope numpy
```

对应关系：

| 包 | 被哪些脚本用到 |
| --- | --- |
| `langchain-core` | `langchain_core.prompts`（`PromptTemplate` / `ChatPromptTemplate` / `FewShotPromptTemplate` / `MessagesPlaceholder`）、`langchain_core.messages`（`HumanMessage` / `AIMessage` / `SystemMessage`） |
| `langchain-community` | `ChatTongyi`、`Tongyi`、`DashScopeEmbeddings` |
| `dashscope` | `langchain-community` 里 Tongyi / DashScopeEmbeddings 这两个集成的底层 SDK，装 `langchain-community` 时建议一并显式装上 |
| `langchain-ollama` | `OllamaLLM`、`OllamaEmbeddings`、`ChatOllama` |
| `openai` | `openai02.py`、`openaiStream.py`、`openaiHistoryMessage.py`、`promptOptmize.py`、`proptFewshot.py`、`jsonExtract.py`、`ollama01.py` |
| `numpy` | `cosineDistance.py`（只在 `get_norm()` 里用了 `np.sqrt`） |

> 仓库没有声明 Python 版本，也没有锁定 LangChain 版本，所以**没有"官方推荐组合"**。按 LangChain 自身的版本要求，Python 3.9+ 比较稳妥。

### 2. 本地模型（Ollama）

代码里出现的 Ollama 模型名只有下面两个，按需拉取：

```bash
ollama pull qwen3:8b             # 对话/生成：langchainOllama.py、langchainStream.py、langchainMessageSimple.py、langchainOllamaMessage.py、ollama01.py
ollama pull qwen3-embedding:4b   # 向量：langchainOllamaEmbedding.py
```

Ollama 默认监听 `http://localhost:11434`，`ollama01.py` 里写的就是这个地址，脚本没改端口就不用动。

### 3. 云端模型（阿里云百炼 / DashScope）

用到 `ChatTongyi` / `Tongyi` / `DashScopeEmbeddings` / `OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")` 的脚本需要百炼 API Key。代码里出现的模型名：

- `qwen3-max` —— `chain.py`、`ChatPromptTemplate.py`、`langchainMessage.py`、`jsonExtract.py`、`openaiHistoryMessage.py`、`proptFewshot.py`、`promptOptmize.py`
- `qwen-max` —— `langchLLM.py`、`langchainPromptFewshot.py`、`langchainPromptTemplate.py`、`langchainPropTemplateChain.py`
- `qwen-plus` —— `openai02.py`、`openaiStream.py`

注意：`langchLLM.py` 的注释明确区分了这两类 —— **`qwen-max` 是 LLM 接口（`Tongyi`），`qwen3-max` 当聊天模型用（`ChatTongyi`）**。

---

## 怎么跑

所有脚本都是"根目录下的独立文件"，没有包结构，所以直接在仓库根目录跑就行：

```bash
python openai02.py
python langchainOllama.py
python cosineDistance.py
```

### 需要设置的环境变量

| 变量 | 谁需要 | 说明 |
| --- | --- | --- |
| `DASHSCOPE_API_KEY` | 见下 | 百炼（DashScope）API Key |

分两种情况：

1. **显式读取的脚本**（`os.getenv("DASHSCOPE_API_KEY")`，没设置会直接 `raise RuntimeError("请先设置 DASHSCOPE_API_KEY 环境变量。")`）：
   `openai02.py`、`openaiStream.py`、`openaiHistoryMessage.py`、`promptOptmize.py`、`proptFewshot.py`、`jsonExtract.py`

   ```powershell
   # PowerShell
   $env:DASHSCOPE_API_KEY = "你的百炼Key"
   ```
   ```bash
   # bash
   export DASHSCOPE_API_KEY="你的百炼Key"
   ```

2. **隐式读取的脚本**（用 `ChatTongyi` / `Tongyi` / `DashScopeEmbeddings`，脚本本身没写 key，由 LangChain 集成从环境变量取）：
   `chain.py`、`ChatPromptTemplate.py`、`langchainMessage.py`、`langchLLM.py`、`langchainPromptFewshot.py`、`langchainPromptTemplate.py`、`langchainPropTemplateChain.py`、`langchainEmbedding.py`
   —— 同样需要设置 `DASHSCOPE_API_KEY`，否则会在调用时报鉴权错误。

**不需要任何 Key 的脚本**：`ollama01.py`、`langchainOllama.py`、`langchainStream.py`、`langchainMessageSimple.py`、`langchainOllamaMessage.py`、`langchainOllamaEmbedding.py`、`cosineDistance.py`、`json07.py`（只用本地 Ollama / 纯标准库）。

> `.gitignore` 里已经忽略了 `.env` 和 `.env.*`，习惯用 `.env` 存 Key 的话不会被提交。

---

## 目录速查

| 文件 | 一句话 |
| --- | --- |
| [ChatPromptTemplate.py](ChatPromptTemplate.py) | `ChatPromptTemplate` + `MessagesPlaceholder` 拼多轮历史，`to_string()` 后再调 `ChatTongyi(qwen3-max)` |
| [chain.py](chain.py) | 同一套 Prompt 模板，改用 `prompt \| model` LCEL 链 `invoke` |
| [cosineDistance.py](cosineDistance.py) | 手写点积 / 模长 / 余弦相似度（`np.sqrt`），算 A-B、A-C、A-D |
| [json07.py](json07.py) | 标准库 `json` 的 `dumps(ensure_ascii=False)` / `loads` 中文示例 |
| [jsonExtract.py](jsonExtract.py) | OpenAI SDK + DashScope 兼容接口，few-shot 抽取股票行情字段（`qwen3-max`） |
| [langchLLM.py](langchLLM.py) | `langchain_community` 的 `Tongyi(qwen-max)` 最简 `invoke` |
| [langchainEmbedding.py](langchainEmbedding.py) | `DashScopeEmbeddings` 的 `embed_query` / `embed_documents` |
| [langchainMessage.py](langchainMessage.py) | `ChatTongyi` + Message 对象列表，`stream()` 流式打印 |
| [langchainMessageSimple.py](langchainMessageSimple.py) | 消息用元组简写 + `ChatOllama(qwen3:8b)` 流式 |
| [langchainOllama.py](langchainOllama.py) | `OllamaLLM(qwen3:8b)` 最简 `invoke` |
| [langchainOllamaEmbedding.py](langchainOllamaEmbedding.py) | `OllamaEmbeddings(qwen3-embedding:4b)` 单条 + 批量嵌入 |
| [langchainOllamaMessage.py](langchainOllamaMessage.py) | Message 对象写法 + `ChatOllama(qwen3:8b)` 流式 |
| [langchainPromptCompre](langchainPromptCompre) | 对比 `PromptTemplate.format()` 与 `.invoke()` 的返回值类型（**无 `.py` 后缀**） |
| [langchainPromptFewshot.py](langchainPromptFewshot.py) | `FewShotPromptTemplate` 五参数版反义词问答 + `Tongyi(qwen-max)` |
| [langchainPromptTemplate.py](langchainPromptTemplate.py) | `PromptTemplate.format()` 起名字 + `model.invoke(字符串)` |
| [langchainPropTemplateChain.py](langchainPropTemplateChain.py) | 同一个起名模板，改用 LCEL 链调用 |
| [langchainStream.py](langchainStream.py) | `OllamaLLM(qwen3:8b).stream()` 逐 chunk 打印（注释里留了 Tongyi 版本） |
| [ollama01.py](ollama01.py) | 原生 OpenAI SDK 指向 `localhost:11434/v1`，`qwen3:8b` 流式 |
| [openai02.py](openai02.py) | 原生 OpenAI SDK + DashScope，`qwen-plus`，非流式 |
| [openaiHistoryMessage.py](openaiHistoryMessage.py) | 多轮历史消息 + `stream=True`，`qwen3-max` |
| [openaiStream.py](openaiStream.py) | 与 `openai02.py` 几乎相同，差别是 `stream=True` |
| [promptOptmize.py](promptOptmize.py) | few-shot 句子匹配（是 / 不是），`qwen3-max` |
| [proptFewshot.py](proptFewshot.py) | few-shot 金融文本四分类（含一条"不清楚类别"样本），`qwen3-max` |

共 22 个 `.py` 脚本 + 1 个无后缀文件。

---

## 已知问题与注意事项

学习过程中留下的半成品，如实列出，跑之前心里有数：

- **`jsonExtract.py` 后半段跑不通**：第 70 行用了 `json.dumps(...)`，但文件从头到尾只 `import os` 和 `from openai import OpenAI`，**没有 `import json`**。所以文件前一半（硬编码 messages 那次循环）能跑，后一半会直接 `NameError`。
- **`langchainPromptCompre` 没有 `.py` 后缀**（连内容一起被 git 跟踪了），不能直接 `python langchainPromptCompre`，要先手动指定解释器或改名。
- **`cosineDistance.py` 的 numpy 是在 `if __name__ == "__main__":` 块里才 import 的**（第 49 行），而 `get_norm()`（第 40 行）依赖全局的 `np`。直接当脚本跑没问题，但被别的文件 `import` 时会 `NameError`。
- **文件名笔误**：`proptFewshot.py`（少个 `m`）、`langchainPropTemplateChain.py`（`Prop` 应为 `Prompt`）、`langchLLM.py`（少个 `ain`）。
- **`proptFewshot.py` 内部标注和示例不一致**：`examples_data` 里用的 label 是 `'财务报告'`，而 `system` 提示词和 `examples_types` 里写的是 `'财务报道'`；另外 `examples_types` 这个列表定义了却没被使用，`examples_data` 里几段示例文本也是复制到一半就断句了。
- **`langchainEmbedding.py` / `langchainOllamaEmbedding.py` 里"不传 model 默认用的是 text-embeddings-v1"这句注释是两个文件里一模一样的复制粘贴**，`DashScopeEmbeddings()` 的默认模型和 Ollama 的默认模型不是同一个东西，这句注释请勿当真，以实际调用结果为准。
- **`ChatPromptTemplate.py` 把整段格式化文本（含 `System:` 前缀）当普通字符串传给了 chat 模型**，与 `chain.py` 用 `MessagesPlaceholder` + 链的写法形成对比；这是练习对照，不是推荐用法。
- **没有 `requirements.txt`**，依赖版本完全靠当前环境决定，不同 LangChain 大版本之间这些 API 可能已经有变动。
- 仓库内**没有** License 文件。

---

以上就是一份个人的 LangChain / 本地大模型学习笔记，代码都很粗糙，但每个小点都亲手跑过一遍。如果对你入门有一点帮助，或者你发现哪段代码写错了，欢迎提 Issue 交流 🎉
