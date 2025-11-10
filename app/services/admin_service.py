from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from ..models.user import User
from ..schemas.user import AdminCreateRequest, AdminUpdateRequest, AdminResponse
from ..schemas.enums import UserRole
from ..repositories.user_repository import UserRepository
from ..core.security import get_password_hash

class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def create_admin(self, admin_data: AdminCreateRequest, created_by_id: int) -> User:
        """Create a new admin account"""
        # Check if email already exists
        if self.user_repo.email_exists(admin_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Prepare admin data
        admin_dict = admin_data.model_dump(exclude={'password', 'confirm_password'})
        admin_dict['hashed_password'] = get_password_hash(admin_data.password)
        admin_dict['role'] = UserRole.ADMIN
        admin_dict['created_by'] = created_by_id
        
        # Create admin
        new_admin = self.user_repo.create(admin_dict)
        return new_admin
    
    def get_all_admins(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all admin accounts"""
        return self.user_repo.get_by_role(UserRole.ADMIN, skip, limit)
    
    def get_admin_by_id(self, admin_id: int) -> User:
        """Get specific admin by ID"""
        admin = self.user_repo.get(admin_id)
        if not admin or admin.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin not found"
            )
        return admin
    
    def update_admin(self, admin_id: int, admin_data: AdminUpdateRequest) -> User:
        """Update admin account"""
        admin = self.get_admin_by_id(admin_id)
        
        # Check if email is being changed and if it's already taken
        if admin_data.email != admin.email:
            if self.user_repo.email_exists(admin_data.email, exclude_id=admin_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Prepare update data
        update_dict = admin_data.model_dump(exclude={'password'})
        
        # Update password only if provided
        if admin_data.password:
            update_dict['hashed_password'] = get_password_hash(admin_data.password)
        
        # Update admin
        updated_admin = self.user_repo.update(admin, update_dict)
        return updated_admin
    
    def delete_admin(self, admin_id: int) -> None:
        """Delete admin account"""
        admin = self.get_admin_by_id(admin_id)
        self.user_repo.delete(admin_id)