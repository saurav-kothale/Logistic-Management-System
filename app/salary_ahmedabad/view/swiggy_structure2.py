import pandas as pd

def calculate_salary_ahmedabad(row, data):

    order_done = row["Parcel DONE ORDERS"]
    job_type = row["jobtype"]
    amount = 0

    if data.swiggy_first_order_start <= order_done <= data.swiggy_first_order_end:
        amount = order_done * data.swiggy_first_order_amount

    elif data.swiggy_order_greter_than < order_done:
        amount = order_done * data.swiggy_second_order_amount

    if job_type == "fulltime" & order_done < 20:
        amount = amount - 100

    if job_type == "partime" & order_done < 12:
        amount = amount - 70

    return amount


def create_table(dataframe):
    
    table = pd.pivot_table(
            data= dataframe,
            index=["DRIVER_ID", "DRIVER_NAME", "CLIENT NAME", "CITY NAME"],
            aggfunc={
            "REJECTION": "sum",
            "BAD ORDER": "sum",
            "Total_Earning": "sum",
            "Parcel DONE ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN ORDER": "sum",
            "IGCC AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "Total_Orders": "sum",
        }
       )

    return table


def add_bonus(row):

    order_done = row["Parcel DONE ORDERS"]
    job_type = row["Job Type"]
    Total_Amount = row["Total Amount"]

    if job_type == "fulltime" & order_done >= 700:
        Total_Amount = Total_Amount + 1000

    elif job_type == "parttime" & order_done >= 400:
        Total_Amount = Total_Amount + 500

    return Total_Amount