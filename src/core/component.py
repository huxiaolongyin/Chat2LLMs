from typing import List
from haystack import component
from haystack.dataclasses import Document
from core.tools.base import generate_function_response


@component
class DocumentProcessor:
    """数据处理组件"""

    @component.output_types(processed_documents=List[str])
    def run(self, documents: List[Document]):
        processed_documents = [doc.content for doc in documents]
        return {"processed_documents": processed_documents}


@component
class FunctionInfo:
    """获取函数执行信息组件"""

    @component.output_types(content=List[str])
    def run(self, documents: List[str], question: str, model: str):
        function_info = generate_function_response(
            question=question, model=model
        )  # todo
        return {"content": {"documents": documents, "function_info": [function_info]}}
