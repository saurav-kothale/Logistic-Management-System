from numpy import average
import pandas as pd

def calculate_salary_surat(row, data):

    order_done = row["PARCEL_DONE_ORDERS"]
    amount = 0

    if data.swiggy_first_order_start <= order_done <= data.swiggy_first_order_end:
        amount = order_done * data.swiggy_first_order_amount

    elif order_done >= data.swiggy_order_greter_than:
        amount = order_done * data.swiggy_second_order_amount

    return amount

def is_weekend(date):
    return date.weekday() >= 5

def week_or_weekend(row):
    date = row["DATE"]
 
    if is_weekend(date):
        return True
    
    else:
        return False
        
    return ""

def calculate_amount_for_surat_rental_model(row, data
                          ):
    
    order_done = row['PARCEL_DONE_ORDERS']
    date = row["DATE"]
    amount = 0
    
    
    if data.swiggy_first_order_start <= order_done <= data.swiggy_first_order_end:
        if is_weekend(date):
            amount = order_done*data.swiggy_first_weekend_amount
            
        else:
            amount = order_done * data.first_week_amount
        

    elif data.second_from_order <= order_done <= data.second_to_order:
        if is_weekend(date):
            amount = order_done * data.second_weekend_amount
        else:
            amount = order_done * data.second_week_amount
        

    elif order_done >= data.order_grether_than:
        if is_weekend(date):
            amount = order_done*data.weekend_amount
        else:
            amount = order_done*data.week_amount


    return amount




def calculate_bike_charges(row, data):
    average = row["AVERAGE"]
    job_type = row["WORK_TYPE"]
    amount = 0

    if job_type == "full time" and average <= data.vahicle_charges_order_fulltime:
        amount = data.vahicle_charges_fulltime

    elif job_type == "part Time" and average <= data.vahicle_charges_order_partime:
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
