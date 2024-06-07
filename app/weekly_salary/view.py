from io import BytesIO
import pandas as pd
from sqlalchemy.orm import Session
from app.weekly_salary.model import WeeklyRawData
from fastapi import status

from sqlalchemy.exc import IntegrityError

def calculate_payment(df):
    def calculate_row(row):
        city_name = row['CITY_NAME']
        client_name = row['CLIENT_NAME']
        done_parcel_orders = row['DONE_PARCEL_ORDERS']
        attendance = row['ATTENDANCE']
        
        if city_name == "SURAT":
            if client_name in ["ZOMATO", "SWIGGY", "ECOM"]:
                return done_parcel_orders * 25
            elif client_name == "BB NOW":
                return done_parcel_orders * 30
            elif client_name == "BIGBASKET":
                return done_parcel_orders * 14
            elif client_name == "BLUDART-BIKER" or client_name == "FLIPKART":
                return done_parcel_orders * 13
        elif city_name == "AHMEDABAD":
            if client_name in ["ZOMATO", "BLINKIT", "ECOM"]:
                return done_parcel_orders * 25
            elif client_name == "BB NOW":
                return done_parcel_orders * 30
            elif client_name == "BIGBASKET":
                return done_parcel_orders * 14
            elif client_name == "BLUDART-BIKER" or client_name == "FLIPKART":
                return done_parcel_orders * 13
            elif client_name == "BLUDART_VAN":
                return attendance * 400
        return 0
    
    df["FINAL_AMOUNT"] = df.apply(calculate_row, axis=1)
    
    return df

    

def validate_header(file_data):
    df = pd.read_excel(file_data)

    expected_header = [
    "CITY_NAME" ,"CLIENT_NAME","DATE",
    "JOINING_DATE", "COMPANY", "SALARY_DATE",
    "STATUS", "WEEK_NAME", "PHONE_NUMBER",
    "AADHAR_NUMBER", "DRIVER_ID", "DRIVER_NAME",
    "WORK_TYPE", "DONE_PARCEL_ORDERS", "DONE_DOCUMENT_ORDERS",
    "DONE_BIKER_ORDERS", "DONE_MICRO_ORDERS", "RAIN_ORDER",
    "IGCC_AMOUNT", "BAD_ORDER", "REJECTION",
    "ATTENDANCE","OTHER_PANALTY", "CASH_COLLECTED", 
    "CASH_DEPOSITED", "PAYMENT_SENT_ONLINE", "POCKET_WITHDRAWAL"
    ]

    missing_header = [header for header in expected_header if header not in df.columns]

    if missing_header:
        raise ValueError(f"Missing Header in file : {', '.join(missing_header)}")
    
    file_data.seek(0)



async def insert_raw_records(df, filename, file_key, db):
    try:
        for index, row in df.iterrows():
            record = WeeklyRawData(
                FILE_KEY=file_key,
                FILE_NAME=filename,
                CITY_NAME=row["CITY_NAME"],
                CLIENT_NAME=row["CLIENT_NAME"],
                DATE=row["DATE"],
                AADHAR_NUMBER=row["ADDAR_NUMBER"],
                DRIVER_ID=row["DRIVER_ID"],
                DRIVER_NAME=row["DRIVER_NAME"],
                WORK_TYPE=row["WORK_TYPE"],
                LOG_IN_HR=row["LOG_IN_HR"],
                PICKUP_DOCUMENT_ORDERS=row["PICKUP_DOCUMENT_ORDERS"],
                DONE_DOCUMENT_ORDERS=row["DONE_DOCUMENT_ORDERS"],
                PICKUP_PARCEL_ORDERS=row["PICKUP_PARCEL_ORDERS"],
                DONE_PARCEL_ORDERS=row["DONE_PARCEL_ORDERS"],
                PICKUP_BIKER_ORDERS=row["PICKUP_BIKER_ORDERS"],
                DONE_BIKER_ORDERS=row["DONE_BIKER_ORDERS"],
                PICKUP_MICRO_ORDERS=row["PICKUP_MICRO_ORDERS"],
                DONE_MICRO_ORDERS=row["DONE_MICRO_ORDERS"],
                CUSTOMER_TIP=row["CUSTOMER_TIP"],
                RAIN_ORDER=row["RAIN_ORDER"],
                IGCC_AMOUNT=row["IGCC_AMOUNT"],
                BAD_ORDER=row["BAD_ORDER"],
                REJECTION=row["REJECTION"],
                ATTENDANCE=row["ATTENDANCE"],
                CASH_COLLECTION=row["CASH_COLLECTED"],
                CASH_DEPOSIT=row["CASH_DEPOSITED"],
                PAYMENT_SENT_ONLINE = row["PAYMENT_SENT_ONLINE"],
                POCKET_WITHDRAWAL = row["POCKET_WITHDRAWAL"],
                OTHER_PANALTY = row["OTHER_PANALTY"]
            )

            db.add(record)

        db.commit()
    except IntegrityError:
        db.rollback()
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Failed to insert records due to integrity constraint violation."
        }
    except Exception as e:
        db.rollback()
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"An unexpected error occurred: {str(e)}"
        }

    return {
        "status": status.HTTP_201_CREATED,
        "message": "Records inserted successfully."
    }


async def delete_record(db, file_key):
    db.query(WeeklyRawData).filter(WeeklyRawData.FILE_KEY == file_key).delete()
    db.commit()
    return{
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "record deleted successfully"
    }



