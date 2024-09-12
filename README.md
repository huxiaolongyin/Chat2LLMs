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
    ├─api
    │  ├─v1             # api 版本
    │  └─router.py      # 主路由
    ├─core              # 核心模块
    │  ├─database       # 数据库处理
    │  │  ├─redis       # 缓冲区
    │  │  └─sqlite      # 数据库
    │  ├─llms           # 大模型交互
    │  └─retrieval      # 向量数据库
    ├─models            # 对象模型
    ├─schemas           # 数据模型
    ├─services          # 服务   
    ├─app.py            # streamlit 主程序(一个简单的页面)
    └─main.py           # 主程序

```

# 启动方式
## 测试
```powershell
# 启动 Arize Phoenix RAG监控服务
python -m phoenix.server.main serve

# 启动 FastAPI 服务
cd src
uvicorn main:app --reload

# 启动 Streamlit 服务
cd src
streamlit run ChatBot.py
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
- [ ] 一个简单的页面
  - [ ] 知识库管理
  - [ ] 知识内容管理
- [ ] 支持Docker Compose 部署

## V0.2.0
- [ ] 支持 Mysql

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