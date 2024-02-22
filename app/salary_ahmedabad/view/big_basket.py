import pandas as pd

def calculate_big_basket_biker_salary(row, data):
    order_done = row["Parcel DONE ORDERS"]
    amount = 0

    if data.biker_from_delivery <= order_done <= data.biker_to_delivery:
        amount = order_done * data.biker_first_amount

    elif order_done >= data.biker_order_greter_than:
        amount = order_done * data.biker_second_amount

    return amount

def calculate_big_basket_micro_salary(row, data):
    order_done = row["Parcel DONE ORDERS"]
    amount = 0

    if data.micro_from_delivery <= order_done <= data.micro_to_delivery:
        amount = order_done * data.micro_first_amount

    elif order_done >= data.micro_order_greter_than:
        amount = order_done * data.micro_second_amount

    return amount


def create_table(dataframe):
    
    table = pd.pivot_table(
            data= dataframe,
            index=["DRIVER_ID", "DRIVER_NAME", "CLIENT NAME", "CITY NAME"],
            aggfunc={
            "REJECTION": "sum",
            "BAD ORDER": "sum",
            "Total_Earning": "sum",
            "Parcel DONE ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN ORDER": "sum",
            "IGCC AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "Total_Orders": "sum",
        }
       )

    return table