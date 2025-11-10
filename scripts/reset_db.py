"""
Reset database - Drop all tables and recreate
⚠️ WARNING: This will delete all data!
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.models.base import Base
from app.core.database import engine
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_database():
    """Drop all tables and recreate"""
    logger.warning("=" * 70)
    logger.warning("⚠️  WARNING: Database Reset")
    logger.warning("=" * 70)
    logger.warning(f"Database: {settings.DB_NAME}")
    logger.warning(f"Host: {settings.DB_HOST}:{settings.DB_PORT}")
    logger.warning("This will DELETE ALL DATA!")
    logger.warning("=" * 70)
    
    # Confirmation
    print("\nType 'yes' to confirm reset (or press Ctrl+C to cancel): ", end='')
    confirm = input().strip().lower()
    
    if confirm not in ['yes', 'y']:
        logger.info("Operation cancelled")
        return False
    
    try:
        logger.info("\nDropping all tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✓ All tables dropped")
        
        logger.info("\nCreating fresh tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Tables created")
        
        logger.info("\n" + "=" * 70)
        logger.info("✓ Database reset complete!")
        logger.info("=" * 70)
        logger.info("\nNext step: Create superadmin")
        logger.info("  python scripts/init_db.py")
        logger.info("=" * 70)
        
        return True
    except Exception as e:
        logger.error(f"✗ Reset failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = reset_database()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n\nOperation cancelled by user")
        sys.exit(1)