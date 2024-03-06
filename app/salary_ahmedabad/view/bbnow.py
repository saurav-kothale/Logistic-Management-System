import pandas as pd

def calculate_bbnow_salary(row, data):
    orders = row["PARCEL_DONE_ORDERS"]
    amount = 0

    if data.from_order <= orders <= data.to_order:
        amount = orders * data.first_amount

    elif orders >= data.order_greter_than:
        amount = (data.to_order) * data.first_amount + (
            orders - data.to_order
        ) * data.second_amount
    
    return amount

def calculate_bbnow_salary1(row, data):
    orders = row["PARCEL_DONE_ORDERS"]
    amount = 0

    if data.from_order <= orders <= data.to_order:
        amount = orders * data.first_amount

    elif orders >= data.order_greter_than:
        amount = orders * data.second_amount

    return amount



def create_table(dataframe):
    
    table = pd.pivot_table(
            data= dataframe,
            index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
            aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "ORDER_AMOUNT": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
        }
       )

    return table