import pandas as pd

def calculate_blinkit_salary(row, data):
    order_done = row["PARCEL_DONE_ORDERS"]
    amount = 0

    if data.from_order <= order_done <= data.to_order:
        amount = order_done * data.first_order_amount

    elif order_done >= data.order_greter_than:
        amount = order_done * data.second_order_amount

    return amount


def create_table(dataframe):
    
    table = pd.pivot_table(
            data= dataframe,
            index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
            aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "ORDER_AMOUNT": "sum",
            "PARCEL_DONE_ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
        }
       )

    return table
