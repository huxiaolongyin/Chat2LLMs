import asyncio
import datetime
from haystack.dataclasses import ChatMessage
from core.pipeline import generate_pipeline
from core.utils import check_openinference, StreamingMannager

# 开启调试模式
check_openinference()


class ChatBot:

    def __init__(
        self,
        is_streaming: bool = True,
        model: str = "llama3.1",
        store: str = "Document",
    ):
        """
        :param is_streaming: 是否使用流式输出
        :param store: 知识库名称
        """
        self.SMer = StreamingMannager()
        # 创建一个pipeline
        self.model = model
        self.pipeline = generate_pipeline(self.SMer, model=self.model, store=store)

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
