from core.config import CONFIG
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from haystack.components.builders import ChatPromptBuilder
from core.component import DocumentProcessor, FunctionInfo
from haystack_integrations.components.generators.ollama import OllamaChatGenerator
from core.utils import StreamingMannager
from core.retrieval import HTWDocument


def generate_pipeline(
    SMer: StreamingMannager, model: str = "llama3.1", store: str = "Document"
) -> Pipeline:
    """
    构建一个pipeline，流程如下
    1. 360 Bert embedding
    2. Qdrant retriever
    3. 文本处理 DocumentProcessor
    4. 函数信息获取 FunctionInfo
    5. Chat Prompt Builder
    6. Ollama

    args:
        SMer: StreamingMannager
        model: ollama 的模型名称，目前仅支持 llama3.1、qwen2.5
        store: 知识库名称
    """
    llm = OllamaChatGenerator(
        model=model,
        url=f"{CONFIG.OLLAMA_URL}/api/chat",
        generation_kwargs={
            "num_predict": 512,
            "temperature": 0.4,
            "keep_alive": '24h', # -1 为永久
        },
        streaming_callback=SMer.write_streaming_chunk,
    )
    embedding_model_path = CONFIG.EMBEDDING_MODEL_PATH
    text_embedder = SentenceTransformersTextEmbedder(model=embedding_model_path)
    retriever = QdrantEmbeddingRetriever(HTWDocument(store).document_store)
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
