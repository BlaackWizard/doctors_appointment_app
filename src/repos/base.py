from abc import ABC, abstractmethod


class BaseRepo(ABC):

    @classmethod
    async def find_all(cls):
        ...

    @classmethod
    async def add(cls, **data):
        ...

    @classmethod
    async def find_by_id(cls, model_id: int):
        ...

    @classmethod
    async def find_one(cls, **filters):
        ...
