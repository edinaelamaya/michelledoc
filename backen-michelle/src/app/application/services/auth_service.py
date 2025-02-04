from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.application.interfaces.repositories import IUserRepository
from app.application.interfaces.security import IPasswordHasher, ITokenService
from app.domain.schemas.user import UserCreate, UserInDB
from app.infrastructure.config import get_settings

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

        # Hashear contraseña
        hashed_password = self.password_hasher.hash_password(user_data.password)
        user_data_dict = user_data.dict()
        user_data_dict["hashed_password"] = hashed_password
        del user_data_dict["password"]

        # Crear usuario
        return await self.user_repository.create(UserCreate(**user_data_dict))

    async def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        user = await self.user_repository.get_by_username(username)
        if not user:
            return None
        if not self.password_hasher.verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, user: UserInDB) -> str:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + expires_delta
        
        to_encode = {
            "sub": str(user.id),
            "username": user.username,
            "exp": expire
        }
        return self.token_service.create_token(to_encode)

    async def verify_token(self, token: str) -> Optional[UserInDB]:
        try:
            payload = self.token_service.verify_token(token)
            user_id = int(payload.get("sub"))
            return await self.user_repository.get_by_id(user_id)
        except JWTError:
            return None