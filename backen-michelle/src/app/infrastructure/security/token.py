from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.application.interfaces.services import ITokenService
from app.infrastructure.config.settings import get_settings

settings = get_settings()

class TokenService(ITokenService):
    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            return payload
        except JWTError:
            return None 