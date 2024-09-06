import os
from core.llms import Ollama
from core.retrieval import HTWDocument
from haystack import Pipeline
from haystack.dataclasses import ChatMessage
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.builders import ChatPromptBuilder
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever

from haystack import component
from typing import List
from haystack.dataclasses import Document


@component
class DocumentProcessor:
    """数据处理组件"""

    @component.output_types(processed_documents=List[str])
    def run(self, documents: List[Document]):
        processed_documents = [doc.content for doc in documents]
        return {"processed_documents": processed_documents}


class ChatBot:
    # 使用的 Embedding 模型

    def __init__(
        self,
        is_streaming: bool = True,
        store: str = "Document",
    ):
        """
        :param is_streaming: 是否使用流式输出
        :param store: 知识库名称
        """
        self.embedding_model_path = os.getenv("MODEL_PATH")
        self.is_streaming = is_streaming
        self.document_store = HTWDocument(store).document_store
        self.pipeline = self._get_pipeline(self.embedding_model_path)

    def _get_pipeline(self, embedding_model_path: str) -> Pipeline:
        """
        构建一个pipeline，流程如下
        1. 360 Bert embedding
        2. Qdrant retriever
        3. 文本处理 DocumentProcessor
        4. Chat Prompt Builder
        5. Ollama llama3.1
        """
        text_embedder = SentenceTransformersTextEmbedder(model=embedding_model_path)
        retriever = QdrantEmbeddingRetriever(self.document_store)
        llm = Ollama(is_streaming=self.is_streaming)
        prompt_builder = ChatPromptBuilder(variables=["question", "content"])

        pipeline = Pipeline()
        pipeline.add_component("text_embedder", text_embedder)
        pipeline.add_component("retriever", retriever)
        pipeline.add_component("processed_documents", DocumentProcessor())
        pipeline.add_component("messages", prompt_builder)
        pipeline.add_component("llm", llm)

        pipeline.connect("text_embedder.embedding", "retriever")
        pipeline.connect("retriever.documents", "processed_documents")
        pipeline.connect("processed_documents", "messages.content")
        pipeline.connect("messages", "llm.messages")

        return pipeline

    def query(
        self, question: str, top_k: int = 5, history_messages: ChatMessage = None
    ):
        """输出查询结果"""
        # if history_messages is None:
        history_messages = [
            ChatMessage.from_user("问题：{{question}}，参考内容：{{content}}")
        ]

        result = self.pipeline.run(
            data={
                "retriever": {
                    "top_k": top_k,
                    "score_threshold": 0.7,
                },
                "text_embedder": {"text": question},
                "messages": {"question": question, "template": history_messages},
            }
        )
        print(result)
        return result["llm"]


if __name__ == "__main__":
    bot = ChatBot(is_streaming=True)
    print(bot.query("你能做些什么"))
