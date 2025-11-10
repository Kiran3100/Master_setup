"""
Test script to verify all required modules are installed
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    print("=" * 60)
    
    modules = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'sqlalchemy': 'SQLAlchemy',
        'psycopg2': 'psycopg2-binary',
        'alembic': 'Alembic',
        'pydantic': 'Pydantic',
        'pydantic_settings': 'Pydantic Settings',
        'jose': 'Python-JOSE',
        'passlib': 'Passlib',
    }
    
    failed = []
    
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"✓ {name:20} - OK")
        except ImportError as e:
            print(f"✗ {name:20} - FAILED: {str(e)}")
            failed.append(module)
    
    print("=" * 60)
    
    if failed:
        print("\n⚠️  Some modules are missing!")
        print("\nInstall missing modules:")
        print(f"pip install {' '.join(failed)}")
        return False
    else:
        print("\n✓ All required modules are installed!")
        return True

if __name__ == "__main__":
    success = test_imports()
    
    if success:
        print("\nYou can now run:")
        print("  python scripts/create_db.py")
        print("  python scripts/init_db.py")
    
    sys.exit(0 if success else 1)