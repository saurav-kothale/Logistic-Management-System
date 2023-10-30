def is_weedend(date):
    return date.weekday() >= 5


def calculate_amount(
        row, 
        first_condition = None, 
        second_condition = None, 
        first_amount = None, 
        second_amount = None, 
        third_amount = None,
        rejection_amount = None
):
    order_done = row['Parcel DONE ORDERS']
    day_type = row['Weekday_or_Weekend']
    rejection = row['REJECTION']
    bad_order = row['BAD ORDER']
    amount = 0
    
    if day_type == 'Weekday':

        if order_done < 19:
            amount = order_done * 25
        elif 19 <= order_done <= 25:
            amount = order_done * 30
        elif order_done > 25:
            amount = order_done * 35
    elif day_type == 'Weekend':
        if order_done < 19:
            amount = order_done * 27
        elif 19 <= order_done <= 25:
            amount = order_done * 32
        elif order_done > 25:
            amount = order_done * 37

    if rejection >= 2:
        amount -= 10 * rejection

    if bad_order >= 2:
        amount -= 10 * bad_order

    return amount


def week_or_weekend(row):
    city_name = row["CITY NAME"]
    client_name = row["CLIENT NAME"]
    date = row["DATE"]

    if (
        city_name == "Surat" and
        client_name in ["Swiggy", "Zomato"]
    ):
        
        if is_weedend(date):
            return "Weekend"
        
        else:
            return "Weekday"
        
    return ""

def calculate_amount_for_surat(row, 
                          first_condition = None, 
                          second_condition = None, 
                          first_amount = None, 
                          second_amount = None, 
                          third_amount = None, 
                          rejection_amount = None, 
                          bad_orders_amount = None
                          ):
    
    order_done = row['Parcel DONE ORDERS']
    day_type = row['Weekday_or_Weekend']
    rejection = row['REJECTION']
    bad_order = row['BAD ORDER']
    amount = 0
    
    if first_condition is not None and second_condition is not None:
        if day_type == 'Weekday':
            if order_done < first_condition:
                amount = first_amount*order_done if first_amount is not None else order_done * 25
            elif first_condition <= order_done <= second_condition:
                amount = second_amount*order_done if second_amount is not None else order_done * 30
            else:
                amount = third_amount*order_done if third_amount is not None else order_done * 35

        elif day_type == 'Weekend':
            if order_done < first_condition:
                amount = first_amount*order_done if first_amount is not None else order_done * 27
            elif first_condition <= order_done <= second_condition:
                amount = second_amount*order_done if second_amount is not None else order_done * 32
            else:
                amount = third_amount*order_done if third_amount is not None else order_done * 37
    else:
        # Default conditions and amounts based on order range
        if day_type == 'Weekday':
            if order_done < 19:
                amount = first_amount*order_done if first_amount is not None else order_done * 25
            elif 19 <= order_done <= 25:
                amount = second_amount*order_done if second_amount is not None else order_done * 30
            else:
                amount = third_amount*order_done if third_amount is not None else order_done * 35

        elif day_type == 'Weekend':
            if order_done < 19:
                amount = amount = first_amount*order_done if first_amount is not None else order_done * 27
            elif 19 <= order_done <= 25:
                amount = second_amount*order_done if second_amount is not None else order_done * 32
            else:
                amount = third_amount*order_done if third_amount is not None else order_done * 37

        if rejection >= 2:
            amount -= 10 * rejection if rejection_amount is None else rejection_amount*rejection

        if bad_order >= 2:
            amount -= 10 * bad_order if bad_orders_amount is None else bad_orders_amount*bad_order


    return amount

