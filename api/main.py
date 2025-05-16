import uvicorn
from src.configuration.app import App
import config
app = App()

if __name__ == "__main__":
    uvicorn.run(app, **config.uvicorn.dict())