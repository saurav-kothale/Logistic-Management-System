import DateTime
from datetime import datetime
from database.database import Base
from sqlalchemy import Boolean, Column, Integer, Date, String,DateTime

class InventoryDB(Base):
    __tablename__ = "inventory"
    invoice_number = Column(Integer, primary_key=True)
    invoice_amount = Column(Integer)
    invoice_date = Column(Date)
    inventory_paydate = Column(Date)
    vender = Column(String)
    invoice_image_id = Column(String)
    created_at = Column(DateTime, default= datetime.now)
    updated_at = Column(DateTime, default = datetime.now)
    is_deleted = Column(Boolean, default=False)