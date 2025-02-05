from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.application.services.document_service import DocumentService
from app.domain.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.infrastructure.api.dependencies.auth import get_current_user
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.mariadb_document_repository import MariaDBDocumentRepository

router = APIRouter()

@router.post("/", response_model=DocumentResponse)
async def create_document(
    document: DocumentCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    document_repository = MariaDBDocumentRepository(db)
    document_service = DocumentService(document_repository)
    return await document_service.create_document(current_user["id"], document)

@router.get("/", response_model=List[DocumentResponse])
async def get_user_documents(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    document_repository = MariaDBDocumentRepository(db)
    document_service = DocumentService(document_repository)
    return await document_service.get_user_documents(current_user["id"])

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    document_repository = MariaDBDocumentRepository(db)
    document_service = DocumentService(document_repository)
    try:
        return await document_service.get_document(document_id, current_user["id"])
    except ValueError:
        raise HTTPException(status_code=404, detail="Document not found")

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: int,
    document_data: DocumentUpdate,
    current_user = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service)
):
    document = await document_service.get_document(document_id)
    if not document or document.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return await document_service.update_document(document_id, document_data)

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service)
):
    document = await document_service.get_document(document_id)
    if not document or document.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Document not found")
    
    await document_service.delete_document(document_id)
    return {"message": "Document deleted successfully"}