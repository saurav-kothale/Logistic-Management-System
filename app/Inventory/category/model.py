from database.database import Base
from sqlalchemy import Column, String
import uuid


class CategoryDB(Base):
    __tablename__ =  "category"
    category_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    category_name = Column(String, unique=True)
    bike_category = Column(String)
    size = Column(String)
    color = Column(String)
    city = Column(String)
    