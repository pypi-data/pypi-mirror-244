
import abc
import asyncio
import json

from typing import Callable
from starlette.types import Scope
from starlette.types import Receive
from starlette.types import Send

from starlette.requests import Request
from starlette.responses import Response
from starlette.responses import JSONResponse

from ezcx.webhooks.request import WebhookRequest
from ezcx.webhooks.response import WebhookResponse


class Router(abc.ABC):
    
    def __init__(self):
        self.routes = {}

    @abc.abstractmethod
    def get_handler(self, tag_or_scope) -> Callable:
        ...

    @staticmethod
    def asyncify(handler: Callable):
        if not asyncio.iscoroutinefunction(handler):
            async def coroutine(res, req):
                handler(res, req)
            return coroutine
        return handler


class PathRouter(Router):

    def register(self, path: str, handler: Callable):
        handler = self.asyncify(handler)
        self.routes[path] = handler

    def get_handler(self, scope: Scope):
        # 2023-12-02 - changed from indexing to "get" method to return None
        # if nothing matches
        return self.routes.get(scope['path'])

class TagRouter(Router):

    def register(self, tag: str, handler: Callable):
        handler = self.asyncify(handler)
        self.routes[tag] = handler

    def get_handler(self, wh_request: WebhookRequest):
        # 2023-12-02 - changed from indexing to "get" method to return None
        # if nothing matches
        return self.routes.get(wh_request.tag)


class Server:

    def __init__(self, router: Router):
        self.router = router

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope, receive)
        body = await request.json()
        wh_request = WebhookRequest(body)
        wh_response = WebhookResponse()
        if isinstance(self.router, TagRouter):
            handler = self.router.get_handler(wh_request)
            path_type, route = 'tag', wh_request.tag
        elif isinstance(self.router, PathRouter):
            handler = self.router.get_handler(scope)
            path_type, route = 'path', scope['path']
        if not handler:
            not_found_error = {
                'type': path_type,
                'route': route
            }
            await JSONResponse(not_found_error, status_code=404)
            return
        await handler(wh_response, wh_request)
        await JSONResponse(wh_response.to_dict())(scope, receive, send)

