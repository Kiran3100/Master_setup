# Authentication logic
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from datetime import timedelta

from ..models.user import User
from ..schemas.user import AdminResponse
from ..schemas.token import LoginRequest, TokenResponse
from ..schemas.enums import UserStatus
from ..repositories.user_repository import UserRepository
from ..core.security import verify_password, create_access_token
from ..core.config import settings

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def login(self, login_data: LoginRequest) -> TokenResponse:
        """Login user and return access token"""
        user = self.authenticate_user(login_data.email, login_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Account is {user.status.value}. Please contact administrator."
            )
        
        access_token = create_access_token(
            data={"sub": user.email, "role": user.role.value}
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=AdminResponse.from_orm(user)
        )