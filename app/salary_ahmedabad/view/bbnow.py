import pandas as pd

def calculate_bbnow_salary(row, data):
    orders = row["DONE_PARCEL_ORDERS"]
    amount = 0

    if data.from_order <= orders <= data.to_order:
        amount = orders * data.first_amount

    elif orders >= data.order_greter_than:
        amount = (data.to_order) * data.first_amount + (
            orders - data.to_order
        ) * data.second_amount
    
    return amount

def calculate_bbnow_salary1(
        row,
        from_order,
        to_order,
        first_amount,
        order_greter_than,
        second_amount
):
    orders = row["DONE_PARCEL_ORDERS"]
    amount = 0

    if from_order <= orders <= to_order:
        amount = orders * first_amount

    elif orders >= order_greter_than:
        amount = ((orders - to_order) * second_amount) + (to_order * first_amount)

    #Implement the code for other conditions

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