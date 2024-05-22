from database.database import Base
from sqlalchemy import JSON, Column, String, DateTime, Boolean
from datetime import datetime

class ProductCategoryDB(Base):
    __tablename__ = "product category"
    product_id = Column(String, primary_key= True)
    product_name = Column(String)
    HSN_code = Column(String)
    category = Column(String)
    created_at = Column(DateTime, default= datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at = Column(DateTime, default = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), onupdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    is_deleted = Column(Boolean, default=False)
    user = Column(JSON)
    
