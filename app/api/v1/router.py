# Aggregates all v1 routes
from fastapi import APIRouter
from .endpoints import auth, superadmin, health, files

api_router = APIRouter()

# Authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Superadmin routes
api_router.include_router(superadmin.router, prefix="/superadmin", tags=["Superadmin"])

# File upload routes
api_router.include_router(files.router, prefix="/upload", tags=["File Upload"])

# Health check
api_router.include_router(health.router, prefix="/health", tags=["System"])