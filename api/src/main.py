import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import HTMLResponse
from configuration.app import App
import config as config

app_instance = App()
app = app_instance.app


@app.get("/api/docs", response_class=HTMLResponse, include_in_schema=False)
async def get_docs():
    return get_swagger_ui_html(openapi_url='/openapi.json', title='API Documentation')


if __name__ == "__main__":
    uvicorn.run(app, **config.uvicorn.dict())
