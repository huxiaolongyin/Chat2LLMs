import requests
from core.config import CONFIG
from haystack_integrations.components.generators.ollama import OllamaChatGenerator
from core.utils import StreamingMannager


class LLMsManager:
    """
    大模型管理
    """

    def __init__(
        self,
        model: str,
        SMer: StreamingMannager = None,
        url: str = f"{CONFIG.OLLAMA_URL}/api/chat",
    ):
        self.model = model
        self.url = url
        self.llm = OllamaChatGenerator(
            model=model,
            url=url,
            generation_kwargs={
                "num_predict": 512,
                "temperature": 0.4,
            },
            streaming_callback=SMer.write_streaming_chunk,
        )

    def __call__(self):
        """
        当类被调用时直接返回 llm 的值
        """
        return self.llm

    def __getattr__(self, name: str):
        """
        允许访问 llm 的属性和方法
        """
        return getattr(self.llm, name)

    def persist(self):
        """持久化ollama模型"""
        # print(CONFIG.OLLAMA_URL)
        json_data = {"model": self.model, "messages": [], "keep_alive": "24h"}
        url = f"{CONFIG.OLLAMA_URL}/api/chat"
        
        requests.post(url=url, json=json_data)
