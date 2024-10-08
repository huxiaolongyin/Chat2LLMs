from typing import List, Dict
from core.config import CONFIG
from transformers import BertConfig
from qdrant_client import QdrantClient
from schemas import StoreBase, DocumentBase
from haystack import Pipeline, Document
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from qdrant_client.models import Distance, VectorParams


class HTWDocument:
    """
    知识库向量化存储，使用 haystack_Qdrant 进行管理
    """

    qdrant_client = QdrantClient(
        host=CONFIG.QRANT_HOST,
        port=CONFIG.QRANT_PORT,
        grpc_port=CONFIG.QRANT_GRPC_PORT,
        prefer_grpc=True,
    )

    def __init__(
        self,
        store: str = "Document",
        model_path: str = CONFIG.EMBEDDING_MODEL_PATH,
    ):
        self.store = store
        self.model_path = model_path
        self.embedding_dim = BertConfig.from_pretrained(model_path).hidden_size
        self.document_store = self.__get_store

    @property
    def __get_store(self):
        document_store = QdrantDocumentStore(
            host=CONFIG.QRANT_HOST,
            index=self.store,
            embedding_dim=self.embedding_dim,
            # recreate_index=True,
            hnsw_config={"m": 16, "ef_construct": 64},  # Optional
        )
        return document_store

    def create_knowledge_store(self, name: str = None):
        """新建知识库"""
        try:
            self.qdrant_client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=self.embedding_dim, distance=Distance.COSINE
                ),
            )

            return {"create_status": "SUCCESS"}
        except Exception as e:
            return {"create_status": "ERROR", "message": str(e)}

    def get_all_knowledge_store_details(self) -> List[StoreBase]:
        """获取所有知识库详细信息"""
        collections = [
            StoreBase(
                store_name=index.name,
                status=collection_info.status,
                document_count=collection_info.points_count,
                embedding_size=collection_info.config.params.vectors.size,
                distance=collection_info.config.params.vectors.distance.value,
            )
            for index in self.qdrant_client.get_collections().collections
            if (collection_info := self.qdrant_client.get_collection(index.name))
        ]

        return collections

    def get_all_knowledge_store_names(self) -> List[str]:
        """获取所有知识库名称"""
        collections = [
            index.name
            for index in self.qdrant_client.get_collections().collections
            if (collection_info := self.qdrant_client.get_collection(index.name))
        ]
        return collections

    def delete_knowledge_store(self, store: str = None):
        """删除知识库"""
        try:
            self.qdrant_client.delete_collection(collection_name=store)
            return {"delete_status": "SUCCESS"}
        except Exception as e:
            return {"delete_status": "ERROR", "message": str(e)}

    def save_knowledge_content(
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
        return indexing_pipeline.run({"documents": documents})

    def get_knowledge_content_or_all(
        self, filter: Dict[str, str] = None
    ) -> List[DocumentBase]:
        """获取知识库内容，若没有，则返回所有知识内容"""
        documents = self.document_store.filter_documents(filter)

        result = [DocumentBase(id=doc.id, content=doc.content) for doc in documents]

        return result

    def delete_knowledge_content(self, ids: List[str] = None):
        """删除知识内容"""
        return self.document_store.delete_documents(ids)
