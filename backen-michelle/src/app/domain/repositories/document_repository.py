from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.models.document import Document
from app.domain.schemas.document import DocumentCreate, DocumentUpdate

class DocumentRepository(ABC):
    @abstractmethod
    async def create(self, user_id: int, document: DocumentCreate) -> Document:
        pass

    @abstractmethod
    async def get_by_id(self, document_id: int) -> Optional[Document]:
        pass

    @abstractmethod
    async def get_by_user(self, user_id: int) -> List[Document]:
        pass

    @abstractmethod
    async def update(self, document_id: int, document_data: DocumentUpdate) -> Optional[Document]:
        pass

    @abstractmethod
    async def delete(self, document_id: int) -> bool:
        pass

    @abstractmethod
    async def search(self, user_id: int, query: str) -> List[Document]:
        pass