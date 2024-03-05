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
    vahicle_charges_order_partime: int = 11
    vahicle_charges_partime: int = 70
    bonus_order_fulltime: int = 630
    bonus_amount_fulltime: int = 1000
    bonus_order_partime: int = 350
    bonus_amount_partime: int = 500
    rejection: int = 2
    rejection_amount : int = 20
    bad_order : int = 2
    bad_order_amount : int = 20

    class Config:
        from_attributes = True

