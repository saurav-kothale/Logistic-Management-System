import pandas as pd

def calculate_salary_surat(row, data):

    order_done = row["Parcel DONE ORDERS"]
    amount = 0

    if data.zomato_first_order_start <= order_done <= data.zomato_first_order_end:
        amount = order_done * data.zomato_first_order_amount

    elif data.zomato_order_greter_than < order_done:
        amount = order_done * data.zomato_second_order_amount

    return amount


def calculate_bike_charges(row, data):
    order_done = row["Parcel DONE ORDERS"]
    job_type = row["Work_Type"]
    amount = 0

    if job_type == "Full Time" and order_done < data.vahicle_charges_order_fulltime:
        amount = data.vahicle_charges_fulltime

    elif job_type == "Part Time" and order_done < data.vahicle_charges_order_partime:
        amount = data.vahicle_charges_partime

    return amount

    



def create_table(dataframe):
    
    table = pd.pivot_table(
            data= dataframe,
            index=["DRIVER_ID", "DRIVER_NAME", "CLIENT NAME", "CITY NAME","Work_Type"],
            aggfunc={
            "REJECTION": "sum",
            "BAD ORDER": "sum",
            "Order_Amount": "sum",
            "Bike_Charges": "sum",
            "Parcel DONE ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN ORDER": "sum",
            "IGCC AMOUNT": "sum",
            "ATTENDANCE": "sum",
        }
       )

    return table


def add_bonus(row, data):

    order_done = row["Parcel DONE ORDERS"]
    amount = 0

    if (row["Work_Type"] == "Full Time") and (order_done >= data.bonus_order_fulltime):
        amount = data.bonus_amount_fulltime

    elif (row["Work_Type"] == "Part Time") and (order_done >= data.bonus_order_partime):
        amount = data.bonus_amount_partime

    return amount