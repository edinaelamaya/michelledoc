from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from application.services.auth_service import AuthService

security = HTTPBearer()

class AuthMiddleware:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def __call__(self, request: Request, credentials: HTTPAuthorizationCredentials = security):
        if not credentials:
            raise HTTPException(status_code=403, detail="Not authenticated")
        
        token = credentials.credentials
        user = await self.auth_service.verify_token(token)
        
        if not user:
            raise HTTPException(status_code=403, detail="Invalid token or expired")
        
        request.state.user = user
        return user