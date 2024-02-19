import pandas as pd


def calculate_ecom_salary(row, data):
    order_done = row["Parcel DONE ORDERS"]
    amount = 0

    if data.from_order <= order_done <= data.to_order:
        amount = order_done * data.first_amount

    elif data.second_from_order <= order_done <= data.second_to_order:
        amount = order_done * data.second_amount

    elif data.order_greter_than <= order_done:
        amount = order_done * data.order_amount

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