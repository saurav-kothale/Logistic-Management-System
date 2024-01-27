from sqlalchemy import Column, String, DateTime
from database.database import Base

class FileInfo(Base):
    __tablename__ = "fileinfo"
    file_key = Column(String, primary_key=True)
    file_name = Column(String)
    file_type = Column(String)
    created_at = Column(DateTime)
    