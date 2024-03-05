from functools import total_ordering
import re

from sqlalchemy import false, true
import pandas as pd


def is_weekend(date):
    return date.weekday() >= 5


def validate_filename(file_name):
    pattern = r'^\d{2}+_\d{4}_[a-z]+\.xlsx$'

    if re.match(pattern, file_name):
        return True
    else:
        return False


def week_or_weekend(row):
    city_name = row["CITY_NAME"]
    client_name = row["CLIENT_NAME"]
    date = row["DATE"]

    if (
        city_name == "Surat" and
        client_name in ["Swiggy", "Zomato"]
    ):
        
        if is_weekend(date):
            return True
        
        else:
            return False
        
    return ""


def calculate_panalties(
        row,
        maximum_rejection,
        rejection_amount, 
        maximum_bad_order,
        bad_orders_amount
):
    rejection = row['REJECTION']
    bad_orders = row['BAD_ORDER']
    amount = 0
    
    if rejection > maximum_rejection:
        amount -= rejection * 10 if rejection_amount is None else rejection * rejection_amount


    if bad_orders > maximum_bad_order:
        amount -= bad_orders * 10 if bad_orders_amount is None else bad_orders_amount * bad_orders


    return amount


def calculate_amount_for_zomato_surat(row, 
                          first_from_order, 
                          first_to_order, 
                          first_week_amount, 
                          first_weekend_amount,
                          second_from_order, 
                          second_to_order, 
                          second_week_amount, 
                          second_weekend_amount,
                          order_grether_than,
                          week_amount,
                          weekend_amount
                          ):
    
    order_done = row['PARCEL_DONE_ORDERS']
    rejection = row['REJECTION']
    bad_orders = row['BAD_ORDER']
    date = row["DATE"]
    amount = 0
    
    
    if first_from_order <= order_done <= first_to_order:
        if is_weekend(date):
            amount = order_done*first_weekend_amount
            
        else:
            amount = order_done * first_week_amount
        

    elif second_from_order <= order_done <= second_to_order:
        if is_weekend(date):
            amount = order_done * second_weekend_amount
        else:
            amount = order_done * second_week_amount
        

    elif order_done >= order_grether_than:
        if is_weekend(date):
            amount = order_done*weekend_amount
        else:
            amount = order_done*week_amount


    return amount




def calculate_amount_for_surat_swiggy(row, 
                          first_from_order, 
                          first_to_order, 
                          first_week_amount, 
                          first_weekend_amount,
                          second_from_order, 
                          second_to_order, 
                          second_week_amount, 
                          second_weekend_amount,
                          order_grether_than,
                          week_amount,
                          weekend_amount,
                          maximum_rejection,
                          rejection_amount, 
                          maximum_bad_order,
                          bad_orders_amount
                          ):
    
    order_done = row['PARCEL_DONE_ORDERS']
    rejection = row['REJECTION']
    bad_orders = row['BAD_ORDER']
    date = row["DATE"]
    amount = 0
    
    
    if first_from_order <= order_done <= first_to_order:
        if is_weekend(date):
            amount = order_done*first_weekend_amount
            
        else:
            amount = order_done * first_week_amount
        

    elif second_from_order <= order_done <= second_to_order:
        if is_weekend(date):
            amount = order_done * second_weekend_amount
        else:
            amount = order_done * second_week_amount
        

    elif order_done >= order_grether_than:
        if is_weekend(date):
            amount = order_done*weekend_amount
        else:
            amount = order_done*week_amount


    return amount


def calculate_amount_for_bbnow_surat(
        row,
        orders_less_then,
        order_amount1,
        from_order,
        to_order,
        order_amount2,
        order_grether_than,
        order_amount3

):
    orders = row["PARCEL_DONE_ORDERS"]
    average = row["AVERAGE"]
    amount = 0

    if average > 13:
        if orders <= from_order & orders >= to_order:
            amount =  orders * order_amount2
        
        elif orders >= order_grether_than:
            amount = ((orders - to_order) * order_amount3) + 420

    else:
        amount = 0

    return amount

    # elif orders_less_then  average:
    #     amount = orders*order_amount2
    
    # elif average >= order_grether_than:
    #     amount = (order_amount2*to_order) + (orders-to_order)*order_amount3

    return amount

