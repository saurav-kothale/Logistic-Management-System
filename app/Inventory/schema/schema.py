from abc import update_abstractmethods
from ssl import create_default_context
from pydantic import BaseModel
from datetime import date, datetime


class Invetory(BaseModel):
    invoice_number : int 
    invoice_amount : int 
    invoice_date : date 
    inventory_paydate : date
    vender : str
    invoice_image_id : str


class InvetoryUpdate(BaseModel):
    invoice_amount : int
    invoice_date : date
    inventory_paydate : date
    vendor : str
    invoice_image_id : str

    class config:
        from_attributes = True

class InvetoryResponse(BaseModel):
    invoice_number : int
    invoice_amount : int
    invoice_date : date
    inventory_paydate : date
    vendor : str
    invoice_image_id : str

    class config:
        from_attributes = True