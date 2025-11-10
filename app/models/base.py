from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, text
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    """Base model with common fields for all models"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=datetime.utcnow
    )
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}