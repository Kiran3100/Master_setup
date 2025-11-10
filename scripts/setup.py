"""
Complete database setup script
- Cleans up existing enums
- Creates database (if needed)
- Creates tables
- Creates superadmin
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.models.base import Base
from app.models.user import User
from app.schemas.enums import UserRole, UserStatus
from app.core.database import engine, get_db_context
from app.core.security import get_password_hash
from app.core.config import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    logger.info("Step 1: Checking/Creating database...")
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
        )
        conn.close()
        logger.info(f"✓ Database '{settings.DB_NAME}' exists")
        return True
    except psycopg2.OperationalError:
        logger.info(f"  Database '{settings.DB_NAME}' doesn't exist, creating...")
        try:
            conn = psycopg2.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database='postgres'
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE {settings.DB_NAME}')
            cursor.close()
            conn.close()
            logger.info(f"✓ Database '{settings.DB_NAME}' created successfully")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to create database: {e}")
            return False

def clean_existing_objects():
    """Clean up existing tables and enums"""
    logger.info("\nStep 2: Cleaning existing database objects...")
    try:
        with engine.connect() as conn:
            # Drop users table
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            conn.commit()
            logger.info("✓ Dropped existing users table")
            
            # Drop enum types
            conn.execute(text("DROP TYPE IF EXISTS user_role_enum CASCADE"))
            conn.execute(text("DROP TYPE IF EXISTS user_status_enum CASCADE"))
            conn.commit()
            logger.info("✓ Dropped existing enum types")
            
        return True
    except Exception as e:
        logger.warning(f"⚠️  Cleanup warning: {e}")
        return True  # Continue anyway

def create_tables():
    """Create all database tables"""
    logger.info("\nStep 3: Creating tables...")
    try:
        Base.metadata.create_all(bind=engine)
        
        # Verify tables
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
        
        if tables:
            logger.info(f"✓ Created {len(tables)} table(s): {', '.join(tables)}")
            return True
        else:
            logger.error("✗ No tables created")
            return False
    except Exception as e:
        logger.error(f"✗ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_superadmin():
    """Create superadmin user"""
    logger.info("\nStep 4: Creating superadmin...")
    try:
        with get_db_context() as db:
            # Check if superadmin exists
            existing = db.query(User).filter(
                User.email == settings.SUPERADMIN_EMAIL
            ).first()
            
            if existing:
                logger.info(f"✓ Superadmin already exists: {settings.SUPERADMIN_EMAIL}")
                return True
            
            # Create superadmin
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
            
            logger.info(f"✓ Superadmin created successfully")
            logger.info(f"  Email: {settings.SUPERADMIN_EMAIL}")
            logger.info(f"  Password: {settings.SUPERADMIN_PASSWORD}")
            return True
    except Exception as e:
        logger.error(f"✗ Error creating superadmin: {e}")
        import traceback
        traceback.print_exc()
        return False

def setup():
    """Run complete setup"""
    print("\n" + "=" * 70)
    print("LEVITICA HR - Complete Database Setup")
    print("=" * 70)
    print(f"Database: {settings.DB_NAME}")
    print(f"Host: {settings.DB_HOST}:{settings.DB_PORT}")
    print(f"User: {settings.DB_USER}")
    print("=" * 70)
    print()
    
    # Step 1: Create database
    if not create_database_if_not_exists():
        logger.error("\n✗ Setup failed at database creation")
        return False
    
    # Step 2: Clean existing objects
    clean_existing_objects()
    
    # Step 3: Create tables
    if not create_tables():
        logger.error("\n✗ Setup failed at table creation")
        return False
    
    # Step 4: Create superadmin
    if not create_superadmin():
        logger.error("\n✗ Setup failed at superadmin creation")
        return False
    
    # Success
    print("\n" + "=" * 70)
    print("✓ Setup completed successfully!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Start the application:")
    print("     uvicorn app.main:app --reload")
    print("")
    print("  2. Open your browser:")
    print("     http://localhost:8000/docs")
    print("")
    print("  3. Login with superadmin:")
    print(f"     Email: {settings.SUPERADMIN_EMAIL}")
    print(f"     Password: {settings.SUPERADMIN_PASSWORD}")
    print("")
    print("  ⚠️  Remember to change the default password!")
    print("=" * 70)
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)