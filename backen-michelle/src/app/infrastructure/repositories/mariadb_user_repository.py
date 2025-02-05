from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.application.interfaces.repositories import IUserRepository
from app.domain.models.user import User
from app.domain.schemas.user import UserCreate, UserUpdate, UserInDB

class MariaDBUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_data: UserCreate) -> UserInDB:
        user = User(**user_data.dict(exclude={'password'}))
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return UserInDB.from_orm(user)

    async def get_by_id(self, user_id: int) -> UserInDB:
        result = await self.session.execute(select(User).filter(User.id == user_id))
        user = result.scalar_one_or_none()
        return UserInDB.from_orm(user) if user else None

    async def get_by_email(self, email: str) -> UserInDB:
        result = await self.session.execute(select(User).filter(User.email == email))
        user = result.scalar_one_or_none()
        return UserInDB.from_orm(user) if user else None

    async def get_by_username(self, username: str) -> UserInDB:
        result = await self.session.execute(select(User).filter(User.username == username))
        user = result.scalar_one_or_none()
        return UserInDB.from_orm(user) if user else None

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserInDB]:
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