import os
from typing import List, Dict
from haystack import Pipeline, Document
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from transformers import BertConfig
from qdrant_client import QdrantClient


class HTWDocument:
    """
    知识库向量化存储
    """

    def __init__(
        self,
        store: str = "Document",
        model_path: str = os.getenv("MODEL_PATH"),
        db_host: str = "localhost",
        port: int = 6333,
    ):
        self.store = store
        self.model_path = model_path
        self.db_host = db_host
        self.port = port
        self.document_store = self.__get_store

    @property
    def __get_store(self):
        embedding_dim = BertConfig.from_pretrained(self.model_path).hidden_size
        document_store = QdrantDocumentStore(
            host=self.db_host,
            port=self.port,
            index=self.store,
            embedding_dim=embedding_dim,
            # recreate_index=True,
            hnsw_config={"m": 16, "ef_construct": 64},  # Optional
        )
        return document_store

    def store_list(self) -> List[str]:
        """获取所有知识库的名称"""
        client = QdrantClient(host=self.db_host, port=self.port)
        indexes = client.get_collections().collections
        return [index.name for index in indexes]

    def write_docs(
        self,
        docs: List[str] = None,
    ):
        """将知识内容，写入知识库"""

        # 获取文档
        documents = [Document(content=doc) for doc in docs]
        indexing_pipeline = Pipeline()
        indexing_pipeline.add_component(
            "embedder", SentenceTransformersDocumentEmbedder(model=self.model_path)
        )
        indexing_pipeline.add_component(
            "writer", DocumentWriter(document_store=self.document_store)
        )
        indexing_pipeline.connect("embedder", "writer")
        res = indexing_pipeline.run({"documents": documents})
        return res

    def get_docs(self, filter: Dict[str, str] = None):
        """获取知识库内容，若没有，则返回所有知识内容"""
        docs = self.document_store.filter_documents(filter)
        res = []
        for doc in docs:
            res.append({"id": doc.id, "content": doc.content})

        return res

    def del_docs(self, ids: List[str] = None):
        """删除知识内容"""
        return self.document_store.delete_documents(ids)
    
    def del_store(self, store: str = None):
        """删除知识库"""
        pass
