from pydantic import BaseModel

class ProductCategorySchema(BaseModel):
    product_name : str
    hsn_code : str
    category : str