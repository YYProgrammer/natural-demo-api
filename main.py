import uvicorn
from fastapi import FastAPI

# from fastapi.staticfiles import StaticFiles
from src.api.api_config import api_config
from src.base.settings.settings import settings

app = FastAPI(
    title="Natural Demo API",
    description="Natural Demo API Service",
    version="1.0.0",
)

print(settings.api_prefix)

api_config.apply(app=app, api_prefix=settings.api_prefix)

# Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=True
    )
