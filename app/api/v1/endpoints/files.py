from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pathlib import Path
from datetime import datetime

from ....core.config import settings
from ..deps import get_current_user
from ....models.user import User

router = APIRouter()

# Create upload directory
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload profile image
    
    - Maximum file size: 4MB
    - Allowed formats: JPEG, PNG, GIF
    """
    # Read file content
    contents = await file.read()
    
    # Validate file size
    if len(contents) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 4MB limit"
        )
    
    # Validate file type
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files (JPEG, PNG, GIF) are allowed"
        )
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{current_user.id}_{int(datetime.utcnow().timestamp())}.{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Return file URL
    file_url = f"/{settings.UPLOAD_DIR}/{unique_filename}"
    return {
        "file_url": file_url,
        "filename": unique_filename,
        "message": "File uploaded successfully"
    }