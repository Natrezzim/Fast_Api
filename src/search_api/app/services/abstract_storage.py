from abc import ABC, abstractmethod


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        pass


class AsyncStorage(ABC):
    @abstractmethod
    async def get(self, index: str, id: str, **kwargs):
        pass

    @abstractmethod
    async def search(self, index: str, size: int, body: dict, **kwargs):
        pass
