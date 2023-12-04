from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any, Dict, List, Union
from uuid import UUID

from aws_lambda_powertools.utilities.data_classes import (
    APIGatewayProxyEvent,
    S3Event,
    SQSEvent,
)
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayEventRequestContext,
)
from aws_lambda_powertools.utilities.data_classes.s3_event import S3EventRecord
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord

from topless.schemas import BaseSchema, dataclass


class EnvelopeBuilder:
    def __init__(self, action_type, event: Dict[str, Any], app):
        self.action_type = action_type
        self.event = event
        self.app = app

    def build(self):
        mapper = {
            "route": RouteEnvelope,
            "topic": TopicEnvelope,
            "bucket": BucketEnvelope,
        }

        envelope = mapper[self.action_type]

        return envelope(self.event, self.app)


class RouteEnvelope(APIGatewayProxyEvent):
    def __init__(self, event: Dict[str, Any], app):
        super().__init__(event)

        self.app = app
        self.route_path = super().path
        self.params = self._load_params()

    @property
    def action_type(self):
        return "route"

    @property
    def path(self):
        return self.route_path

    @property
    def key(self):
        return self.http_method

    @property
    def payload(self) -> Dict[str, Any]:
        return {**(self.json_body or {}), **self.params}

    def _load_params(self):
        return {
            **(self.query_string_parameters or {}),
            **(self.multi_value_query_string_parameters or {}),
            **self._load_path_parameters(),
        }

    def _load_path_parameters(self):
        for path_pattern in self.app.registered_paths:
            params = self._extract_params(path_pattern, self.path)

            if params:
                self.route_path = path_pattern
                return params

        return {}

    def _extract_params(self, path_pattern, path):
        regex = self._path_to_regex(path_pattern)
        match = regex.match(path)
        if not match:
            return None  # or raise an error if a match is expected

        return match.groupdict()

    def _path_to_regex(self, path_pattern):
        # Convert dynamic segments like {param} to regex groups
        compiled = re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", path_pattern)
        return re.compile(f"^{compiled}$")


class BucketEnvelope(S3Event):
    def __init__(self, event: Dict[str, Any], app):
        super().__init__(event)
        self.app = app
        self.has_records = True

    @property
    def action_type(self):
        return "bucket"

    @property
    def path(self):
        paths = []
        for record in self.records:
            paths.append(record.s3.bucket.name)

        return paths

    @property
    def key(self):
        keys = []
        for record in self.records:
            keys.append(record.s3.get_object.key)

    @property
    def payload(self) -> Dict[str, Any]:
        data = {}
        for record in self.records:
            data[record.s3.get_object.key] = record.s3.get_object

        return data


class TopicEnvelope(SQSEvent):
    def __init__(self, event: Dict[str, Any], app):
        super().__init__(event)
        self.app = app

    @property
    def action_type(self):
        return "topic"

    @property
    def path(self):
        paths = []
        for record in self.records:
            paths.append(record.json_body.get("Message").get("topic"))

        return paths

    @property
    def key(self):
        keys = []
        for record in self.records:
            keys.append(record.json_body.get("Message").get("version"))

    @property
    def payload(self) -> Dict[str, Any]:
        data = {}
        for record in self.records:
            topic = self._build_message(record)

            data[topic.topic] = topic

        return data

    def _build_message(self, record: SQSRecord):
        return TopicMessage(**record.json_body.get("Message"))


@dataclass
class TopicMessage(BaseSchema):
    id: str
    resource_id: str
    payload: str
    topic: str
    origin: str
    at: str
    version: str


ActionEnvelope = Union[RouteEnvelope, BucketEnvelope, TopicEnvelope]
