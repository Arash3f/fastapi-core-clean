from abc import ABC, abstractmethod
from typing import Self

from app.domain.repositories.user_repository import UserRepository


class UnitOfWork(ABC):
    users: UserRepository

    async def __aenter__(self) -> Self:
        return self

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
