import asyncio
import datetime
from core.config import CONFIG
from haystack.dataclasses import ChatMessage
from core.pipeline import generate_pipeline
from core.utils import check_openinference, StreamingMannager
from core.llms_manager import LLMsManager
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from core.retrieval.embedding import HTWDocument

# 开启调试模式
check_openinference()


class ChatBot:
    """
    构建一个ChatBot类，用于与用户进行交互
    steps:
        1. 获取pipeline

    """

    def __init__(
        self,
        model: str,
        store: str = "Document",
        is_streaming: bool = True,
    ):
        """
        args:
            model: 使用的模型名称
            # embedding_model: 使用的embedding模型
            store: 选择已经存入的知识库名称，和embedding模型对应
            is_streaming: 是否开启流式输出
        """
        self.model = model
        
        # 初始化流式输出管理器
        self.SMer = StreamingMannager()

        # 创建一个pipeline
        llm = LLMsManager(model=self.model, SMer=self.SMer).llm
        embedding_model_path = CONFIG.EMBEDDING_MODEL_PATH
        text_embedder = SentenceTransformersTextEmbedder(model=embedding_model_path)
        retriever = QdrantEmbeddingRetriever(HTWDocument(store).document_store)
        self.pipeline = generate_pipeline(llm, text_embedder, retriever)

    def query(
        self, question: str, top_k: int = 5, history_messages: ChatMessage = None
    ) -> dict:
        """输出查询结果"""

        # 清空之前的输出
        self.SMer.create_empty_placeholder()

        # 获取历史消息
        history_messages = history_messages or [
            ChatMessage.from_user("问题：{{question}}，参考内容：{{content}}")
        ]

        # 执行pipeline
        response = self.pipeline.run(
            data={
                "retriever": {
                    "top_k": top_k,
                    "score_threshold": 0.7,
                },
                "text_embedder": {"text": question},
                "function_info": {"question": question, "model": self.model},
                "messages": {"question": question, "template": history_messages},
            },
            include_outputs_from="retriever",
        )

        # 获取结果
        documents = response["retriever"]["documents"]
        answer = response["llm"]["replies"][0].content

        # 标记流的结束
        self.SMer.write_end_chunk()

        return answer, documents

    async def get_stream(self):
        """获取流式输出，用于api调用"""
        while self.SMer.running:
            try:
                chunk = await asyncio.wait_for(self.SMer.queue.get(), timeout=0.1)
                if chunk == "None":
                    self.SMer.running = False
                else:
                    data = {
                        "object": "message",
                        "content": chunk.content,
                        "role": chunk.meta["role"],
                        "model": chunk.meta["model"],
                        "done": chunk.meta["done"],
                        "create_time": datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }
                    yield f"data: {data}\n\n"
            except asyncio.TimeoutError:
                continue
