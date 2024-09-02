import os
from config import set_env
from model import Ollama
from embedding import Knowledge
from haystack import Pipeline
from haystack.dataclasses import ChatMessage
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.builders import ChatPromptBuilder
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever


class ChatWithOllama:
    def __init__(self, max_history_length: int = 8, is_streaming: bool = True):
        set_env()
        model_path = os.getenv("MODEL_PATH")
        self.MAX_HISTORY_LENGTH = max_history_length
        self.is_streaming = is_streaming
        self.query_pipeline = self._get_pipeline(model_path)

        # 加载消息
        with open(
            "D:/code/chat2LLMs/temp/prompt_template.txt", "r", encoding="utf-8"
        ) as file:
            messages_template = file.read()

        self.history_messages = [
            ChatMessage.from_system(messages_template),
            ChatMessage.from_user("问题：{{question}}，查询内容：{{content}}"),
        ]

    def _get_pipeline(self, model_path):
        """建立一个pipeline"""
        document_store = Knowledge.document_store
        # 建立模型
        llm = Ollama(is_streaming=self.is_streaming)
        retriever = QdrantEmbeddingRetriever(document_store=document_store)
        text_embedder = SentenceTransformersTextEmbedder(model=model_path)
        prompt_builder = ChatPromptBuilder(variables=["question", "content"])
        history_builder = ChatPromptBuilder()

        query_pipeline = Pipeline()
        query_pipeline.add_component("text_embedder", text_embedder)
        query_pipeline.add_component("retriever", retriever)
        query_pipeline.add_component("messages", prompt_builder)
        query_pipeline.add_component("llm", llm)
        query_pipeline.add_component("history_messages", history_builder)
        query_pipeline.connect("text_embedder.embedding", "retriever")
        query_pipeline.connect("retriever.documents", "messages.content")
        query_pipeline.connect("messages", "llm.messages")
        query_pipeline.connect("messages", "history_messages")

        return query_pipeline

    def chat(self, question: str):
        result = self.query_pipeline.run(
            data={
                "retriever": {"top_k": 5},
                "text_embedder": {"text": question},
                "messages": {"question": question, "template": self.history_messages},
            }
        )
        # 历史消息存储
        answer = result["llm"]["replies"]

        # 控制上下文长度
        self.history_messages = self._trim_history(result["history_messages"]["prompt"])
        self.history_messages.extend(answer)
        self.history_messages.append(
            ChatMessage.from_user("问题：{{question}}，查询内容：{{content}}")
        )
        return answer[0].content, self.history_messages

    def knowledge_list(self):
        document_store = Knowledge.document_store
        doc_list = []
        for doc in document_store.filter_documents():
            doc_list.append(doc.content)
        return doc_list

    def _trim_history(self, messages):
        if len(messages) > self.MAX_HISTORY_LENGTH:
            first_message = messages[0]
            latest_messages = messages[-(self.MAX_HISTORY_LENGTH - 1) :]
            return [first_message] + latest_messages
        else:
            return messages
