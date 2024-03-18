from pydantic import BaseModel
from enum import Enum

class BikeCategory(str, Enum):
    optima_cx_er = "OPTIMA CX ER"
    




class ProductSchema(BaseModel):
    product_name: str
    category : str
    sub_category : str
    quantity : int
    size : str
    city : str