from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from .enums import UserRole, UserStatus

class AdminCreateRequest(BaseModel):
    """Schema for creating admin"""
    name: str = Field(..., min_length=1, max_length=255, description="Company/Admin name")
    email: EmailStr = Field(..., description="Email address")
    account_url: Optional[str] = Field(None, max_length=255, description="Account URL")
    phone_number: str = Field(..., min_length=1, description="Phone number")
    website: Optional[str] = Field(None, max_length=255, description="Website URL")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    confirm_password: str = Field(..., description="Confirm password")
    address: Optional[str] = Field(None, max_length=500, description="Address")
    plan_name: str = Field(..., description="Plan name")
    plan_type: str = Field(..., description="Plan type")
    currency: str = Field(default="USD", description="Currency")
    language: str = Field(default="English", description="Language")
    status: UserStatus = Field(default=UserStatus.ACTIVE, description="Account status")
    profile_image: Optional[str] = Field(None, description="Profile image URL/path")
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Phone number is required')
        return v

class AdminUpdateRequest(BaseModel):
    """Schema for updating admin without password validation"""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    account_url: Optional[str] = Field(None, max_length=255)
    phone_number: str = Field(..., min_length=1)
    website: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=8, description="Leave empty to keep current password")
    address: Optional[str] = Field(None, max_length=500)
    plan_name: str
    plan_type: str
    currency: str = Field(default="USD")
    language: str = Field(default="English")
    status: UserStatus
    profile_image: Optional[str] = None

class AdminResponse(BaseModel):
    """Admin response schema"""
    id: int
    name: str
    email: str
    role: UserRole
    status: UserStatus
    account_url: Optional[str] = None
    phone_number: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    plan_name: Optional[str] = None
    plan_type: Optional[str] = None
    currency: Optional[str] = None
    language: Optional[str] = None
    profile_image: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    """Basic user response without sensitive data"""
    id: int
    name: str
    email: str
    role: UserRole
    status: UserStatus
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)