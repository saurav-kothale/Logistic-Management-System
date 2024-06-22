from io import BytesIO
import pandas as pd
from sqlalchemy import true
from sqlalchemy.orm import Session
from app.weekly_salary.raw_file.model import WeeklyRawData
from fastapi import status

from sqlalchemy.exc import IntegrityError
    

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

def validate_city(file_data):
    df = pd.read_excel(file_data)

    cities = ["surat", "ahmedabad", "vadodara"]
    
    df_cities_count = df["CITY_NAME"].nunique()
    df_cities = df["CITY_NAME"].unique()

    for count in range(df_cities_count):
        if df_cities[count] not in cities:
            raise Exception(f"Invalid field : {df_cities[count]}")
        
    return True

def validate_client(file_data):
    df = pd.read_excel(file_data)

    clients = ["bb 5k", "bb now", "blinkit", "e com", "flipkart", "zomato", "swiggy", "bluedart biker", "bluedart van", "uptown fresh"]
    
    df_client_count = df["CLIENT_NAME"].nunique()
    df_client = df["CLIENT_NAME"].unique()

    for count in range(df_client_count):
        if df_client[count] not in clients:
            raise Exception(f"Invalid field : {df_client[count]}")
        
    return True


            








async def insert_raw_records(df, filename, file_key, db):
    # try:
    for index, row in df.iterrows():
        record = WeeklyRawData(
            FILE_KEY=file_key,
            FILE_NAME=filename,
            CITY_NAME=row["CITY_NAME"],
            CLIENT_NAME=row["CLIENT_NAME"],
            DATE=row["DATE"],
            JOINING_DATE=row["JOINING_DATE"],
            COMPANY=row["COMPANY"],
            SALARY_DATE=row["SALARY_DATE"],
            SATAUS = row["STATUS"],
            WEEK_NAME = row["WEEK_NAME"],
            PHONE_NUMBER = row["PHONE_NUMBER"],
            AADHAR_NUMBER=row["AADHAR_NUMBER"],
            DRIVER_ID=str(row["DRIVER_ID"]),
            DRIVER_NAME=row["DRIVER_NAME"],
            WORK_TYPE=row["WORK_TYPE"],
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
            OTHER_PANALTY = row["OTHER_PANALTY"]
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
    db.query(WeeklyRawData).filter(WeeklyRawData.FILE_KEY == file_key).delete()
    db.commit()
    return{
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "record deleted successfully"
    }



