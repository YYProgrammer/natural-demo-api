from typing import Any, Dict, List

from fastapi import APIRouter, FastAPI
from fastapi.openapi.utils import get_openapi


class CustomFastAPI(FastAPI):
    def __init__(self, api_prefix: str, api_apidoc_token: str):
        super().__init__(
            title="Messager Agent API",
            description="Messager Agent API",
            version="1.0.0",
            openapi_url=f"{api_prefix}/{api_apidoc_token}/openapi.json",
            docs_url=f"{api_prefix}/docs",
            redoc_url=f"{api_prefix}/redoc",
        )

        self.api_prefix = api_prefix

    def openapi(self) -> Dict[str, Any]:
        if self.openapi_schema:
            return self.openapi_schema

        openapi_schema = get_openapi(title="apidoc", version="1.0.0", description="", routes=self.routes)

        new_paths = {}

        for path in openapi_schema["paths"]:
            if path.startswith(self.api_prefix):
                new_path = path.replace(self.api_prefix, "")
                new_paths[new_path] = openapi_schema["paths"][path]
            else:
                new_paths[path] = openapi_schema["paths"][path]

        openapi_schema["paths"] = new_paths

        for path in openapi_schema["paths"]:
            for method in openapi_schema["paths"][path]:
                operation = openapi_schema["paths"][path][method]
                if "summary" in operation:
                    description = operation.get("description", "")
                    operation["summary"] = f"{path} {description}"

        self.openapi_schema = openapi_schema
        return self.openapi_schema


class RestRegistry:
    _router_list: List[APIRouter] = []

    @classmethod
    def register(cls, router: APIRouter) -> None:
        cls._router_list.append(router)

    @classmethod
    def apply(cls, app: FastAPI, api_prefix: str) -> None:
        for router in cls._router_list:
            app.include_router(router, prefix=api_prefix)
