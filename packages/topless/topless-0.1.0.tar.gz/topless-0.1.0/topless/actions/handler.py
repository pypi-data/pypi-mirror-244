from dataclasses import dataclass
from typing import Callable

from aws_lambda_powertools.utilities.typing import LambdaContext
from strenum import StrEnum

from topless.actions.envelopes import ActionEnvelope
from topless.schemas import BaseSchema
from topless.utils.words import capitalize


class ActionType(StrEnum):
    ROUTE = "route"
    BUCKET = "bucket"
    SCHEDULE = "schedule"
    TOPIC = "topic"


class ActionHandler:
    def __init__(
        self,
        action_type: ActionType,
        path: str,
        key: str,
        schema: BaseSchema,
        fn: Callable,
        **kwargs,
    ):
        self.action_type = action_type
        self.path = path
        self.key = key
        self.schema = schema
        self.handler = None
        self.fn = fn
        self.data = kwargs

    def execute(self, envelope: ActionEnvelope):
        payload = self.schema.load(envelope.payload)

        return self.fn(payload)

    @property
    def name(self):
        return self.fn.__self__.__class__.__name__

    @property
    def service(self):
        names = self.fn.__self__.__class__.__module__.split(".")

        if len(names):
            return names[0]

        return "default"

    @property
    def resource(self):
        if self.handler:
            return self.handler

        return self.get_resource_name()

    def get_resource_name(self):
        service = capitalize(self.service)
        action_type = capitalize(self.action_type)

        return f"{action_type}Default"
