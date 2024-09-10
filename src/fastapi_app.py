from fastapi import FastAPI
from routes import router


def create_app():
    from config import CONFIG

    app = FastAPI(title="Chat2LLMs", version=CONFIG.VERSION)

    app.include_router(router, prefix=CONFIG.WEB_ROUTE_PREFIX)

    return app


app = create_app()
