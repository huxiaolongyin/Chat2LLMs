# Chat2LLMs
本项目计划开发一个 基于LLM的知识库问答系统。

能够实现
- 知识的多种类型文件导入
- 问答系统
- 语音交互
- 知识图谱建设

# 应用场景
- 作为企业的知识库
- 作为智能客服
- 硬件的智能服务

# 开发
技术栈
- Python >= 3.8
- 向量化：Bert-Chinese-base-v1
- 向量数据库：qdrant
- 数据库：SQLite
- 缓冲区：Redis
- 大模型：基于ollama的 llama3.1
- 大模型交互：haystack
- api服务：Fastapi
- 语音：whisper
- 知识图谱：待定

# 文件结构
```powershell
src
    ├─api # 提供api服务
    ├─chat # 聊天
    ├─config # 设置
    ├─core # 核心
    ├─embedding # 知识文件向量化
    ├─llms # 提供模型服务
    ├─pipeline # 管道
    ├─prompts # 提示词
    ├─retriever # 检索
    ├─speech2text # 语音转文字
    ├─text2speech # 文字转语音
    ├─textcls # 文字分类
    ├─vectorstore # 向量库存储
```

# 开发计划
## 实现语音交互的知识库问答服务

- [ ] 语音识别
- [ ] 与大模型交互
- [ ] 上下文处理
- [ ] 会话处理
- [ ] RAG知识库
- [ ] 实时信息的爬取

| tips：基于以上这些就可以进行硬件小助手的开发

## 管理系统
- [ ] 问答交互页面
- [ ] 知识文件导入管理


# 参考
- Fastgpt：https://github.com/labring/FastGPT
- ollama：https://github.com/ollama/ollama
- langchain：https://github.com/langchain-ai/langchain
