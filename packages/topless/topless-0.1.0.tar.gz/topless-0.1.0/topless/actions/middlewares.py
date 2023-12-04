from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from topless.actions.envelopes import ActionEnvelope, RouteEnvelope
from topless.actions.handler import ActionHandler, ActionType
from topless.actions.response import Response
from topless.errors import (
    BadRequestError,
    ErrorCode,
    ForbiddenError,
    NotFoundError,
    ValidationError,
)
from topless.logger import logger


class BaseMiddleware(ABC):
    def __init__(self, app):
        self.app = app

    def before_action(self, envelope, handler):
        pass

    def after_action(self, response, handler):
        pass

    def before_envelope(self, event, context):
        pass

    def on_error(self, error):
        pass


class LogMiddleware(BaseMiddleware):
    def before_action(self, envelope: ActionEnvelope, _):
        envelope_type = envelope.__class__.__name__

        # logger.info(f"Envelope: {envelope_type}")

    def after_action(self, response, handler):
        pass
        # logger.info(f"Response: {response}")


class ResponseMiddleware(BaseMiddleware):
    def after_action(self, response, _):
        if isinstance(response, Response):
            return response.dump()

        return Response.ok(response).dump()

    def on_error(self, error: Exception):
        if isinstance(error, ValidationError):
            errors = self._get_validation_errors(error.messages)
            response = Response.bad_request(errors)
        elif isinstance(error, BadRequestError):
            response = Response.bad_request(str(error))
        elif isinstance(error, ForbiddenError):
            response = Response.forbidden(str(error))
        elif isinstance(error, NotFoundError):
            response = Response.not_found(str(error.args[0]))
        else:
            response = Response.internal_server_error()

        return response.dump()

    def _get_validation_errors(self, fields):
        errors = []
        for key, value in fields.items():
            errors.append(
                {
                    "code": ErrorCode.INVALID_FIELD,
                    "field": key,
                    "message": value[0],
                }
            )
        return errors


class ScopeMiddleware(BaseMiddleware):
    def before_action(self, envelope: RouteEnvelope, handler: ActionHandler):
        if handler.action_type != ActionType.ROUTE:
            return

        # Retrieve the required scope for this action
        required_scope = handler.data.get("scope")
        if not required_scope:
            # No specific scope required for this action
            return

        try:
            request_scopes = envelope.request_context.authorizer.scopes
        except AttributeError:
            request_scopes = []

        # Check if the required scope is in the request's scopes
        if required_scope not in request_scopes:
            raise ForbiddenError(f"Insufficient scope. Required: {required_scope}")
