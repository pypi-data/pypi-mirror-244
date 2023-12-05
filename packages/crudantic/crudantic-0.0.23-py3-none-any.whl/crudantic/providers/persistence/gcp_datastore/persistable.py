import os
from uuid import uuid4
from typing import Self, ClassVar

from google.cloud import datastore

from crudantic.providers.persistence.persistable import Persistable
from crudantic.providers.logging.structlog.provider import get_logger

logger = get_logger(__name__)


class GCPPersistable(Persistable):
    client: ClassVar[datastore.Client] = datastore.Client(
        project=os.getenv("PROJECT_ID"),
        database=os.getenv("DATABASE_NAME"),
    )

    @staticmethod
    def unique_id():
        return uuid4().__str__().replace("-", "")

    def build_key(self):
        key = (self.__class__.__name__, self.id)
        return key

    @classmethod
    def create(cls, instance: Self) -> Self:
        key = cls.client.key(
            *instance.build_key(),
        )

        entity = datastore.Entity(key)
        entity.update(instance.model_dump())
        cls.client.put(entity)
        instance = cls.model_validate(entity)

        return instance

    @classmethod
    def read(cls, id: str | int) -> Self:
        instance = cls.model_construct(id=id)
        key = cls.client.key(
            *instance.build_key(),
        )
        existing = cls.client.get(key)
        if existing:
            instance = cls.model_validate(existing)
        else:
            raise ValueError(f"Instance {cls.__name__}[{key}] not found")

        return instance

    def update(self, instance: Self | None = None) -> Self:
        if not instance:
            instance = self

        key = self.client.key(*instance.build_key())
        existing = self.client.get(key)
        existing.update(instance.model_dump())
        self.client.put(existing)

        updated = self.client.get(key)
        instance = self.__class__.model_validate(updated)

        return instance

    def delete(self) -> Self:
        key = self.client.key(
            *self.build_key(),
        )

        existing = self.client.get(key)
        self.client.delete(key)

        return self.__class__.model_validate(existing)

    @classmethod
    def list(cls, limit=10):
        query = cls.client.query(kind=cls.__name__)
        results = [cls.model_validate(item) for item in query.fetch(limit=limit)]
        return results
