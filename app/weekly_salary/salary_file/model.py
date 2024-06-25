from database.database import Base
from sqlalchemy import INTEGER, Column, String, Integer, Date

class WeeklySalaryData(Base):
    __tablename__ = "weekly_salary_data"
    ID = Column(Integer, primary_key=True, index=True)
    FILE_KEY = Column(String)
    FILE_NAME = Column(String)
    CITY_NAME = Column(String)
    CLIENT_NAME = Column(String)
    DATE = Column(String)
    JOINING_DATE = Column(Date)
    COMPANY = Column(String) 
    SALARY_DAY = Column(String)
    STATUS = Column(String)
    EXIT_DATE = Column(String, nullable=True) ## new column add
    WEEK_NAME = Column(String)
    PHONE_NUMBER = Column(String) ## Add the 10 for validation
    AADHAR_NUMBER = Column(String)
    DRIVER_ID = Column(String)
    DRIVER_NAME = Column(String)
    DESIGNATION_NAME = Column(String)   ## replace with the week_type
    DONE_PARCEL_ORDERS = Column(Integer)
    DONE_DOCUMENT_ORDERS = Column(Integer)
    DONE_BIKER_ORDERS = Column(Integer)
    DONE_MICRO_ORDERS = Column(Integer)
    RAIN_ORDER = Column(Integer)
    IGCC_AMOUNT = Column(Integer)
    BAD_ORDER = Column(Integer)
    REJECTION = Column(Integer)
    ATTENDANCE = Column(Integer)
    CASH_COLLECTED = Column(Integer)
    CASH_DEPOSITED = Column(Integer)
    PAYMENT_SENT_ONLINE = Column(Integer)
    POCKET_WITHDRAWAL = Column(Integer)
    OTHER_PANALTY = Column(Integer)
    FINAL_AMOUNT = Column(Integer)

# API response data for fatak_pay 
#     MONTH_NAME = Column(String)
#     WEEK_NAME = Column(String)
#     STATUS = Column(String) ## update with EMPLOYEE_STATUS
#     COMPANY = Column(String) 
#     SALARY_DATE = Column(Date)
#     JOINING_DATE = Column(Date)
#     CITY_NAME = Column(String)
#     CLIENT_NAME = Column(String)
#     EXIT_DATE = Column(Date)
#     AADHAR_NUMBER = Column(String(12))
#     PHONE_NUMBER = Column(String(10)) ## Add the 10 for validation
#     DESIGNATION_NAME = Column(String)
#     DRIVER_ID = Column(String)
#     DRIVER_NAME = Column(String)
#     FINAL_AMOUNT = Column(Integer)



