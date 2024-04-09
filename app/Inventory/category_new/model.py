from sqlalchemy import Boolean, Column, DateTime, String
from database.database import Base
import uuid

class NewCategoryDb(Base):
    __tablename__ = "new_category"
    category_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    category_name = Column(String, unique=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)