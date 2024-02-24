from pydantic import BaseModel
from fastapi import UploadFile, Form

class SuratZomatoStructure2(BaseModel):
    zomato_first_order_start: int = 1 
    zomato_first_order_end: int = 29
    zomato_first_order_amount: int = 30
    zomato_order_greter_than: int = 30
    zomato_second_order_amount: int = 35
    vahicle_charges_order_fulltime : int = 20
    vahicle_charges_fulltime : int = 100
    vahicle_charges_order_partime: int = 12
    vahicle_charges_partime: int = 70
    bonus_order_fulltime: int = 700
    bonus_amount_fulltime: int = 1000
    bonus_order_partime: int = 400
    bonus_amount_partime: int = 500

    class Config:
        from_attributes = True
