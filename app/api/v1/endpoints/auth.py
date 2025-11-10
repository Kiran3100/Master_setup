from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....schemas.token import LoginRequest, TokenResponse
from ....schemas.user import AdminResponse
from ....services.auth_service import AuthService
from ..deps import get_current_user
from ....models.user import User

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login endpoint - Returns JWT Bearer token
    
    **Request Body:**
    ```json
    {
        "email": "superadmin@levitica.com",
        "password": "Admin@123"
    }
    ```
    
    **Response:**
    ```json
    {
        "access_token": "eyJhbGci...",
        "token_type": "bearer",
        "user": {...}
    }
    ```
    
    Use the access_token in subsequent requests:
    ```
    Authorization: Bearer <access_token>
    ```
    """
    try:
        auth_service = AuthService(db)
        return auth_service.login(login_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/me", response_model=AdminResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Requires: Bearer token in Authorization header
    """
    return current_user

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout endpoint
    
    Note: JWT tokens are stateless, actual logout happens client-side
    This endpoint is for logging/tracking purposes
    
    Requires: Bearer token in Authorization header
    """
    return {
        "message": "Successfully logged out",
        "user": current_user.email
    }

@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Refresh access token
    
    Returns a new token for the authenticated user
    
    Requires: Bearer token in Authorization header
    """
    from ....core.security import create_access_token
    
    access_token = create_access_token(
        data={"sub": current_user.email, "role": current_user.role.value}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": AdminResponse.model_validate(current_user)
    }