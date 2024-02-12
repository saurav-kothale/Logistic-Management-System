from pydantic import BaseModel

class SuratZomatoStructure1(BaseModel):
    first_order_from: int = 1
    first_order_to: int = 19
    first_week_amount: int = 20
    first_weekend_amount: int = 22
    second_order_from: int = 20
    second_order_to: int = 25
    second_week_amount: int = 25
    second_weekend_amount: int = 27
    order_grether_than: int = 25
    week_amount: int = 30
    weekend_amount: int = 32
    maximum_rejection: int = 2
    rejection_amount: int = 10
    maximum_bad_orders: int = 2
    bad_order_amount: int = 10