from abc import ABC


class BaseRepo(ABC):

    @classmethod
    async def find_all(cls):
        ...

    @classmethod
    async def find_all_by_filters(cls, **filters):
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

    @classmethod
    async def update(cls, model_id, **values):
        ...

    @classmethod
    async def delete_one(cls, model_id):
        ...
