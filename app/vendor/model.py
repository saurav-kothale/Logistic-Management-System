
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from pydantic import Json
from sqlalchemy import Column, JSON, String, ARRAY
from database.database import Base


class Vendor(Base):
    __tablename__ = "vendor"
    vendor_id = Column(UUID(as_uuid = True), primary_key=True, default=uuid4)
    vendor_name = Column(String)
    working_city = Column(String)
    register_address = Column(String)
    GST_number = Column(String)
    HSN_code = Column(String)
    PAN_number = Column(String)
    chapter_head = Column(String)
    email = Column(ARRAY(String))
    mobile_number = Column(ARRAY(String))        
    bank_details = Column(JSON)
    document = Column(JSON)
