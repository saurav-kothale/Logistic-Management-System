from datetime import datetime
from pydantic import BaseModel

class CityCategorySchema(BaseModel):
    city_name : str
    created_at : datetime
    updated_at : datetime
    is_deleted : bool = False

class CityUpdateSchema(BaseModel):
    city_name : str
