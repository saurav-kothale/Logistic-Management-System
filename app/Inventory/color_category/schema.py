from datetime import datetime
from pydantic import BaseModel

class ColorCategorySchema(BaseModel):
    color_name : str
    created_at : datetime
    updated_at : datetime
    is_deleted : bool = False

class ColorUpdateSchema(BaseModel):
    color_name : str
