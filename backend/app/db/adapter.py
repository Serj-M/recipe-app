from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    """Абстрактный класс реализует принцип инверсии зависимости(DIP)"""

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
