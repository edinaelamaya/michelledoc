from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.models.user import User
from app.domain.schemas.user import UserCreate, UserUpdate

class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: UserCreate) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        pass