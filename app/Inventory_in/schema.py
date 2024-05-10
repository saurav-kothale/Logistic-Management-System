from abc import update_abstractmethods
from ssl import create_default_context
from pydantic import BaseModel, Field, validator
from datetime import date, datetime


class Invetory(BaseModel):
    invoice_number : str 
    invoice_amount : int 
    invoice_date : date  
    inventory_paydate : date
    vendor : str
    invoice_image_id : str


class InvetoryUpdate(BaseModel):
    invoice_number : str
    invoice_amount : int
    invoice_date : date 
    inventory_paydate : date
    vendor : str
    invoice_image_id : str

    class config:
        from_attributes = True

class InvetoryResponse(BaseModel):
    invoice_id : str
    invoice_number : str
    invoice_amount : int
    invoice_date : date
    inventory_paydate : date
    vendor : str
    invoice_image_id : str

    class config:
        from_attributes = True