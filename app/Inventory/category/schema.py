from pydantic import BaseModel

class Category(BaseModel):
    category_id : str
    category_name : str
    bike_category : list[str]
    size : list[str]
    color : list[str]
    city : list[str]


class CategoryUpdate(BaseModel):
    category_name : str
    bike_category : list[str]
    size : list[str]
    color : list[str]
    city : list[str]