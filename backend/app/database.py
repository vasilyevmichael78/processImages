from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import dotenv
import logging

logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/image_db")
logging.info(f"DATABASE_URL: {DATABASE_URL}")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """Create all tables if they don't exist."""
    from app.models.image import Image, ImageVersion  # Import models
    Base.metadata.create_all(bind=engine)