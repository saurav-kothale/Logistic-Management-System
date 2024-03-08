import pandas as pd

def calculate_big_basket_biker_salary(
        row,
        biker_from_delivery,
        biker_to_delivery,
        biker_first_amount,
        biker_order_greter_than,
        biker_second_amount
):
    order_done = row["BIKE"]
    amount = 0

    if biker_from_delivery <= order_done <= biker_to_delivery:
        amount = order_done * biker_first_amount

    elif order_done >= biker_order_greter_than:
        amount = order_done * biker_second_amount

    return amount

def calculate_big_basket_micro_salary(
        row,
        micro_from_delivery,
        micro_to_delivery,
        micro_first_amount,
        micro_order_greter_than,
        micro_second_amount


):
    order_done = row["MICRO"]
    amount = 0

    if micro_from_delivery <= order_done <= micro_to_delivery:
        amount = order_done * micro_first_amount

    elif order_done >= micro_order_greter_than:
        amount = order_done * micro_second_amount

    return amount


def create_table(dataframe):
    
    table = pd.pivot_table(
            data= dataframe,
            index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
            aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "BIKE": "sum",
            "MICRO" : "sum",
            "ORDER_AMOUNT": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
        }
       )

    return table