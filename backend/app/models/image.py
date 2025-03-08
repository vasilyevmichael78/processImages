from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    original_path = Column(String, nullable=False)
    thumbnail_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(tz=None))

    versions = relationship("ImageVersion", back_populates="image", cascade="all, delete")

class ImageVersion(Base):
    __tablename__ = "image_versions"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    version_id = Column(String, nullable=False, index=True)
    processed_path = Column(String, nullable=False)
    processed_thumbnail_path = Column(String, nullable=False)  # New field
    created_at = Column(DateTime, default=datetime.now(tz=None))

    image = relationship("Image", back_populates="versions")