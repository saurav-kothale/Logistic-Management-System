from pydantic import BaseModel

class AhmedabadBlinkitSchema(BaseModel):
    file_id : str
    file_name: str
    from_order : int = 1
    to_order : int = 19
    first_order_amount : int = 24
    order_greter_than : int = 20
    second_order_amount : int = 28

    

