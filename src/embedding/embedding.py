import os
from typing import List
from config import set_env
from haystack import Pipeline, Document
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore


class Knowledge:
    """
    知识库向量化存储
    """

    # document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")
    document_store = QdrantDocumentStore(
        url="localhost",
        index="Document",
        embedding_dim=768,
        # recreate_index=True,
        hnsw_config={"m": 16, "ef_construct": 64},  # Optional
    )

    @classmethod
    def write(cls, docs: List[str]):
        """将知识内容，写入知识库"""
        set_env()
        model_path = os.getenv("MODEL_PATH")
        # 获取文档
        documents = [Document(content=doc) for doc in docs]
        indexing_pipeline = Pipeline()
        indexing_pipeline.add_component(
            "embedder", SentenceTransformersDocumentEmbedder(model=model_path)
        )
        indexing_pipeline.add_component(
            "writer", DocumentWriter(document_store=cls.document_store)
        )
        indexing_pipeline.connect("embedder", "writer")
        indexing_pipeline.run({"documents": documents})

    def delete(self):
        self.document_store.delete_documents()

    @classmethod
    def get(cls):
        """从知识库获取文档"""
        return cls.document_store.filter_documents()
