from sqlalchemy import Boolean, Column, DateTime, Integer, String
from database.database import Base


class ProductOutDb(Base):
    __tablename__ = "inventory out"
    product_out_id =  Column(String , primary_key=True)
    HSN_code  = Column(String)
    product_name = (Column(String))
    category = Column(String)
    bike_category = Column(String)
    size = Column(String)
    quntity = Column(Integer)
    name = Column(String)
    color = Column(String)
    city = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)