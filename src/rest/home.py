from datetime import datetime

from fastapi import APIRouter, Response
from injector import inject

router = APIRouter()


@router.get("/echo")
@inject
def echo(hello: str = "Hello") -> Response:
    return Response(content=f"{hello}, current time is {datetime.now()}", media_type="text/plain")
