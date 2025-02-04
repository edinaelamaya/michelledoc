from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.domain.models.document import Document
from app.domain.schemas.document import DocumentCreate, DocumentUpdate
from app.domain.repositories.document_repository import DocumentRepository

class MariaDBDocumentRepository(DocumentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, document: DocumentCreate) -> Document:
        db_document = Document(
            title=document.title,
            content=document.content,
            user_id=user_id
        )
        self.session.add(db_document)
        await self.session.commit()
        await self.session.refresh(db_document)
        return db_document

    async def get_by_id(self, document_id: int) -> Optional[Document]:
        result = await self.session.execute(
            select(Document).filter(Document.id == document_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: int) -> List[Document]:
        result = await self.session.execute(
            select(Document)
            .filter(Document.user_id == user_id)
            .order_by(Document.updated_at.desc())
        )
        return result.scalars().all()

    async def update(self, document_id: int, document_data: DocumentUpdate) -> Optional[Document]:
        document = await self.get_by_id(document_id)
        if not document:
            return None
            
        for key, value in document_data.dict(exclude_unset=True).items():
            setattr(document, key, value)
            
        await self.session.commit()
        await self.session.refresh(document)
        return document

    async def delete(self, document_id: int) -> bool:
        document = await self.get_by_id(document_id)
        if not document:
            return False
            
        await self.session.delete(document)
        await self.session.commit()
        return True

    async def search(self, user_id: int, query: str) -> List[Document]:
        result = await self.session.execute(
            select(Document)
            .filter(
                Document.user_id == user_id,
                or_(
                    Document.title.ilike(f"%{query}%"),
                    Document.content.ilike(f"%{query}%")
                )
            )
            .order_by(Document.updated_at.desc())
        )
        return result.scalars().all()