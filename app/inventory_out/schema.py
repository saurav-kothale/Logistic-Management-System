from pydantic import BaseModel

class InventoryOut(BaseModel):
    product_name : str
    category : str
    bike_category : str
    color : str
    size : str
    city : str
    quantity : int