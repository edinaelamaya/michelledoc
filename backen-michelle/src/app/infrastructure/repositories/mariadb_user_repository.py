from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.application.interfaces.repositories import IUserRepository
from app.domain.models.user import User
from app.domain.schemas.user import UserCreate, UserUpdate, UserInDB
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)

class MariaDBUserRepository(IUserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: dict) -> UserInDB:
        query = text("""
            INSERT INTO users (username, email, password)
            VALUES (:username, :email, :password)
        """)
        
        result = await self.db.execute(
            query,
            {
                "username": user_data["username"],
                "email": user_data["email"],
                "password": user_data["password"]
            }
        )
        await self.db.commit()
        
        # Obtener el ID del usuario insertado
        user_id = result.lastrowid
        
        # Crear y retornar el objeto UserInDB
        return UserInDB(
            id=user_id,
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"]
        )

    async def get_by_id(self, user_id: int) -> UserInDB:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.scalar_one_or_none()
        return UserInDB.from_orm(user) if user else None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_by_email(self, email: str) -> UserInDB | None:
        try:
            query = text("SELECT * FROM users WHERE email = :email")
            result = await self.db.execute(query, {"email": email})
            user = result.fetchone()
            if user:
                user_dict = dict(zip(user.keys(), user))
                return UserInDB(**user_dict)
            return None
        except Exception as e:
            logger.error(f"Error en get_by_email: {str(e)}")
            raise

    async def get_by_username(self, username: str) -> UserInDB | None:
        query = text("SELECT id, username, email, password FROM users WHERE username = :username")
        result = await self.db.execute(query, {"username": username})
        row = result.fetchone()
        if row:
            # Convertir el resultado a diccionario
            user_dict = {
                "id": row[0],
                "username": row[1],
                "email": row[2],
                "password": row[3]
            }
            return UserInDB(**user_dict)
        return None

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserInDB]:
        user = await self.get_by_id(user_id)
        if not user:
            return None
            
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
            
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
            
        await self.db.delete(user)
        await self.db.commit()
        return True