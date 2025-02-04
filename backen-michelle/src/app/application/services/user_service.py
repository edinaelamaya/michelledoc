from typing import Optional
from app.application.interfaces.repositories import IUserRepository
from app.domain.schemas.user import UserUpdate, UserInDB

class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def get_user(self, user_id: int) -> Optional[UserInDB]:
        return await self.user_repository.get_by_id(user_id)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserInDB]:
        current_user = await self.user_repository.get_by_id(user_id)
        if not current_user:
            raise ValueError("User not found")
            
        if user_data.email and user_data.email != current_user.email:
            if await self.user_repository.get_by_email(user_data.email):
                raise ValueError("Email already registered")
                
        if user_data.username and user_data.username != current_user.username:
            if await self.user_repository.get_by_username(user_data.username):
                raise ValueError("Username already taken")
                
        return await self.user_repository.update(user_id, user_data)

    async def delete_user(self, user_id: int) -> bool:
        return await self.user_repository.delete(user_id)