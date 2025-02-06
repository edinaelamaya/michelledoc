from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.application.interfaces.repositories import IUserRepository
from app.application.interfaces.services import IPasswordHasher, ITokenService
from app.domain.schemas.user import UserCreate, UserInDB, UserLogin
from app.infrastructure.config.settings import get_settings
from app.scripts.init_db import create_database

settings = get_settings()

class AuthService:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def register_user(self, user_data: UserCreate) -> UserInDB:
        # Verificar si el usuario ya existe
        if await self.user_repository.get_by_email(user_data.email):
            raise ValueError("Email already registered")
        if await self.user_repository.get_by_username(user_data.username):
            raise ValueError("Username already taken")
        
        # Preparar datos del usuario
        user_dict = {
            "username": user_data.username,
            "email": user_data.email,
            "password": user_data.password
        }

        # Crear usuario
        return await self.user_repository.create(user_dict)

    async def authenticate_user(self, user_data: UserLogin) -> Optional[UserInDB]:
        user = await self.user_repository.get_by_username(user_data.username)
        if not user:
            raise ValueError("Usuario no encontrado")
        if user_data.password != user.password:
            raise ValueError("Contraseña incorrecta")
        return user

    def create_access_token(self, user: UserInDB) -> str:
        data = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email
        }
        return self.token_service.create_token(data)

    async def verify_token(self, token: str) -> Optional[UserInDB]:
        payload = self.token_service.verify_token(token)
        if not payload:
            return None
        user_id = int(payload.get("sub"))
        return await self.user_repository.get_by_id(user_id)