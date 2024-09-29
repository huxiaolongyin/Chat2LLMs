from haystack import Pipeline
from haystack.components.builders import ChatPromptBuilder
from core.component import DocumentProcessor, FunctionInfo


def generate_pipeline(llm, text_embedder, retriever) -> Pipeline:
    """
    构建一个pipeline，流程如下
    1. 选择嵌入模型，将 quetion 进行向量化
    2. 从 Qdrant 进行检索： retriever
    3. 文本处理 DocumentProcessor
    4. 函数信息获取 FunctionInfo
    5. 构建 prompt
    6. 与大模型交互，获取答案

    args:
        llm: 大模型
        store: 知识库名称
    """

    prompt_builder = ChatPromptBuilder(variables=["question", "content"])

    pipeline = Pipeline()
    pipeline.add_component("text_embedder", text_embedder)
    pipeline.add_component("retriever", retriever)
    pipeline.add_component("processed_documents", DocumentProcessor())
    pipeline.add_component("function_info", FunctionInfo())
    pipeline.add_component("messages", prompt_builder)
    pipeline.add_component("llm", llm)

    pipeline.connect("text_embedder.embedding", "retriever")
    pipeline.connect("retriever.documents", "processed_documents")
    pipeline.connect("processed_documents", "function_info.documents")
    pipeline.connect("function_info.content", "messages.content")
    pipeline.connect("messages", "llm.messages")

    return pipeline
