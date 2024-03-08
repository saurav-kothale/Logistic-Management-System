from pydantic import BaseModel

class AhemedabadEcomSchema(BaseModel):
    file_id : str
    file_name: str
    from_order: int = 1
    to_order: int = 40
    first_amount : int = 13
    second_from_order : int = 41
    second_to_order : int = 60
    second_amount : int = 14
    order_greter_than : int = 61
    order_amount : int = 15


