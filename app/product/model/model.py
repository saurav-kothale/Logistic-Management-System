from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import Relationship
from database.database import Base
import uuid

class ProductDB(Base):
    __tablename__ = "product"
    product_id = Column(String, primary_key=True, default=(uuid.uuid4()))
    product_name = Column(String)
    category = Column(String)
    bike_category = Column(String)
    quantity = Column(Integer)
    size = Column(String)
    city = Column(String)
    color = Column(String)
    user = Column(JSON)
    HSN_code = Column(String)
    GST = Column(String)
    unit = Column(String)
    invoice_id = Column(String, ForeignKey("inventory.invoice_id"))
    invoice = Relationship("InventoryDB", back_populates="products")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)