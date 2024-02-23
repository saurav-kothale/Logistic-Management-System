import pandas as pd

def calculate_salary_surat(row, data):

    order_done = row["Parcel DONE ORDERS"]
    job_type = row["Work_Type"]
    amount = 0

    if data.swiggy_first_order_start <= order_done <= data.swiggy_first_order_end:
        amount = order_done * data.swiggy_first_order_amount

    elif data.swiggy_order_greter_than < order_done:
        amount = order_done * data.swiggy_second_order_amount

    if job_type == "Full Time" and order_done < 20:
        amount = amount - 100

    if job_type == "Part Time" and order_done < 12:
        amount = amount - 70

    return amount


def create_table(dataframe):
    
    table = pd.pivot_table(
            data= dataframe,
            index=["DRIVER_ID", "DRIVER_NAME", "CLIENT NAME", "CITY NAME","Work_Type"],
            aggfunc={
            "REJECTION": "sum",
            "BAD ORDER": "sum",
            "Total_Earning": "sum",
            "Parcel DONE ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN ORDER": "sum",
            "IGCC AMOUNT": "sum",
            "ATTENDANCE": "sum",
        }
       )

    return table


def add_bonus(row):

    order_done = row["Parcel DONE ORDERS"]
    Total_Amount = row["Total_Earning"]

    if (row["Work_Type"] == "Full Time") and (order_done >= 700):
        Total_Amount = Total_Amount + 1000

    elif (row["Work_Type"] == "Part Time") and (order_done >= 400):
        Total_Amount = Total_Amount + 500

    return Total_Amount