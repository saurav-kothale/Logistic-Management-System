from functools import total_ordering
import re

from sqlalchemy import false, true


def is_weekend(date):
    return date.weekday() >= 5


def validate_filename(file_name):
    pattern = r'^\d{2}+_\d{4}_[a-z]+\.xlsx$'

    if re.match(pattern, file_name):
        return True
    else:
        return False


def week_or_weekend(row):
    city_name = row["CITY NAME"]
    client_name = row["CLIENT NAME"]
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
                          weekend_amount,
                          maximum_rejection,
                          rejection_amount, 
                          maximum_bad_order,
                          bad_orders_amount
                          ):
    
    order_done = row['Parcel DONE ORDERS']
    rejection = row['REJECTION']
    bad_orders = row['BAD ORDER']
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

    
    if rejection > maximum_rejection:
        amount -= rejection * 10 if rejection_amount is None else rejection * rejection_amount


    if bad_orders > maximum_bad_order:
        amount -= bad_orders * 10 if bad_orders_amount is None else bad_orders_amount * bad_orders


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
    
    order_done = row['Parcel DONE ORDERS']
    rejection = row['REJECTION']
    bad_orders = row['BAD ORDER']
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

    
    if rejection > maximum_rejection:
        amount -= rejection * 10 if rejection_amount is None else rejection * rejection_amount


    if bad_orders > maximum_bad_order:
        amount -= bad_orders * 10 if bad_orders_amount is None else bad_orders_amount * bad_orders


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
    orders = row["Parcel DONE ORDERS"]
    average = row["Average"]
    attendance = row["Attendance"]
    amount = 0

    if average <= orders_less_then:
        amount = attendance*order_amount1

    elif orders_less_then < average <= to_order:
        amount = orders*order_amount2
    
    elif average >= order_grether_than:
        amount = (order_amount2*to_order) + (orders-to_order)*order_amount3

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
    
    orders = row["Parcel DONE ORDERS"]
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
    
    orders = row["Parcel DONE ORDERS"]
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
    order_amount

):

    orders = row["Document DONE ORDERS"]
    amount = 0

    if first_from_condition <= orders <= first_to_condition:
      amount = first_amount * orders
  
    elif second_from_condition <= orders <= second_to_condition:
      amount = second_amount * orders

    elif third_from_condition <= orders <= third_to_condition:
      amount = third_amount * orders

    elif orders >= order_greater_than:
      amount = order_amount * orders

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
    order_amount

):

    orders = row["Parcel DONE ORDERS"]
    amount = 0

    if first_from_condition <= orders <= first_to_condition:
      amount = first_amount * orders
  
    elif second_from_condition <= orders <= second_to_condition:
      amount = second_amount * orders

    elif third_from_condition <= orders <= third_to_condition:
      amount = third_amount * orders

    elif orders >= order_greater_than:
      amount = order_amount * orders

    return amount
    

    