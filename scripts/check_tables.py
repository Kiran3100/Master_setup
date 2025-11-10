"""
Check if database tables exist
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.core.database import engine
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_tables():
    """Check which tables exist in the database"""
    logger.info("=" * 70)
    logger.info("Database Tables Check")
    logger.info("=" * 70)
    logger.info(f"Database: {settings.DB_NAME}")
    logger.info(f"Host: {settings.DB_HOST}:{settings.DB_PORT}")
    logger.info("=" * 70)
    
    try:
        with engine.connect() as conn:
            # Get all tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
            
            if tables:
                logger.info(f"\n✓ Found {len(tables)} table(s):")
                for table in tables:
                    logger.info(f"  - {table}")
                    
                    # Get column count
                    result = conn.execute(text(f"""
                        SELECT COUNT(*) 
                        FROM information_schema.columns 
                        WHERE table_name = '{table}'
                    """))
                    col_count = result.fetchone()[0]
                    
                    # Get row count
                    result = conn.execute(text(f'SELECT COUNT(*) FROM "{table}"'))
                    row_count = result.fetchone()[0]
                    
                    logger.info(f"    Columns: {col_count}, Rows: {row_count}")
            else:
                logger.warning("\n✗ No tables found in database!")
                logger.info("\nTo create tables, run:")
                logger.info("  python scripts/init_db.py")
            
            logger.info("\n" + "=" * 70)
            return len(tables) > 0
            
    except Exception as e:
        logger.error(f"\n✗ Error checking tables: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_tables()
    sys.exit(0 if success else 1)