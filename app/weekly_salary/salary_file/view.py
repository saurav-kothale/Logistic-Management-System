from fastapi import status
from app.weekly_salary.salary_file.model import WeeklySalaryData
import pandas as pd

def calculate_payment(df):
    def calculate_row(row):
        city_name = row['CITY_NAME']
        client_name = row['CLIENT_NAME']
        done_biker_orders = row["DONE_BIKER_ORDERS"]
        done_parcel_orders = row['DONE_PARCEL_ORDERS']
        done_document_orders = row["DONE_DOCUMENT_ORDERS"]
        attendance = row['ATTENDANCE']
        payment_sent_online = row['PAYMENT_SENT_ONLINE']
        pocket_withdrawal = row['POCKET_WITHDRAWAL']
        other_panalty = row['OTHER_PANALTY']
        igcc_amount = row['IGCC_AMOUNT']
        rejection = row['REJECTION']
        bad_order = row['BAD_ORDER']
        amount = 0
        
        if city_name == "surat":
            if client_name in ["zomato", "swiggy"]:
                amount = done_parcel_orders * 25
            elif client_name == "e com":
                amount = done_parcel_orders * 12
            elif client_name == "bb now":
                amount = done_parcel_orders * 25
            elif client_name == "bluedart biker":
                amount = done_parcel_orders * 10
            elif client_name == "bluedart biker":
                amount = done_document_orders * 5
            elif client_name == "flipkart":
                amount = done_parcel_orders * 10
            elif client_name == "bluedart van":
                amount = attendance * 450
            elif client_name == "uptown fresh":
                amount = attendance * 400


                
        elif city_name == "ahmedabad":
            if client_name == "zomato":
                amount = done_parcel_orders * 25
            elif client_name == "e com":
                amount = done_parcel_orders * 11
            elif client_name == "bb now":
                amount = done_parcel_orders * 25
            elif client_name == "bb 5k":
                amount = done_biker_orders * 25
            elif client_name == "blinkit":
                amount = done_parcel_orders * 20
            elif client_name == "flipkart":
                amount = done_parcel_orders * 10
            
            
        elif city_name == "vadodara":

            if client_name == "bb now":
                amount = done_parcel_orders * 25



        if client_name in ["zomato", "swiggy"]:
            panalty = payment_sent_online + pocket_withdrawal + other_panalty + igcc_amount + (rejection*30) + (bad_order*50) + 100
            amount = amount - panalty    
        return amount
    
    df["FINAL_AMOUNT"] = df.apply(calculate_row, axis=1)
    
    return df


async def insert_salary_records(df, filename, file_key, db):
    # try:
    for index, row in df.iterrows():
        record = WeeklySalaryData(
            FILE_KEY=file_key,
            FILE_NAME=filename,
            CITY_NAME=row["CITY_NAME"],
            CLIENT_NAME=row["CLIENT_NAME"],
            DATE=row["DATE"],
            JOINING_DATE=row["JOINING_DATE"],
            COMPANY=row["COMPANY"],
            SALARY_DAY=str(row["SALARY_DAY"]),
            STATUS = row["STATUS"],
            EXIT_DATE = str(row["EXIT_DATE"]),
            WEEK_NAME = row["WEEK_NAME"],
            PHONE_NUMBER = row["PHONE_NUMBER"],
            AADHAR_NUMBER=row["AADHAR_NUMBER"],
            DRIVER_ID=str(row["DRIVER_ID"]),
            DRIVER_NAME=row["DRIVER_NAME"],
            DESIGNATION_NAME=row["DESIGNATION_NAME"],
            # LOG_IN_HR=row["LOG_IN_HR"],
            # PICKUP_DOCUMENT_ORDERS=row["PICKUP_DOCUMENT_ORDERS"],
            DONE_PARCEL_ORDERS=row["DONE_PARCEL_ORDERS"],
            DONE_DOCUMENT_ORDERS=row["DONE_DOCUMENT_ORDERS"],
            # PICKUP_PARCEL_ORDERS=row["PICKUP_PARCEL_ORDERS"],
            # PICKUP_BIKER_ORDERS=row["PICKUP_BIKER_ORDERS"],
            DONE_BIKER_ORDERS=row["DONE_BIKER_ORDERS"],
            # PICKUP_MICRO_ORDERS=row["PICKUP_MICRO_ORDERS"],
            DONE_MICRO_ORDERS=row["DONE_MICRO_ORDERS"],
            RAIN_ORDER=row["RAIN_ORDER"],
            IGCC_AMOUNT=row["IGCC_AMOUNT"],
            BAD_ORDER=row["BAD_ORDER"],
            REJECTION=row["REJECTION"],
            ATTENDANCE=row["ATTENDANCE"],
            CASH_COLLECTED=row["CASH_COLLECTED"],
            CASH_DEPOSITED=row["CASH_DEPOSITED"],
            PAYMENT_SENT_ONLINE = row["PAYMENT_SENT_ONLINE"],
            POCKET_WITHDRAWAL = row["POCKET_WITHDRAWAL"],
            OTHER_PANALTY = row["OTHER_PANALTY"],
            FINAL_AMOUNT = row["FINAL_AMOUNT"]
        )

        db.add(record)

    db.commit()
    # except IntegrityError:
    #     db.rollback()
    #     return {
    #         "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         "message": "Failed to insert records due to integrity constraint violation."
    #     }
    # except Exception as e:
    #     db.rollback()
    #     return {
    #         "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         "message": f"An unexpected error occurred: {str(e)}"
    #     }

    return {
        "status": status.HTTP_201_CREATED,
        "message": "Records inserted successfully."
    }


