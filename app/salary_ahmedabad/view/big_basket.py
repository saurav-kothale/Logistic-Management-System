import pandas as pd

def calculate_big_basket_biker_salary(
        row,
        biker_from_delivery,
        biker_to_delivery,
        first_biker_amount,
        second_biker_from_delivery,
        second_biker_to_delivery,
        second_biker_amount,
        third_biker_from_delivery,
        third_biker_to_delivery,
        third_biker_amount,
        fourth_biker_from_delivery,
        fourth_biker_to_delivery,
        fourth_biker_amount,
        biker_order_greter_than,
        biker_second_amount
):
    order_done = row["DONE_BIKER_ORDERS"]
    amount = 0

    if biker_from_delivery <= order_done <= biker_to_delivery:
        amount = order_done * first_biker_amount

    elif second_biker_from_delivery <= order_done <= second_biker_to_delivery:
        amount = order_done * second_biker_amount

    elif third_biker_from_delivery <= order_done <= third_biker_to_delivery:
        amount = order_done * third_biker_amount

    elif fourth_biker_from_delivery <= order_done <= fourth_biker_to_delivery:
        amount = order_done * fourth_biker_amount

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
    order_done = row["DONE_MICRO_ORDERS"]
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
            "DONE_BIKER_ORDERS": "sum",
            "DONE_MICRO_ORDERS" : "sum",
            "ORDER_AMOUNT": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
        }
       )

    return table