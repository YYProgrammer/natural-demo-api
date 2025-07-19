from typing import List

from fastapi import APIRouter, FastAPI


class RestRegistry:
    _router_list: List[APIRouter] = []

    @classmethod
    def register(cls, router: APIRouter) -> None:
        cls._router_list.append(router)

    @classmethod
    def apply(cls, app: FastAPI, api_prefix: str) -> None:
        for router in cls._router_list:
            app.include_router(router, prefix=api_prefix)
