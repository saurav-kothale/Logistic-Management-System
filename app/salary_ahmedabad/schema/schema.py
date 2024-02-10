from pydantic import BaseModel
from fastapi import UploadFile, Form

class AhmedabadZomatoSchema(BaseModel):
    zomato_first_order_start: int = 1 
    zomato_first_order_end: int = 29
    zomato_first_order_amount: int = 30
    zomato_order_greter_than: int = 30
    zomato_second_order_amount: int = 35

    class Config:
        from_attributes = True