from datetime import datetime
from pydantic import BaseModel

class CategorySchema(BaseModel):
    category_name : str
    created_at : datetime
    updated_at : datetime
    is_deleted : bool = False

class CategoryUpdateSchema(BaseModel):
    category_name : str
