from sqlalchemy import Column, ForeignKey, Integer, String
from database.database import Base

class ProductDB(Base):
    __tablename__ = "product"
    product_id = Column(String, primary_key=True)
    product_name = Column(String)
    category = Column(String)
    sub_category = Column(String)
    quantity = Column(Integer)
    size = Column(String)
    city = Column(String)
    invoice = Column(Integer, ForeignKey("inventory.invoice_number"))