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

    @staticmethod
    def ollama_persist(model: str):
        """持久化ollama模型"""

        json_data = {"model": model, "messages": [], "keep_alive": "24h"}
        url = f"http://{CONFIG.OLLAMA_URL}/api/chat"
        requests.post(url=url, json=json_data)
