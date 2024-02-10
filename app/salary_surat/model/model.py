from sqlalchemy import Column, DateTime, String
from database.database import Base


class SalaryFile(Base):
    __tablename__ = "salaryinfo"
    filekey = Column(String, primary_key=True)
    file_name = Column(String)
    file_type = Column(String)
    created_at = Column(DateTime)
