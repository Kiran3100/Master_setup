from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Index, text
from datetime import datetime
from .base import Base
from ..schemas.enums import UserRole, UserStatus

class User(Base):
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Basic Information
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Role and Status - FIXED: Don't create enum types automatically
    role = Column(
        SQLEnum(UserRole, native_enum=False, create_constraint=False), 
        nullable=False, 
        default=UserRole.USER
    )
    status = Column(
        SQLEnum(UserStatus, native_enum=False, create_constraint=False), 
        nullable=False, 
        default=UserStatus.ACTIVE
    )
    
    # Company/Admin specific fields
    account_url = Column(String(255), nullable=True)
    phone_number = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    address = Column(String(500), nullable=True)
    plan_name = Column(String(100), nullable=True)
    plan_type = Column(String(100), nullable=True)
    currency = Column(String(10), nullable=True, default="USD")
    language = Column(String(50), nullable=True, default="English")
    profile_image = Column(String(500), nullable=True)
    
    # Audit fields
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=text('CURRENT_TIMESTAMP')
    )
    created_by = Column(Integer, nullable=True)
    
    # Indexes for better query performance
    __table_args__ = (
        Index('ix_users_email_status', 'email', 'status'),
        Index('ix_users_role_status', 'role', 'status'),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"