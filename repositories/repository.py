from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one(self, schema):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, parameter):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, parameter):
        raise NotImplementedError
