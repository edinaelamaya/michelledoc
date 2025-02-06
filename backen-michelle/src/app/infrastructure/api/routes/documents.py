from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.domain.schemas.document import DocumentCreate, DocumentUpdate, DocumentInDB
from app.application.services.document_service import DocumentService
from app.infrastructure.api.dependencies.services import get_document_service

router = APIRouter()

@router.post("/", response_model=DocumentInDB)
async def create_document(
    document: DocumentCreate,
    document_service: DocumentService = Depends(get_document_service)
):
    try:
        # Por ahora usaremos un user_id fijo para pruebas
        user_id = 1
        return await document_service.create_document(user_id, document)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[DocumentInDB])
async def get_documents(
    document_service: DocumentService = Depends(get_document_service)
):
    try:
        # Por ahora usaremos un user_id fijo para pruebas
        user_id = 1
        return await document_service.get_user_documents(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/{document_id}", response_model=DocumentInDB)
async def get_document(
    document_id: int,
    document_service: DocumentService = Depends(get_document_service)
):
    try:
        # Por ahora usaremos un user_id fijo para pruebas
        user_id = 1
        return await document_service.get_document(document_id, user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.put("/{document_id}", response_model=DocumentInDB)
async def update_document(
    document_id: int,
    document: DocumentUpdate,
    document_service: DocumentService = Depends(get_document_service)
):
    try:
        return await document_service.update_document(document_id, document)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    document_service: DocumentService = Depends(get_document_service)
):
    try:
        success = await document_service.delete_document(document_id)
        if success:
            return {"message": "Document deleted successfully"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )