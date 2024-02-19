import pandas as pd


def calculate_flipkart_salary(row, data):
    order_done = row["Parcel DONE ORDERS"]
    amount = 0

    amount = order_done * data.amount

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