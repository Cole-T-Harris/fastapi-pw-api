from sqlalchemy import Column, Integer, String

from .database import Base

#Database Models
class Thumbnail(Base):
    __tablename__ = "thumbnails"

    id = Column(Integer, primary_key=True)
    branch = Column(String, unique=True, index=True)
    url = Column(String)