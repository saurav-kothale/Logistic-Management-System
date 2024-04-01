import pandas as pd

def is_weekend(date):
    return date.isoweekday() > 6

def calculate_salary_surat(
        row,
        zomato_first_order_start,
        zomato_first_order_end,
        zomato_first_order_amount,
        zomato_order_greter_than,
        zomato_second_order_amount

):

    order_done = row["DONE_PARCEL_ORDERS"]
    amount = 0

    if zomato_first_order_start <= order_done <= zomato_first_order_end:
        amount = order_done * zomato_first_order_amount

    elif order_done >= zomato_order_greter_than:
        amount = order_done * zomato_second_order_amount

    return amount


def calculate_bike_charges(row, data):
    average = row["AVERAGE"]
    job_type = row["WORK_TYPE"]
    amount = 0

    if job_type == "full time" and average <= data.fulltime_average:
        amount = data.vahicle_charges_fulltime

    elif job_type == "part time" and average <= data.partime_average:
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
            "DONE_PARCEL_ORDERS": "sum",
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


def add_bonus(
        row,
        bonus_order_fulltime,
        bonus_amount_fulltime,
        bonus_order_partime,
        bonus_amount_partime

):

    order_done = row["DONE_PARCEL_ORDERS"]
    amount = 0

    if (row["WORK_TYPE"] == "full time") and (order_done >= bonus_order_fulltime):
        amount = bonus_amount_fulltime

    elif (row["WORK_TYPE"] == "part time") and (order_done >= bonus_order_partime):
        amount = bonus_amount_partime

    return amount


def calculate_rejection(
        row,
        rejection_orders,
        rejection_amount

):
    rejection = row["REJECTION"]
    amount = 0

    if rejection >= rejection_orders:
        amount = rejection * rejection_amount

    return amount


def calculate_bad_orders(
        row,
        bad_orders,
        bad_orders_amount
):
    bad_order = row["BAD_ORDER"]
    amount = 0

    if bad_order >= bad_orders:
        amount = bad_order * bad_orders_amount

    return amount


def calculate_amount_for_surat_rental_model(
        row,
        zomato_first_order_start,
        zomato_first_order_end,
        zomato_first_week_amount,
        zomato_first_weekend_amount,
        zomato_second_order_start,
        zomato_second_order_end,
        zomato_second_week_amount,
        zomato_second_weekend_amount,
        zomato_order_greter_than,
        zomato_third_week_amount,
        zomato_third_weekend_amount

):

    order_done = row["DONE_PARCEL_ORDERS"]
    date = row["DATE"]
    amount = 0

    if zomato_first_order_start <= order_done <= zomato_first_order_end:
        if is_weekend(date):
            amount = order_done * zomato_first_weekend_amount

        else:
            amount = order_done * zomato_first_week_amount

    elif zomato_second_order_start <= order_done <= zomato_second_order_end:
        if is_weekend(date):
            amount = order_done * zomato_second_weekend_amount
        else:
            amount = order_done * zomato_second_week_amount

    elif order_done >= zomato_order_greter_than:
        if is_weekend(date):
            amount = order_done * zomato_third_weekend_amount
        else:
            amount = order_done * zomato_third_week_amount

    return amount


def calculate_bike_charges_for_rental_model(
        row,
        fulltime_average,
        fulltime_greter_than_order,
        vahicle_charges_fulltime,
        partime_average,
        partime_greter_than_order,
        vahicle_charges_partime

):
    average = row["AVERAGE"]
    job_type = row["WORK_TYPE"]
    orders = row["DONE_PARCEL_ORDERS"]
    amount = 0

    if (
        job_type == "full time"
        and average <= fulltime_average
        and orders <= fulltime_greter_than_order
    ):
        amount = vahicle_charges_fulltime

    elif (
        job_type == "full time"
        and average <= fulltime_average
        and orders >= fulltime_greter_than_order
    ):
        amount = vahicle_charges_fulltime

    elif (
        job_type == "part Time"
        and average <= partime_average
        and orders <= partime_greter_than_order
    ):
        amount = vahicle_charges_partime
    
    elif (
        job_type == "part Time"
        and average <= partime_average
        and orders >= partime_greter_than_order
    ):
        amount = vahicle_charges_partime

    return amount