def calculate_order_for_less_amount(
        row,
        orders_less_then,
        order_amount1,
        amount = 0
):
    average = row["AVERAGE"]
    attendance = row["ATTENDANCE"]

    if average <= 13:
        amount = attendance * 400
    
    return amount

    


def calculate_amount_for_ecom_surat(
        row,
        from_order,
        to_order,
        first_amount,
        second_condition_from,
        second_condition_to,
        second_condition_amount,
        third_condition,
        third_condition_amount,

):
    
    orders = row["PARCEL_DONE_ORDERS"]
    amount = 0

    if from_order <= orders <= to_order:
        amount = orders*first_amount

    elif second_condition_from <= orders <= second_condition_to:
        amount = orders * second_condition_amount

    elif orders >= third_condition:
        amount = orders * third_condition_amount

    return amount


def calculate_amount_for_flipkart_surat(
        row,
        from_order,
        to_order,
        first_amount,
        second_condition_from,
        second_condition_to,
        second_condition_amount,
        third_condition,
        third_condition_amount,

):
    
    orders = row["PARCEL_DONE_ORDERS"]
    amount = 0

    if from_order <= orders <= to_order:
        amount = orders*first_amount

    elif second_condition_from <= orders <= second_condition_to:
        amount = orders * second_condition_amount

    elif orders >= third_condition:
        amount = orders * third_condition_amount

    return amount


def calculate_document_amount(
    row,
    first_from_condition,
    first_to_condition,
    first_amount,
    second_from_condition,
    second_to_condition,
    second_amount,
    third_from_condition,
    third_to_condition,
    third_amount,
    order_greater_than,
    ORDER_AMOUNT

):

    orders = row["DOCUMENT_DONE_ORDERS"]
    amount = 0

    if first_from_condition <= orders <= first_to_condition:
      amount = first_amount * orders
  
    elif second_from_condition <= orders <= second_to_condition:
      amount = second_amount * orders

    elif third_from_condition <= orders <= third_to_condition:
      amount = third_amount * orders

    elif orders >= order_greater_than:
      amount = ORDER_AMOUNT * orders

    return amount


def calculate_parcel_amount(
    row,
    first_from_condition,
    first_to_condition,
    first_amount,
    second_from_condition,
    second_to_condition,
    second_amount,
    third_from_condition,
    third_to_condition,
    third_amount,
    order_greater_than,
    ORDER_AMOUNT

):

    orders = row["PARCEL_DONE_ORDERS"]
    amount = 0

    if first_from_condition <= orders <= first_to_condition:
      amount = first_amount * orders
  
    elif second_from_condition <= orders <= second_to_condition:
      amount = second_amount * orders

    elif third_from_condition <= orders <= third_to_condition:
      amount = third_amount * orders

    elif orders >= order_greater_than:
      amount = ORDER_AMOUNT * orders

    return amount
    

def calculate_salary_surat(row, data):

    order_done = row["PARCEL_DONE_ORDERS"]
    job_type = row["jobtype"]
    amount = 0

    if data.zomato_first_order_start <= order_done <= data.zomato_first_order_end:
        amount = order_done * data.zomato_first_order_amount

    elif data.zomato_order_greter_than < order_done:
        amount = order_done * data.zomato_second_order_amount

    if job_type == "full time" & order_done < 20:
        amount = amount - 100

    if job_type == "partime" & order_done < 12:
        amount = amount - 70

    return amount


def create_table(dataframe):
    
    table = pd.pivot_table(
            data= dataframe,
            index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
            aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "Total_Earning": "sum",
            "PARCEL_DONE_ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "Total_Orders": "sum",
        }
       )

    return table


def add_bonus(row):

    order_done = row["PARCEL_DONE_ORDERS"]
    job_type = row["WORK_TYPE"]
    ORDER_AMOUNT = row["ORDER_AMOUNT"]

    if job_type == "full time" & order_done >= 700:
        ORDER_AMOUNT = ORDER_AMOUNT + 1000

    elif job_type == "part time" & order_done >= 400:
        ORDER_AMOUNT = ORDER_AMOUNT + 500

    return ORDER_AMOUNT

    