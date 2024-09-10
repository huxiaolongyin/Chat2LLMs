import os
import asyncio
import datetime
import streamlit as st
from typing import List
from haystack import Pipeline, component
from haystack.dataclasses import Document, ChatMessage, StreamingChunk
from core.retrieval import HTWDocument
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.builders import ChatPromptBuilder
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from haystack_integrations.components.generators.ollama import OllamaChatGenerator

from openinference.instrumentation.haystack import HaystackInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

endpoint = "http://localhost:6006/v1/traces"  # The URL to your Phoenix instance
tracer_provider = trace_sdk.TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))
HaystackInstrumentor().instrument(tracer_provider=tracer_provider)


@component
class DocumentProcessor:
    """数据处理组件"""

    @component.output_types(processed_documents=List[str])
    def run(self, documents: List[Document]):
        processed_documents = [doc.content for doc in documents]
        return {"processed_documents": processed_documents}


class ChatBot:
    # 使用的 Embedding 模型
    embedding_model_path = os.getenv("MODEL_PATH")

    def __init__(
        self,
        is_streaming: bool = True,
        store: str = "Document",
    ):
        """
        :param is_streaming: 是否使用流式输出
        :param store: 知识库名称
        """
        # 创建一个新的事件循环
        loop = asyncio.new_event_loop()
        # 将其设置为当前线程的事件循环
        asyncio.set_event_loop(loop)
        # 现在可以创建队列了
        self.queue = asyncio.Queue()
        self.running = True
        self.is_streaming = is_streaming
        self.document_store = HTWDocument(store).document_store
        self.llm = OllamaChatGenerator(
            model="llama3.1",
            url="http://192.168.30.66:11434/api/chat",
            generation_kwargs={
                "num_predict": 512,
                "temperature": 0.4,
            },
            streaming_callback=self.write_streaming_chunk,
        )

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
        llm = self.llm
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
    ) -> str:
        """输出查询结果"""
        self.placeholder = st.empty()
        self.tokens = []
        if history_messages is None:
            history_messages = [
                ChatMessage.from_user("问题：{{question}}，参考内容：{{content}}")
            ]

        # 创建一个任务来执行pipeline
        response = self.pipeline.run(
            data={
                "retriever": {
                    "top_k": top_k,
                    "score_threshold": 0.7,
                },
                "text_embedder": {"text": question},
                "messages": {"question": question, "template": history_messages},
            }
        )["llm"]

        # 标记流的结束
        self.queue.put_nowait("None")
        if "replies" in response:
            return response["replies"]
        else:
            raise Exception("No replies found in response")

    def write_streaming_chunk(self, chunk: StreamingChunk):
        """写入流式输出的内容"""
        self.queue.put_nowait(chunk)
        self.tokens.append(chunk.content)
        self.placeholder.write("".join(self.tokens))

    async def get_stream(self):
        while self.running:
            try:
                chunk = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                if chunk == "None":
                    self.running = False
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
