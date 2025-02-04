from abc import ABC, abstractmethod
from typing import Optional

class IPasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

class ITokenService(ABC):
    @abstractmethod
    def create_token(self, data: dict, expires_delta: Optional[int] = None) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> Optional[dict]:
        pass

    @abstractmethod
    def get_token_payload(self, token: str) -> dict:
        pass