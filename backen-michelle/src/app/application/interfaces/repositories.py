from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.schemas.user import UserCreate, UserUpdate, UserInDB
from app.domain.schemas.document import DocumentCreate, DocumentUpdate, DocumentInDB

class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user_data: UserCreate) -> UserInDB:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[UserInDB]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserInDB]:
        pass

    @abstractmethod
    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserInDB]:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        pass

class IDocumentRepository(ABC):
    @abstractmethod
    async def create(self, document_data: DocumentCreate) -> DocumentInDB:
        pass

    @abstractmethod
    async def get_by_id(self, document_id: int) -> Optional[DocumentInDB]:
        pass

    @abstractmethod
    async def get_all_by_user(self, user_id: int) -> List[DocumentInDB]:
        pass

    @abstractmethod
    async def update(self, document_id: int, document_data: DocumentUpdate) -> Optional[DocumentInDB]:
        pass

    @abstractmethod
    async def delete(self, document_id: int) -> bool:
        pass

    @abstractmethod
    async def search(self, user_id: int, query: str) -> List[DocumentInDB]:
        pass