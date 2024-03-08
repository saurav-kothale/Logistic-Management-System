from pydantic import BaseModel

class AhemedabadFlipkartSchema(BaseModel):
    file_id : str
    file_name : str
    amount : int = 12

