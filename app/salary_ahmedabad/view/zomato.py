import pandas as pd

def calculate_salary_ahmedabad(row, data):

    order_done = row["PARCEL_DONE_ORDERS"]
    amount = 0

    if data.zomato_first_order_start <= order_done <= data.zomato_first_order_end:
        amount = order_done * data.zomato_first_order_amount

    elif data.zomato_order_greter_than < order_done:
        amount = order_done * data.zomato_second_order_amount

    return amount


def calculate_bike_charges(row, data):
    order_done = row["PARCEL_DONE_ORDERS"]
    job_type = row["WORK_TYPE"]
    amount = 0

    if job_type == "full time" and order_done < data.vahicle_charges_order_fulltime:
        amount = data.vahicle_charges_fulltime

    elif job_type == "part time" and order_done < data.vahicle_charges_order_partime:
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