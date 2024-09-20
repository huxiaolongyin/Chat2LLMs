import os
from typing import List, Dict
from core.config import CONFIG
from haystack import Pipeline, Document
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from transformers import BertConfig
from qdrant_client import QdrantClient
from schemas import StoreBase, DocumentBase


class HTWDocument:
    """
    知识库向量化存储
    """

    def __init__(
        self,
        store: str = "Document",
        model_path: str = CONFIG.EMBEDDING_MODEL_PATH,
        db_host: str = CONFIG.QRANT_HOST,
        port: int = CONFIG.QRANT_PORT,
    ):
        self.store = store
        self.model_path = model_path
        self.db_host = db_host
        self.port = port
        self.embedding_dim = BertConfig.from_pretrained(model_path).hidden_size
        self.document_store = self.__get_store

    @property
    def __get_store(self):
        document_store = QdrantDocumentStore(
            host=self.db_host,
            port=self.port,
            index=self.store,
            embedding_dim=self.embedding_dim,
            # recreate_index=True,
            hnsw_config={"m": 16, "ef_construct": 64},  # Optional
        )
        return document_store

    def store_collections(self) -> List[StoreBase]:
        """获取所有知识库详细信息"""
        client = QdrantClient(host=self.db_host, port=self.port)
        collections = [
            StoreBase(
                store_name=index.name,
                status=collection_info.status,
                document_count=collection_info.points_count,
                embedding_size=collection_info.config.params.vectors.size,
                distance=collection_info.config.params.vectors.distance.value,
            )
            for index in client.get_collections().collections
            if (collection_info := client.get_collection(index.name))
        ]

        return collections

    def get_store_list(self) -> List[str]:
        """获取所有知识库名称"""
        client = QdrantClient(host=self.db_host, port=self.port)
        collections = [
            index.name
            for index in client.get_collections().collections
            if (collection_info := client.get_collection(index.name))
        ]
        return collections

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

    def get_documents(self, filter: Dict[str, str] = None) -> List[DocumentBase]:
        """获取知识库内容，若没有，则返回所有知识内容"""
        documents = self.document_store.filter_documents(filter)

        result = [DocumentBase(id=doc.id, content=doc.content) for doc in documents]

        return result

    def del_docs(self, ids: List[str] = None):
        """删除知识内容"""
        return self.document_store.delete_documents(ids)

    def del_store(self, store: str = None):
        """删除知识库"""
        client = QdrantClient(host=self.db_host, port=self.port)
        try:
            client.delete_collection(collection_name=store)
            return {"delete_status": "SUCCESS"}
        except Exception as e:
            return {"delete_status": "ERROR", "message": str(e)}

    def new_store(self, name: str = None):
        """新建知识库"""
        client = QdrantClient(host=self.db_host, port=self.port)
        try:
            client.create_collection(
                collection_name=name,
                vectors_config={"size": self.embedding_dim, "distance": "Cosine"},
            )
            return {"create_status": "SUCCESS"}
        except Exception as e:
            return {"create_status": "ERROR", "message": str(e)}
