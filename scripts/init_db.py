"""
Database initialization script
Creates tables and superadmin account for PostgreSQL
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, ProgrammingError
from app.models.base import Base
from app.models.user import User
from app.schemas.enums import UserRole, UserStatus
from app.core.database import engine, get_db_context
from app.core.security import get_password_hash
from app.core.config import settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)
logger = logging.getLogger(__name__)

def check_db_connection():
    """Check if database connection is working"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False

def create_tables():
    """Create all database tables"""
    try:
        logger.info("Creating database tables...")
        
        # Drop all tables first (only for fresh start)
        # Base.metadata.drop_all(bind=engine)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("✓ Database tables created successfully!")
        
        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            
        if tables:
            logger.info(f"  Tables created: {', '.join(tables)}")
        else:
            logger.warning("  No tables found!")
            
        return True
    except Exception as e:
        logger.error(f"✗ Error creating tables: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_superadmin(db: Session):
    """Create superadmin account if it doesn't exist"""
    try:
        # Check if superadmin already exists
        existing_superadmin = db.query(User).filter(
            User.email == settings.SUPERADMIN_EMAIL
        ).first()
        
        if existing_superadmin:
            logger.info(f"✓ Superadmin already exists: {settings.SUPERADMIN_EMAIL}")
            return existing_superadmin
        
        # Create superadmin
        logger.info("Creating superadmin account...")
        superadmin = User(
            name=settings.SUPERADMIN_NAME,
            email=settings.SUPERADMIN_EMAIL,
            hashed_password=get_password_hash(settings.SUPERADMIN_PASSWORD),
            role=UserRole.SUPERADMIN,
            status=UserStatus.ACTIVE,
            phone_number="+1234567890",
            currency="USD",
            language="English"
        )
        
        db.add(superadmin)
        db.commit()
        db.refresh(superadmin)
        
        logger.info(f"✓ Superadmin created successfully!")
        logger.info(f"  ID: {superadmin.id}")
        logger.info(f"  Email: {settings.SUPERADMIN_EMAIL}")
        logger.info(f"  Password: {settings.SUPERADMIN_PASSWORD}")
        logger.warning("  ⚠️  Please change the default password immediately!")
        
        return superadmin
    
    except IntegrityError as e:
        db.rollback()
        logger.error(f"✗ Error creating superadmin (duplicate?): {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"✗ Unexpected error creating superadmin: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

def init_database():
    """Initialize database with tables and superadmin"""
    logger.info("=" * 70)
    logger.info("LEVITICA HR MANAGEMENT SYSTEM - Database Initialization")
    logger.info("=" * 70)
    
    # Display configuration
    logger.info(f"Database: {settings.DB_NAME}")
    logger.info(f"Host: {settings.DB_HOST}:{settings.DB_PORT}")
    logger.info(f"User: {settings.DB_USER}")
    logger.info("=" * 70)
    
    # Check database connection
    logger.info("Step 1: Checking database connection...")
    if not check_db_connection():
        logger.error("✗ Cannot connect to PostgreSQL database!")
        logger.error("")
        logger.error("Please ensure:")
        logger.error(f"  1. PostgreSQL is running")
        logger.error(f"  2. Database '{settings.DB_NAME}' exists")
        logger.error(f"  3. Credentials in .env are correct")
        logger.error("")
        logger.error("To create database, run:")
        logger.error("  python scripts/create_db.py")
        logger.error("")
        logger.error("Or use Docker:")
        logger.error("  docker-compose -f docker-compose-postgres.yml up -d")
        logger.error("")
        return False
    
    logger.info("✓ Database connection successful")
    logger.info("")
    
    # Create tables
    logger.info("Step 2: Creating database tables...")
    if not create_tables():
        logger.error("✗ Failed to create tables")
        return False
    logger.info("")
    
    # Create superadmin
    logger.info("Step 3: Creating superadmin account...")
    try:
        with get_db_context() as db:
            create_superadmin(db)
    except Exception as e:
        logger.error(f"✗ Failed to create superadmin: {str(e)}")
        return False
    
    logger.info("")
    logger.info("=" * 70)
    logger.info("✓ Database initialization completed successfully!")
    logger.info("=" * 70)
    logger.info("")
    logger.info("Next steps:")
    logger.info("  1. Start application:")
    logger.info("     uvicorn app.main:app --reload")
    logger.info("")
    logger.info("  2. Access API documentation:")
    logger.info("     http://localhost:8000/docs")
    logger.info("")
    logger.info("  3. Login with superadmin:")
    logger.info(f"     Email: {settings.SUPERADMIN_EMAIL}")
    logger.info(f"     Password: {settings.SUPERADMIN_PASSWORD}")
    logger.info("")
    logger.info("=" * 70)
    return True

if __name__ == "__main__":
    try:
        success = init_database()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n\nFatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)