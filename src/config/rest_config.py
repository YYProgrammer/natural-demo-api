from fastapi import FastAPI

from src.api.chathistory.routes import router as router_chathistory
from src.api.hello.routes import router as router_hello
from src.api.notification.routes import router as router_notification
from src.api.planning.routes import remote_router as router_remote
from src.api.planning.routes import router as router_planning
from src.base.settings.settings import settings
from src.rest.healthz import router as router_status
from src.rest.home import router as router_home
from src.rest.rest import RestRegistry


def configure_rest(app: FastAPI):
    RestRegistry.register(router_home)
    RestRegistry.register(router_status)
    RestRegistry.register(router_planning)
    RestRegistry.register(router_remote)
    RestRegistry.register(router_notification)
    RestRegistry.register(router_hello)
    RestRegistry.register(router_chathistory)

    RestRegistry.apply(app, api_prefix=settings.api_prefix)
