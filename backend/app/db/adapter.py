from abc import ABC, abstractmethod


class BaseAdapter(ABC):

    @abstractmethod
    async def add(self, **kwargs):
        pass

    @abstractmethod
    async def get(self, **kwargs):
        pass

    @abstractmethod
    async def remove(self, **kwargs):
        pass

    @abstractmethod
    async def update(self, **kwargs):
        pass
