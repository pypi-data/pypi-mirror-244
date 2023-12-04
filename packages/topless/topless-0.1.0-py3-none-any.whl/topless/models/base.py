from __future__ import annotations

from typing import ClassVar, List

from topless.models.orm.manager import Manager, ModelDescriptor
from topless.schemas import BaseSchema


class BaseModel(BaseSchema):
    _registry: List[BaseModel] = []

    objects: ClassVar = ModelDescriptor(Manager())

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry.append(cls)
