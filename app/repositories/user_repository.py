from sqlalchemy.orm import Session
from typing import Optional, List
from ..models.user import User
from ..schemas.enums import UserRole, UserStatus
from .base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_role(self, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role"""
        return self.db.query(User).filter(User.role == role).offset(skip).limit(limit).all()
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all active users"""
        return self.db.query(User).filter(User.status == UserStatus.ACTIVE).offset(skip).limit(limit).all()
    
    def email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """Check if email exists (optionally excluding a specific user ID)"""
        query = self.db.query(User).filter(User.email == email)
        if exclude_id:
            query = query.filter(User.id != exclude_id)
        return query.first() is not None