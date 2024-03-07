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
    return date.isoweekday() > 6


def week_or_weekend(row):
    date = row["DATE"]

    if is_weekend(date):
        return True

    else:
        return False

    return ""


def calculate_amount_for_surat_rental_model(row, data):

    order_done = row["PARCEL_DONE_ORDERS"]
    date = row["DATE"]
    amount = 0

    if data.swiggy_first_order_start <= order_done <= data.swiggy_first_order_end:
        if is_weekend(date):
            amount = order_done * data.swiggy_first_weekend_amount

        else:
            amount = order_done * data.swiggy_first_week_amount

    elif data.swiggy_second_order_start <= order_done <= data.swiggy_second_order_end:
        if is_weekend(date):
            amount = order_done * data.swiggy_second_weekend_amount
        else:
            amount = order_done * data.swiggy_second_week_amount

    elif order_done >= data.swiggy_order_greter_than:
        if is_weekend(date):
            amount = order_done * data.swiggy_third_weekend_amount
        else:
            amount = order_done * data.swiggy_third_week_amount

    return amount


def calculate_bike_charges(row, data):
    average = row["AVERAGE"]
    job_type = row["WORK_TYPE"]
    orders = row["PARCEL_DONE_ORDERS"]
    amount = 0

    if (
        job_type == "full time"
        and average <= data.fulltime_average
        and orders <= data.fulltime_greter_than_order
    ):
        amount = data.vahicle_charges_fulltime

    elif (
        job_type == "full time"
        and average <= data.fulltime_average
        and orders >= data.fulltime_greter_than_order
    ):
        amount = data.vahicle_charges_fulltime

    elif (
        job_type == "part Time"
        and average <= data.partime_average
        and orders <= data.partime_greter_than_order
    ):
        amount = data.vahicle_charges_partime
    
    elif (
        job_type == "part Time"
        and average <= data.partime_average
        and orders >= data.partime_greter_than_order
    ):
        amount = data.vahicle_charges_partime

    return amount


def create_table(dataframe):

    table = pd.pivot_table(
        data=dataframe,
        index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME", "WORK_TYPE"],
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
            "BAD_ORDER_AMOUNT": "sum",
        },
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

    if rejection >= data.rejection_orders:
        amount = rejection * data.rejection_amount

    return amount


def calculate_bad_orders(row, data):
    bad_order = row["BAD_ORDER"]
    amount = 0

    if bad_order >= data.bad_orders:
        amount = bad_order * data.bad_orders_amount

    return amount
