import datetime
from turtle import color
from pydantic import BaseModel
from sqlalchemy import false

class Item(BaseModel):
    item_id : str
    user_id : str
    category : str
    sub_category : str
    product_name : str
    quantity : int
    size : str
    color : str
    is_used : bool = False
    created_at : datetime.datetime
    updated_at : datetime.datetime
    is_deleted : bool  = False

class FleetInventory(BaseModel):
    container_id : str
    invoice_no : str
    invoice_amount : int
    pay_date : datetime.datetime
    created_at: datetime.datetime
    updated_at : datetime.datetime
    vendor : str
    item : list[Item]
    is_deleted : bool = False