async def delete_record(db, file_key):
    db.query(WeeklySalaryData).filter(WeeklySalaryData.FILE_KEY == file_key).delete()
    db.commit()
    return{
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "record deleted successfully"
    }


def create_pivot_table(df):
    
    table = pd.pivot_table(
            data= df,
            index=[
                "PHONE_NUMBER"
                # "CITY_NAME", "DATE", "JOINING_DATE", "COMPANY",
                # "SALARY_DATE", "STATUS", "WEEK_NAME",
                # "PHONE_NUMBER", "AADHAR_NUMBER", "WORK_TYPE",
                
            ],
            aggfunc={
            "DONE_PARCEL_ORDERS" : "sum",
            "DONE_DOCUMENT_ORDERS" : "sum",
            "DONE_BIKER_ORDERS" : "sum",
            "DONE_MICRO_ORDERS" : "sum",
            "RAIN_ORDER" : "sum",
            "IGCC_AMOUNT" : "sum",
            "BAD_ORDER" : "sum",
            "REJECTION" : "sum",
            "ATTENDANCE" : "sum",
            "CASH_COLLECTED" : "sum",
            "CASH_DEPOSITED" : "sum",
            "PAYMENT_SENT_ONLINE" : "sum",
            "POCKET_WITHDRAWAL" : "sum",
            "OTHER_PANALTY" : "sum",
            "FINAL_AMOUNT": "sum"
        }
       ).reset_index()
    
    non_aggregated_fields = df[[
        "DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME",
        "CITY_NAME", "DATE", "JOINING_DATE", "COMPANY",
        "SALARY_DAY", "STATUS", "WEEK_NAME",
        "PHONE_NUMBER", "AADHAR_NUMBER", "WORK_TYPE","EXIT_DATE", "DESIGNATION_NAME"
    ]].drop_duplicates(subset=["PHONE_NUMBER"])

    # Merge the pivot table with non-aggregated fields
    result = pd.merge(table, non_aggregated_fields, on="PHONE_NUMBER", how="left")

    return result

    # return table


# def create_merge_pivot_table(df):
#     table = pd.pivot_table(
#             data= df,
#             index=[
#                 "DRIVER_ID"
#                 # "CITY_NAME", "DATE", "JOINING_DATE", "COMPANY",
#                 # "SALARY_DATE", "STATUS", "WEEK_NAME",
#                 # "PHONE_NUMBER", "AADHAR_NUMBER", "WORK_TYPE",
                
#             ],
#             aggfunc={
#             "DONE_PARCEL_ORDERS" : "sum",
#             "DONE_DOCUMENT_ORDERS" : "sum",
#             "DONE_BIKER_ORDERS" : "sum",
#             "DONE_MICRO_ORDERS" : "sum",
#             "RAIN_ORDER" : "sum",
#             "IGCC_AMOUNT" : "sum",
#             "BAD_ORDER" : "sum",
#             "REJECTION" : "sum",
#             "ATTENDANCE" : "sum",
#             "CASH_COLLECTED" : "sum",
#             "CASH_DEPOSITED" : "sum",
#             "PAYMENT_SENT_ONLINE" : "sum",
#             "POCKET_WITHDRAWAL" : "sum",
#             "OTHER_PANALTY" : "sum",
#             "FINAL_AMOUNT": "sum"
#         }
#        ).reset_index()
    
#     non_aggregated_fields = df[[
#         "DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME",
#         "CITY_NAME", "DATE", "JOINING_DATE", "COMPANY",
#         "SALARY_DATE", "STATUS", "WEEK_NAME",
#         "PHONE_NUMBER", "AADHAR_NUMBER", "WORK_TYPE"
#     ]].drop_duplicates(subset=["DRIVER_ID"])

#     # Merge the pivot table with non-aggregated fields
#     result = pd.merge(table, non_aggregated_fields, on="DRIVER_ID", how="left")

#     return result


