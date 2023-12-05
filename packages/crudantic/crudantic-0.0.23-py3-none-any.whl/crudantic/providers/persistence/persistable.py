from typing import Self, Any
from abc import ABC, abstractclassmethod, abstractmethod

from pydantic import BaseModel

from crudantic.providers.logging.structlog.provider import get_logger

logger = get_logger(__name__)


class Persistable(BaseModel):
    @classmethod
    def create(cls, instance: Self) -> Self:
        pass

    @classmethod
    def read(cls, id: str) -> Self:
        pass

    def update(self, instance: Self) -> Self:
        pass

    @classmethod
    def delete(cls, id: str) -> Self:
        pass

    @classmethod
    def list(cls):
        pass
