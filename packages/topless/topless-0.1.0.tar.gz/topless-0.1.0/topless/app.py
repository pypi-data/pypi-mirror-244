import inspect
from typing import Callable, Dict, List, Optional

from topless.actions.handler import ActionHandler
from topless.actions.middlewares import BaseMiddleware
from topless.models.connection import Connection
from topless.models.orm.mapper import registry
from topless.schemas import BaseSchema


class Topless:
    _instance = None
    _mapper = None

    def get_connection_string(self):
        return self.connection.get_connection_string()

    def get_mapper(self):
        if not self._mapper:
            self._mapper = registry()

        return self._mapper

    def __init__(self, name: Optional[str] = None):
        self.name = name
        self.services: List[str] = []

        self.actions: List[ActionHandler] = []
        self.middlewares: List[BaseMiddleware] = []
        self.connection: Connection = Connection.instance()

        self.registered_paths: List[str] = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Topless, cls).__new__(cls)

        return cls._instance

    def register_service(self, service):
        self.services.append(service)

        return service

    def register_middleware(self, service):
        middleware = service(self)
        self.middlewares.append(middleware)

        return middleware

    def schedule(self, cron: str, handler=None, **kwargs):
        def decorator(cls: Callable):
            self._build_action("schedule", cls, cron, "cron")
            return cls

        return decorator

    def topic(self, name: str, version: str = "v1", handler=None, **kwargs):
        def decorator(cls: Callable):
            self._build_action("topic", cls, name, version)
            return cls

        return decorator

    def bucket(self, name: str, path: str, handler=None, **kwargs):
        def decorator(cls: Callable):
            self._build_action("bucket", cls, name, path)
            return cls

        return decorator

    def route(self, path: str, methods: List[str] = ["GET"], handler=None, **kwargs):
        def decorator(cls: Callable):
            self.registered_paths.append(path)
            self._build_action("route", cls, path, methods, **kwargs)

            return cls

        return decorator

    def _build_action(self, action_type, cls, path, key, **kwargs):
        action = cls().handle
        schema = self._get_inferred_schema(action)

        # for route, key is methods which can be a list like ['GET', 'POST']
        if isinstance(key, list):
            for k in key:
                handler = ActionHandler(action_type, path, k, schema, action, **kwargs)
                self.actions.append(handler)
        else:
            handler = ActionHandler(action_type, path, key, schema, action, **kwargs)
            self.actions.append(handler)

    def _get_inferred_schema(self, action: Callable) -> BaseSchema:
        sig = inspect.signature(action)
        params = list(sig.parameters.values())

        if params[0] and params[0].annotation is not params[0].empty:
            return params[0].annotation

        raise Exception("Invalid schema")
