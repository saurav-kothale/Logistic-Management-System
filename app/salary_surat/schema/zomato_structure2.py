from typing import Optional
from xml.etree.ElementInclude import include
from pandas import to_datetime
from pydantic import BaseModel, validator
from fastapi import UploadFile, Form
from sqlalchemy import true
from datetime import date as date_type

from app.client_salary import zomato

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

class SuratZomatoStructureNew2(BaseModel):
    slab : bool = True
    zomato_first_order_start: int = 1 
    zomato_first_order_end: int = 29
    zomato_first_order_amount: int = 30
    zomato_order_greter_than: int = 30
    zomato_second_order_amount: int = 35
    vahicle_charges: bool = True
    fulltime_average: int = 20
    fulltime_greter_than_order : int = 20
    vahicle_charges_fulltime : int = 100
    partime_average: int = 11
    partime_greter_than_order: int = 11
    vahicle_charges_partime: int = 70
    bonus : bool = True
    bonus_order_fulltime: int = 630
    bonus_amount_fulltime: int = 1000
    bonus_order_partime: int = 350
    bonus_amount_partime: int = 500
    rejection : bool = True
    rejection_orders: int = 2
    rejection_amount : int = 20
    bad_order : bool = True
    bad_orders : int = 2
    bad_order_amount : int = 20

    class Config:
        from_attributes = True


class SuratZomatoStructureNew3(BaseModel):
    from_date :Optional[str]
    to_date : Optional[str]
    zomato_first_order_start: int = 1 
    zomato_first_order_end: int = 29
    zomato_first_week_amount: int = 30
    zomato_first_weekend_amount: int = 32
    zomato_second_order_start:int = 20
    zomato_second_order_end:int = 25
    zomato_second_week_amount: int = 25
    zomato_second_weekend_amount: int = 27
    zomato_order_greter_than: int = 26
    zomato_third_week_amount: int = 30
    zomato_third_weekend_amount: int = 32

    class Config:
        from_attributes = True

class TimeStructureSchema(BaseModel):
    file_key : str
    include_slab : bool = True
    slabs : list[SuratZomatoStructureNew3]
    include_vahicle_charges: bool = True
    fulltime_average: int = 20
    fulltime_greter_than_order : int = 20
    vahicle_charges_fulltime : int = 100
    partime_average: int = 11
    partime_greter_than_order: int = 12
    vahicle_charges_partime: int = 70
    include_bonus : bool = True
    bonus_order_fulltime: int = 700
    bonus_amount_fulltime: int = 1000
    bonus_order_partime: int = 400
    bonus_amount_partime: int = 500
    include_rejection : bool = True
    rejection_orders: int = 2
    rejection_amount : int = 20
    include_bad_order : bool = True
    bad_orders : int = 2
    bad_orders_amount : int = 20