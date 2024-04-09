from datetime import datetime
from pydantic import BaseModel

class BikeCategorySchema(BaseModel):
    bike_name : str
    created_at : datetime
    updated_at : datetime
    is_deleted : bool = False

class BikeUpdateSchema(BaseModel):
    bike_name : str
