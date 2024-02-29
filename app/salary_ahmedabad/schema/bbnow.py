from pydantic import BaseModel

class AhmedabadBbnowSchema(BaseModel):
    from_order: int = 1
    to_order : int = 15
    first_amount : int = 30
    order_greter_that: int = 16
    second_amount: int = 35
    