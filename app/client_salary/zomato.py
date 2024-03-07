from app.client_salary.Isalary import ISalary

class ZomatoOrderCalculation:

    def __init__(self, row):
        self.order_done = row["Parcel DONE ORDERS"]
        self.rejections = row["REJECTION"]
        self.bad_orders = row["BAD ORDER"]
        self.date = row["DATE"]
        