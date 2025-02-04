from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    title: str
    content: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class DocumentInDB(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True

class DocumentResponse(DocumentInDB):
    pass