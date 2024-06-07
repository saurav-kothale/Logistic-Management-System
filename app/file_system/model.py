from sqlalchemy import Boolean, Column, String, DateTime, Integer
from database.database import Base

class FileInfo(Base):
    __tablename__ = "fileinfo"
    filekey = Column(String, primary_key=True)
    file_name = Column(String)
    file_type = Column(String)
    weekly = Column(Boolean)
    created_at = Column(DateTime)


class FileRecord(Base):
    __tablename__ = "rawfile_record"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    CITY_NAME = Column(String)
    CLIENT_NAME = Column(String)
    DATE = Column(String)
    AADHAR_NUMBER = Column(String(12))
    DRIVER_ID = Column(String)
    DRIVER_NAME = Column(String)
    WORK_TYPE = Column(String)
    LOG_IN_HR = Column(String)
    PICKUP_DOCUMENT_ORDERS = Column(String)
    DONE_DOCUMENT_ORDERS = Column(Integer)
    PICKUP_PARCEL_ORDERS = Column(Integer)
    DONE_PARCEL_ORDERS = Column(Integer)
    PICKUP_BIKER_ORDERS = Column(Integer)
    DONE_BIKER_ORDERS = Column(Integer)
    PICKUP_MICRO_ORDERS = Column(Integer)
    DONE_MICRO_ORDERS = Column(Integer)
    CUSTOMER_TIP = Column(Integer)
    RAIN_ORDER = Column(Integer)
    IGCC_AMOUNT = Column(Integer)
    BAD_ORDER = Column(Integer)
    REJECTION = Column(Integer)
    ATTENDANCE = Column(Integer)
    CASH_COLLECTION = Column(Integer)
    CASH_DEPOSIT = Column(Integer)
    PAYMENT_SENT_ONLINE = Column(Integer)



    