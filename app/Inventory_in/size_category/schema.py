from datetime import datetime
from pydantic import BaseModel

class SizeCategorySchema(BaseModel):
    size_name : str
    created_at : datetime
    updated_at : datetime
    is_deleted : bool = False

class SizeUpdateSchema(BaseModel):
    size_name : str
