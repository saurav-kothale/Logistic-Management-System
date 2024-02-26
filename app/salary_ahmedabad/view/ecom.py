import pandas as pd


def calculate_ecom_salary(row, data):
    order_done = row["PARCEL_DONE_ORDERS"]
    amount = 0

    if data.from_order <= order_done <= data.to_order:
        amount = order_done * data.first_amount

    elif data.second_from_order <= order_done <= data.second_to_order:
        amount = order_done * data.second_amount

    elif data.order_greter_than <= order_done:
        amount = order_done * data.ORDER_AMOUNT

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