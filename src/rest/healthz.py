from fastapi import APIRouter
from injector import inject

router = APIRouter()


@router.get("/healthz")
@inject
def healthz() -> dict[str, str]:
    return {}
