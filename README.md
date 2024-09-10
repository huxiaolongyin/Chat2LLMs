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
**技术栈**
- Python >= 3.8
- 向量数据库：qdrant
- 数据库：SQLite/MySQL
- 缓冲区：Redis
- 大模型交互：haystack
- 大模型监控：phoenix
- api服务：Fastapi
- 知识图谱：待定

**模型方面**
- 向量化模型：360Zhinao-search
- 文本大模型：基于 ollama的 llama3.1
- 语音模型：whisper
  
# 文件结构
```powershell
src
    ├─assistant # 助手
    ├─auth # 用户认证
    ├─chat # 聊天
    ├─config # 设置
    ├─core # 核心
    ├─database # 数据库管理
    ├─knowledge # 知识库管理
    ├─manage # 管理服务
    ├─message # 消息
    ├─models # 数据库、表对象模型

```

# 开发计划
## V0.1.0
实现最小化可行产品(MVP)
- [x] 支持文本问答
- [x] 支持 RAG 知识库管理，进行上传、删除、查询
- [x] 支持上下文
- [x] 支持助手管理
- [x] 支持会话管理
- [x] 实时流处理

## V0.2.0
- [ ] 支持Docker Compose 部署
- [ ] 支持文本模型选择、嵌入模型选择
- [ ] 支持语音交互
- [ ] 支持 doc 文件上传管理
- [ ] 支持用户认证
- [ ] 支持实体识别

## V0.3.0
- [ ] 支持知识图谱
- [ ] 支持网上数据的爬取


## todo
- [ ] 日志
- [ ] 函数调用
  

# 参考
- Fastgpt：https://github.com/labring/FastGPT
- ollama：https://github.com/ollama/ollama
- langchain：https://github.com/langchain-ai/langchain
- taskingAI：https://github.com/TaskingAI/TaskingAI