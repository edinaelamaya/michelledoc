from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.application.services.auth_service import AuthService
from app.domain.schemas.user import UserCreate, UserResponse
from app.infrastructure.api.dependencies.auth import get_auth_service, get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user = await auth_service.register_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = auth_service.create_access_token(user)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user = Depends(get_current_user)):
    return current_user