from pydantic import BaseModel, EmailStr
from .user import AdminResponse

class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "superadmin@levitica.com",
                    "password": "Admin@123"
                }
            ]
        }
    }

class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    user: AdminResponse
    
    model_config = {
        "from_attributes": True
    }

class TokenData(BaseModel):
    """Token data schema"""
    email: str | None = None
    role: str | None = None