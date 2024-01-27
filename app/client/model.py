
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from pydantic import Json
from sqlalchemy import Column, JSON, String, ARRAY
from database.database import Base


class Client(Base):
    __tablename__ = "client"
    client_id = Column(UUID(as_uuid = True), primary_key=True, default=uuid4)
    client_name = Column(String)
    client_hub_name = Column(String)
    address = Column(String)
    city = Column(String)
    GST_number = Column(String)
    email = Column(ARRAY(String))
    mobile_number = Column(ARRAY(String))
    HSN_code = Column(String)
    PAN_number = Column(String)
    bank_details = Column(JSON)
    document = Column(JSON)
