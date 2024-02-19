from pydantic import BaseModel
from fastapi import UploadFile, Form

class AhmedabadSwiggySchema(BaseModel):
    file_id: str
    file_name : str
    swiggy_first_order_start: int = 1 
    swiggy_first_order_end: int = 29
    swiggy_first_order_amount: int = 30
    swiggy_order_greter_than: int = 30
    swiggy_second_order_amount: int = 35

    class Config:
        from_attributes = True
