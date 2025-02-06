from typing import List, Optional
from app.application.interfaces.repositories import IDocumentRepository
from app.domain.schemas.document import DocumentCreate, DocumentUpdate, DocumentInDB
from app.infrastructure.database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession

class DocumentService:
    def __init__(self, document_repository: IDocumentRepository, db: AsyncSession):
        self.document_repository = document_repository
        self.db = db

    async def create_document(self, user_id: int, document_data: DocumentCreate) -> DocumentInDB:
        return await self.document_repository.create(user_id, document_data)

    async def get_document(self, document_id: int, user_id: int) -> DocumentInDB:
        document = await self.document_repository.get_by_id(document_id, user_id)
        if not document:
            raise ValueError("Document not found")
        return document

    async def get_user_documents(self, user_id: int) -> List[DocumentInDB]:
        return await self.document_repository.get_all_by_user(user_id)

    async def update_document(self, document_id: int, document_data: DocumentUpdate) -> Optional[DocumentInDB]:
        current_document = await self.document_repository.get_by_id(document_id)
        if not current_document:
            raise ValueError("Document not found")
        
        return await self.document_repository.update(document_id, document_data)

    async def delete_document(self, document_id: int) -> bool:
        return await self.document_repository.delete(document_id)

    async def search_documents(self, user_id: int, query: str) -> List[DocumentInDB]:
        return await self.document_repository.search(user_id, query)

    async def get_documents(self, user_id: int):
        # Lógica para obtener documentos del usuario
        pass