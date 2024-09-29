from fastapi import FastAPI
from api.routes import router


def create_app():
    from core.config import CONFIG
    from fastapi.staticfiles import StaticFiles
    from fastapi.openapi.docs import get_swagger_ui_html
    
    # todo: 解决静态文件加载
    app = FastAPI(title="Chat2LLMs", version=CONFIG.VERSION)

    # 挂载静态文件目录
    # app.mount("/static", StaticFiles(directory="static"), name="static")

    # @app.get("/docs", include_in_schema=False)
    # async def custom_swagger_ui_html():
    #     return get_swagger_ui_html(   
    #         openapi_url=app.openapi_url,
    #         title=app.title + " - Swagger UI",
    #         oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    #         swagger_js_url="/static/swagger-ui-bundle.js",
    #         swagger_css_url="/static/swagger-ui.css",
    #     )
    app.include_router(router, prefix=CONFIG.WEB_ROUTE_PREFIX)
    return app


app = create_app()
