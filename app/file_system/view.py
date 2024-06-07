import pandas as pd
from sqlalchemy.orm import Session
from app.file_system.model import FileRecord
from fastapi import status

from sqlalchemy.exc import IntegrityError

async def insert_records(df, file_name, db):
    try:
        for index, row in df.iterrows():
            record = FileRecord(
                file_name=file_name,
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
                CASH_COLLECTION=row["CASH_COLLECTION"],
                CASH_DEPOSIT=row["CASH_DEPOSIT"]
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

async def delete_record(db, file_name):
    db.query(FileRecord).filter(FileRecord.file_name == file_name).delete()
    db.commit()
    return{
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "record deleted successfully"
    }

