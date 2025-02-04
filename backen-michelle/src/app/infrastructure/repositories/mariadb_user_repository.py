from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.user import User
from app.domain.schemas.user import UserCreate, UserUpdate
from app.domain.repositories.user_repository import UserRepository

class MariaDBUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserCreate) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).filter(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).filter(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).filter(User.username == username)
        )
        return result.scalar_one_or_none()

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if not user:
            return None
            
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
            
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
            
        await self.session.delete(user)
        await self.session.commit()
        return True