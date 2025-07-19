import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.base.settings.settings import settings
from src.config.exception_config import configure_exception_handlers
from src.config.rest_config import configure_rest
from src.rest.rest import CustomFastAPI


def application() -> FastAPI:
    app: FastAPI = CustomFastAPI(api_prefix=settings.api_prefix, api_apidoc_token=settings.api_apidoc_token)

    configure_exception_handlers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    configure_rest(app)

    return app


app: FastAPI = application()


def startup():
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)


if __name__ == "__main__":
    startup()
