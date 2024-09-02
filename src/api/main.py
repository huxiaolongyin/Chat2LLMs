import json
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from chat import ChatWithOllama
from fastapi.responses import StreamingResponse
from api.chat_api_model import ChatData
from api.knowledge_model import KnowledgeModel
from embedding import Knowledge

# from api.router import router
from openinference.instrumentation.haystack import HaystackInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

endpoint = "http://localhost:6006/v1/traces" # The URL to your Phoenix instance
tracer_provider = trace_sdk.TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

HaystackInstrumentor().instrument(tracer_provider=tracer_provider)

def create_app():
    app = FastAPI()
    ollama = ChatWithOllama()
    security = HTTPBearer()

    @app.get("/health")
    def get_health():
        """获取服务健康状态"""
        return {"status": "OK"}

    @app.get("/knowledge")
    def get_knowledge():
        """获取知识内容"""
        return {"knowledge": ollama.knowledge_list()}

    @app.post("/chat")
    def get_chat(chat: ChatData):
        # async def generate_response():
        #     answer, _ = ollama.chat(chat.question)
        #     yield f"data: {json.dumps({'answer': answer}, ensure_ascii=False)}\n\n"
        answer, _ = ollama.chat(chat.question)
        return StreamingResponse({json.dumps({"answer": answer}, ensure_ascii=False)})

    @app.post("/add_knowledge")
    def add_knowledge(KnowledgeModel: KnowledgeModel):
        Knowledge.write([KnowledgeModel.data])

        return {"status": "OK"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
