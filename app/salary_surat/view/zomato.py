from app.salary_surat.view.view import is_weekend

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
    
    order_done = row['DONE_PARCEL_ORDERS']
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

    
    if rejection > maximum_rejection:
        amount -= rejection * 10 if rejection_amount is None else rejection * rejection_amount


    if bad_orders > maximum_bad_order:
        amount -= bad_orders * 10 if bad_orders_amount is None else bad_orders_amount * bad_orders


    return amount


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