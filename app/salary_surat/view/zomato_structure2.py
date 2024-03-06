import pandas as pd

def calculate_salary_surat(row, data):

    order_done = row["PARCEL_DONE_ORDERS"]
    amount = 0

    if data.zomato_first_order_start <= order_done <= data.zomato_first_order_end:
        amount = order_done * data.zomato_first_order_amount

    elif order_done >= data.zomato_order_greter_than:
        amount = order_done * data.zomato_second_order_amount

    return amount


def calculate_bike_charges(row, data):
    average = row["AVERAGE"]
    job_type = row["WORK_TYPE"]
    amount = 0

    if job_type == "full time" and average <= data.vahicle_charges_order_fulltime:
        amount = data.vahicle_charges_fulltime

    elif job_type == "part time" and average <= data.vahicle_charges_order_partime:
        amount = data.vahicle_charges_partime

    return amount   



def create_table(dataframe):
    
    table = pd.pivot_table(
            data= dataframe,
            index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME","WORK_TYPE"],
            aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "ORDER_AMOUNT": "sum",
            "BIKE_CHARGES": "sum",
            "PARCEL_DONE_ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
            "REJECTION_AMOUNT": "sum",
            "BAD_ORDER_AMOUNT": "sum"
        }
       )

    return table


def add_bonus(row, data):

    order_done = row["PARCEL_DONE_ORDERS"]
    amount = 0

    if (row["WORK_TYPE"] == "full time") and (order_done >= data.bonus_order_fulltime):
        amount = data.bonus_amount_fulltime

    elif (row["WORK_TYPE"] == "part time") and (order_done >= data.bonus_order_partime):
        amount = data.bonus_amount_partime

    return amount


def calculate_rejection(row, data):
    rejection = row["REJECTION"]
    amount = 0

    if rejection >= data.rejection:
        amount = rejection * data.rejection_amount

    return amount


def calculate_bad_orders(row, data):
    bad_order = row["BAD_ORDER"]
    amount = 0

    if bad_order >= data.bad_order:
        amount = bad_order * data.bad_order_amount

    return amount

def create_dynamic_pivot_table(dataframe):

    dynamic_columns = [
            "REJECTION", "BAD_ORDER", "ORDER_AMOUNT", "BIKE_CHARGES",
            "PARCEL_DONE_ORDERS", "CUSTOMER_TIP", "RAIN_ORDER",
            "IGCC_AMOUNT", "ATTENDANCE", "TOTAL_ORDERS",
            "REJECTION_AMOUNT", "BAD_ORDER_AMOUNT"
        ]
    
    dynamic_columns = [col for col in dynamic_columns if col in dataframe.columns]
    
    table = pd.pivot_table(
            data= dataframe,
            index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME","WORK_TYPE"],
            aggfunc={col: "sum" for col in dynamic_columns}
       )

    return table

