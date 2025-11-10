from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....core.database import get_db
from ....schemas.user import AdminCreateRequest, AdminUpdateRequest, AdminResponse
from ....services.admin_service import AdminService
from ..deps import get_current_superadmin
from ....models.user import User

router = APIRouter()

@router.post("/admins", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def create_admin(
    admin_data: AdminCreateRequest,
    db: Session = Depends(get_db),
    current_superadmin: User = Depends(get_current_superadmin)
):
    """
    Create a new admin account (Superadmin only)
    
    This endpoint allows superadmin to create admin accounts with company details.
    All fields marked with * in the UI are required.
    """
    admin_service = AdminService(db)
    return admin_service.create_admin(admin_data, current_superadmin.id)

@router.get("/admins", response_model=List[AdminResponse])
def list_admins(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_superadmin: User = Depends(get_current_superadmin)
):
    """List all admin accounts (Superadmin only)"""
    admin_service = AdminService(db)
    return admin_service.get_all_admins(skip, limit)

@router.get("/admins/{admin_id}", response_model=AdminResponse)
def get_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_superadmin: User = Depends(get_current_superadmin)
):
    """Get specific admin details (Superadmin only)"""
    admin_service = AdminService(db)
    return admin_service.get_admin_by_id(admin_id)

@router.put("/admins/{admin_id}", response_model=AdminResponse)
def update_admin(
    admin_id: int,
    admin_data: AdminUpdateRequest,
    db: Session = Depends(get_db),
    current_superadmin: User = Depends(get_current_superadmin)
):
    """Update admin account (Superadmin only)"""
    admin_service = AdminService(db)
    return admin_service.update_admin(admin_id, admin_data)

@router.delete("/admins/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_superadmin: User = Depends(get_current_superadmin)
):
    """Delete admin account (Superadmin only)"""
    admin_service = AdminService(db)
    admin_service.delete_admin(admin_id)
    return None