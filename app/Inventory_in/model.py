import DateTime
import uuid
from datetime import datetime, timezone
from database.database import Base
from sqlalchemy import Boolean, Column, Integer, Date, String,DateTime, Uuid, true
from sqlalchemy.orm import Relationship

class InventoryDB(Base):
    __tablename__ = "inventory"
    invoice_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    invoice_number = Column(String)
    invoice_amount = Column(Integer)
    invoice_date = Column(Date)
    inventory_paydate = Column(Date)
    vendor = Column(String)
    invoice_image_id = Column(String)
    created_at = Column(DateTime, default= datetime.now(timezone.utc))
    updated_at = Column(DateTime, default = datetime.now(timezone.utc), onupdate = datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)
    products = Relationship("ProductDB", back_populates="invoice")