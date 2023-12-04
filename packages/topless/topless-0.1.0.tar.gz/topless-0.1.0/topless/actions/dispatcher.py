from typing import Any

from aws_lambda_powertools.utilities.typing import LambdaContext

from topless.actions.envelopes import (
    ActionEnvelope,
    BucketEnvelope,
    RouteEnvelope,
    TopicEnvelope,
)
from topless.app import Topless
from topless.utils.words import snakefy


class Dispatcher:
    def __init__(self, app: Topless, event: Any, context: LambdaContext):
        self.event = event
        self.context = context
        self.app = app

    @property
    def action_type(self):
        fname = snakefy(self.context.function_name.split("-")[1])

        _, action, *_ = fname.split("_")  # type: ignore
        return action

    def run(self):
        try:
            for middleware in self.app.middlewares:
                middleware.before_envelope(self.event, self.context)

            envelope = self._build_envelope()

            handler = self._locate(envelope)

            for middleware in self.app.middlewares:
                middleware.before_action(envelope, handler)

            response = handler.execute(envelope)

            for middleware in self.app.middlewares:
                response_md = middleware.after_action(response, handler)
                if response_md:
                    response = response_md

            return response

        except Exception as e:
            for middleware in reversed(self.app.middlewares):
                response_md = middleware.on_error(e)
                if response_md:
                    return response_md

    def _build_envelope(self):
        mapper = {
            "route": RouteEnvelope,
            "topic": TopicEnvelope,
            "bucket": BucketEnvelope,
        }

        envelope = mapper[self.action_type]

        return envelope(self.event, self.app)

    def _locate(self, envelope: ActionEnvelope):
        fn = None
        for action in self.app.actions:
            if (
                action.action_type == envelope.action_type
                and action.path == envelope.path
                and action.key == envelope.key
            ):
                fn = action
                break

        if fn:
            return fn
        else:
            raise Exception(
                f"Action not found. (type:{envelope.action_type}, path:{envelope.path}, key:{envelope.key})"
            )
