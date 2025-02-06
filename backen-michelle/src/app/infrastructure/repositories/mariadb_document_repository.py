from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, text
from app.domain.models.document import Document
from app.domain.schemas.document import DocumentCreate, DocumentUpdate, DocumentInDB
from app.domain.repositories.document_repository import DocumentRepository
from app.application.interfaces.repositories import IDocumentRepository

class MariaDBDocumentRepository(IDocumentRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, document_data: DocumentCreate) -> DocumentInDB:
        query = text("""
            INSERT INTO documents (title, content, user_id)
            VALUES (:title, :content, :user_id)
        """)
        
        result = await self.db.execute(
            query,
            {
                "title": document_data.title,
                "content": document_data.content,
                "user_id": user_id
            }
        )
        await self.db.commit()
        
        document_id = result.lastrowid
        return DocumentInDB(
            id=document_id,
            title=document_data.title,
            content=document_data.content,
            user_id=user_id
        )

    async def get_by_id(self, document_id: int, user_id: int = None) -> DocumentInDB:
        query = text("SELECT * FROM documents WHERE id = :id")
        result = await self.db.execute(query, {"id": document_id})
        document = result.fetchone()
        if document:
            return DocumentInDB(
                id=document.id,
                title=document.title,
                content=document.content,
                user_id=document.user_id
            )
        return None

    async def get_all_by_user(self, user_id: int) -> list[DocumentInDB]:
        query = text("SELECT * FROM documents WHERE user_id = :user_id")
        result = await self.db.execute(query, {"user_id": user_id})
        documents = result.fetchall()
        return [
            DocumentInDB(
                id=doc.id,
                title=doc.title,
                content=doc.content,
                user_id=doc.user_id
            ) for doc in documents
        ]

    async def update(self, document_id: int, document_data: DocumentUpdate) -> DocumentInDB:
        query = text("""
            UPDATE documents 
            SET title = :title, content = :content
            WHERE id = :id
        """)
        
        await self.db.execute(
            query,
            {
                "id": document_id,
                "title": document_data.title,
                "content": document_data.content
            }
        )
        await self.db.commit()
        
        return await self.get_by_id(document_id)

    async def delete(self, document_id: int) -> bool:
        query = text("DELETE FROM documents WHERE id = :id")
        result = await self.db.execute(query, {"id": document_id})
        await self.db.commit()
        return result.rowcount > 0

    async def search(self, user_id: int, query: str) -> List[Document]:
        result = await self.db.execute(
            text("""
                SELECT * FROM documents
                WHERE user_id = :user_id AND
                (title LIKE :query OR content LIKE :query)
            """),
            {
                "user_id": user_id,
                "query": f"%{query}%"
            }
        )
        documents = result.fetchall()
        return [
            Document(
                id=doc.id,
                title=doc.title,
                content=doc.content,
                user_id=doc.user_id
            ) for doc in documents
        ]