from pydantic import BaseModel

class InventoryOut(BaseModel):
    product_name : str
    name : str
    category : str
    HSN_code : str
    bike_category : str
    color : str
    size : str
    city : str
    quantity : int