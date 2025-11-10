from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from pathlib import Path
from contextlib import asynccontextmanager
import logging

from .core.config import settings
from .core.database import check_db_connection, close_db_connection
from .api.v1.router import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler"""
    # Startup
    logger.info("Starting application...")
    
    if check_db_connection():
        logger.info("✓ Database connection successful")
    else:
        logger.error("✗ Database connection failed")
    
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"✓ Upload directory ready")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    close_db_connection()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    ## HR Management System API
    
    ### 🔐 Authentication
    
    This API uses **Bearer Token (JWT)** authentication.
    
    #### How to Authenticate:
    
    1. **Login:** Call `POST /api/v1/auth/login` with credentials
       ```json
       {
         "email": "superadmin@levitica.com",
         "password": "Admin@123"
       }
       ```
    
    2. **Get Token:** Copy the `access_token` from response
    
    3. **Authorize:** 
       - Click the **Authorize** 🔓 button above
       - Enter your token (just the token, not "Bearer")
       - Click **Authorize**
    
    4. **Test:** All protected endpoints will now work!
    
    #### Default Credentials
    - **Email:** superadmin@levitica.com
    - **Password:** Admin@123
    
    ⚠️ **Change default password after first login!**
    """,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=app.description,
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your Bearer token (without 'Bearer' prefix)"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
upload_path = Path(settings.UPLOAD_DIR)
if upload_path.exists():
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """API Root"""
    return {
        "message": "Welcome to Levitica HR Management API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
        "authentication": "Bearer Token (JWT)",
        "login": "/api/v1/auth/login"
    }

# Health check
@app.get("/health", tags=["System"])
def health_check():
    """Health check"""
    db_status = check_db_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected" if db_status else "disconnected"
    }