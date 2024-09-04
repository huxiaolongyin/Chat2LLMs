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


class ChatWithOllama:
    def __init__(self, max_history_length: int = 8, is_streaming: bool = True):
        model_path = os.getenv("MODEL_PATH")
        self.MAX_HISTORY_LENGTH = max_history_length
        self.is_streaming = is_streaming
        self.query_pipeline = self._get_pipeline(model_path)

    def _get_pipeline(self, model_path):
        """建立一个pipeline"""
        document_store = HTWDocument().document_store
        # 建立模型
        llm = Ollama(is_streaming=self.is_streaming)
        retriever = QdrantEmbeddingRetriever(
            document_store=document_store,
        )
        text_embedder = SentenceTransformersTextEmbedder(model=model_path)
        prompt_builder = ChatPromptBuilder(variables=["question", "content"])

        query_pipeline = Pipeline()
        query_pipeline.add_component("text_embedder", text_embedder)
        query_pipeline.add_component("retriever", retriever)
        query_pipeline.add_component("processed_documents", DocumentProcessor())
        query_pipeline.add_component("messages", prompt_builder)
        query_pipeline.add_component("llm", llm)

        query_pipeline.connect("text_embedder.embedding", "retriever")
        query_pipeline.connect("retriever.documents", "processed_documents")
        query_pipeline.connect("processed_documents", "messages.content")
        query_pipeline.connect("messages", "llm.messages")

        return query_pipeline

    def chat(self, question: str, top_k: int, history_messages: ChatMessage):
        result = self.query_pipeline.run(
            data={
                "retriever": {"top_k": top_k, "score_threshold": 0.7},
                "text_embedder": {"text": question},
                "messages": {"question": question, "template": history_messages},
            }
        )
        # 历史消息存储
        answer = result["llm"]["replies"]

        return answer

    def knowledge_list(self):
        document_store = HTWDocument().document_store
        doc_list = []
        for doc in document_store.filter_documents():
            doc_list.append((doc.id, doc.content))
        return doc_list

    def add_knowledge(self, content):
        document_store = HTWDocument().document_store
        document_store.write_documents([content])

    def _trim_history(self, messages):
        if len(messages) > self.MAX_HISTORY_LENGTH:
            first_message = messages[0]
            latest_messages = messages[-(self.MAX_HISTORY_LENGTH - 1) :]
            return [first_message] + latest_messages
        else:
            return messages
