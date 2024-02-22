from pydantic import BaseModel

class AhmedabadBigBascketSchema(BaseModel):
    file_id: str
    file_name: str
    biker_from_delivery: int = 1
    biker_to_delivery: int = 15
    biker_first_amount: int = 30
    biker_order_greter_than: int = 16
    biker_second_amount: int = 30
    micro_from_delivery: int = 1
    micro_to_delivery: int = 22
    micro_first_amount: int = 20
    micro_order_greter_than : int = 23
    micro_second_amount: int = 22
