from app.salary_ahmedabad.view.Isalary import ISalary
import pandas as pd


class ZomatoSalary(ISalary):

    def __init__(self, row, data):
        self.row = row
        self.data = data
        self.order_done = self.row["Parcel DONE ORDERS"]
        self.job_type = self.row["job_type"]
        self.amount = 0

    def calculate(self):

        if (
            self.data.zomato_first_order_start
            < self.order_done
            < self.data.zomato_first_order_end
        ):
            self.amount = self.order_done * self.data.zomato_first_order_amount

        elif self.data.zomato_order_greter_than > self.order_done:
            self.amount = self.order_done * self.data.zomato_second_order_amount

        if self.job_type == "fulltime" & self.order_done < 20:
            self.amount = self.amount - 100

        if self.job_type == "partime" & self.order_done < 12:
            self.amount = self.amount - 70

        return self.amount


    def calculate_bonus(self):

        if self.job_type == "fulltime" & self.order_done >= 750:
            self.amount = self.amount + 1000

        elif self.job_type == "parttime" & self.order_done >= 400:
            self.amount = self.amount + 500

        return self.amount
    
    def make_pivot_table(self, dataframe):
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


def calculate_salary_surat(row, data):

    order_done = row["Parcel DONE ORDERS"]
    job_type = row["jobtype"]
    amount = 0

    if data.zomato_first_order_start <= order_done <= data.zomato_first_order_end:
        amount = order_done * data.zomato_first_order_amount

    elif data.zomato_order_greter_than < order_done:
        amount = order_done * data.zomato_second_order_amount

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

    

        
