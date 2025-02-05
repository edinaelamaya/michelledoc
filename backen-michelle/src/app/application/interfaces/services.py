from abc import ABC, abstractmethod
from typing import Optional
from app.domain.schemas.user import UserCreate, UserInDB
from app.domain.schemas.document import DocumentCreate, DocumentInDB

class IAuthService(ABC):
    @abstractmethod
    async def register_user(self, user_data: UserCreate) -> UserInDB:
        pass

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        pass

    @abstractmethod
    async def create_access_token(self, user: UserInDB) -> str:
        pass

    @abstractmethod
    async def verify_token(self, token: str) -> Optional[UserInDB]:
        pass

class IVoiceService(ABC):
    @abstractmethod
    async def process_command(self, audio_data: bytes, user_id: int) -> dict:
        pass

    @abstractmethod
    async def transcribe_audio(self, audio_data: bytes) -> str:
        pass

    @abstractmethod
    async def verify_voice(self, audio_data: bytes, user_id: int) -> bool:
        pass

class IPasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

class ITokenService(ABC):
    @abstractmethod
    def create_token(self, data: dict) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> Optional[dict]:
        pass

class IFileStorage(ABC):
    @abstractmethod
    async def save_file(self, file_data: bytes, filename: str) -> str:
        pass

    @abstractmethod
    async def get_file(self, filename: str) -> bytes:
        pass

class IAIService(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        pass

    @abstractmethod
    async def analyze_sentiment(self, text: str) -> dict:
        pass

    @abstractmethod
    async def summarize_text(self, text: str, max_length: int = 200) -> str:
        pass