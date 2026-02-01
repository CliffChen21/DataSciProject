"""
Database Utilities
Handles database connections and operations
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend import config

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """
    Get database session
    Use as context manager or dependency injection
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database tables
    """
    logger.info('Initializing database...')
    Base.metadata.create_all(bind=engine)
    logger.info('Database initialized successfully')
