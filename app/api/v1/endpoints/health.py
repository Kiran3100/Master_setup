# Health check endpoints
from fastapi import APIRouter
from ....core.config import settings

router = APIRouter()

@router.get("")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }