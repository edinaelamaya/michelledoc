from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.services.auth_service import AuthService
from app.application.services.document_service import DocumentService
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.mariadb_user_repository import MariaDBUserRepository
from app.infrastructure.repositories.mariadb_document_repository import MariaDBDocumentRepository
# from app.infrastructure.security.password import PasswordHasher
# from app.infrastructure.security.token import TokenService

async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    user_repository = MariaDBUserRepository(db)
    # password_hasher = PasswordHasher()
    # token_service = TokenService()
    return AuthService(user_repository, 'kskjs', 'jshshshs')

async def get_document_service(db: AsyncSession = Depends(get_db)) -> DocumentService:
    document_repository = MariaDBDocumentRepository(db)
    return DocumentService(document_repository)

async def get_current_user(
    auth_service: AuthService = Depends(get_auth_service),
    token: str = Depends(security)
):
    user = await auth_service.verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return user