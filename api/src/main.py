import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import HTMLResponse
from configuration.app import App
import config as config

app_instance = App()
app = app_instance.app


@app.get("/api/docs", response_class=HTMLResponse)
async def get_docs() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")


@app.get("/health")
async def health_check():
    return {"status": "ok"}

