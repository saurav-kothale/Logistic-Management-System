from logging import exception
from fastapi import APIRouter, Body, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy import false
from app.salary_surat.schema.zomato_structure2 import (
    SuratZomatoStructure2,
    SuratZomatoStructureNew2,
)
from app.salary_surat.view.zomato_structure2 import (
    add_bonus,
    calculate_salary_surat,
    create_table,
    calculate_bike_charges,
    calculate_rejection,
    calculate_bad_orders,
)
import pandas as pd
import tempfile, json
import uuid
from app.salary_surat.model.model import SalaryFile
from datetime import datetime
from database.database import SessionLocal
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
from decouple import config


surat_zomato_structure2_router = APIRouter()
db = SessionLocal()
row_bucket = config("ROW_BUCKET")
processed_bucket = config("PROCESSED_FILE_BUCKET")


@surat_zomato_structure2_router.post("/zomato/structure2")
def claculate_salary(
    data: SuratZomatoStructure2 = Depends(), file: UploadFile = File(...)
):

    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y")

    df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "zomato")]

    df["TOTAL_ORDERS"] = df["DOCUMENT_DONE_ORDERS"] + df["PARCEL_DONE_ORDERS"]

    driver_totals = (
        df.groupby("DRIVER_ID")
        .agg({"PARCEL_DONE_ORDERS": "sum", "ATTENDANCE": "sum"})
        .reset_index()
    )

    driver_totals["AVERAGE"] = round(
        driver_totals["PARCEL_DONE_ORDERS"] / driver_totals["ATTENDANCE"], 0
    )

    df = pd.merge(
        df, driver_totals[["DRIVER_ID", "AVERAGE"]], on="DRIVER_ID", how="left"
    )

    df["ORDER_AMOUNT"] = df.apply(lambda row: calculate_salary_surat(row, data), axis=1)

    df["BIKE_CHARGES"] = df.apply(lambda row: calculate_bike_charges(row, data), axis=1)

    df["REJECTION_AMOUNT"] = df.apply(
        lambda row: calculate_rejection(row, data), axis=1
    )

    df["BAD_ORDER_AMOUNT"] = df.apply(
        lambda row: calculate_bad_orders(row, data), axis=1
    )

    table = create_table(df).reset_index()

    table["BONUS"] = table.apply(lambda row: add_bonus(row, data), axis=1)

    table["PANALTIES"] = (
        table["IGCC_AMOUNT"] + table["REJECTION_AMOUNT"] + table["BAD_ORDER_AMOUNT"]
    )

    table["FINAL_AMOUNT"] = (
        table["ORDER_AMOUNT"]
        + table["BONUS"]
        - table["PANALTIES"]
        - table["BIKE_CHARGES"]
    )

    table["VENDER_FEE (@6%)"] = (table["FINAL_AMOUNT"] * 0.06) + (table["FINAL_AMOUNT"])

    table["FINAL PAYBLE AMOUNT (@18%)"] = (table["VENDER_FEE (@6%)"] * 0.18) + (
        table["VENDER_FEE (@6%)"]
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            table.to_excel(writer, sheet_name="Sheet1", index=False)

        file_id = uuid.uuid4()
        file_key = f"uploads/{file_id}/{file.filename}"

        new_file = SalaryFile(
            filekey=file_key,
            file_name=file.filename,
            file_type=".xlsx",
            created_at=datetime.now(),
        )

        db.add(new_file)

        db.commit()

        try:
            s3_client.upload_fileobj(temp_file, processed_bucket, file_key)

        except exception as e:
            return {"error": e}

    return {
        "message": "Successfully Calculated Salary for Zomato Surat",
        "file_id": file_id,
        "file_name": file.filename,
    }


#     return FileResponse(
#     temp_file.name,
#     media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#     headers={"Content-Disposition": f"attachment; filename=calculated_{file.filename}"},
#     filename=f"calculated_{file.filename}.xlsx",
# )


# return response


# def calculate_zomato_salary_structure2(df, structure, filename):
#     df["DATE"] = pd.to_datetime(df["DATE"])

#     df = df[(df["CITY_NAME"] == "Surat") & (df["CLIENT_NAME"] == "Zomato")]

#     df["Total_Earning"] = df.apply(lambda row: calculate_salary_surat(row, structure), axis=1)

#     df["Total_Orders"] = df["DOCUMENT_DONE_ORDER"] + df["PARCEL_DONE_ORDERS"]

#     table = create_table(df).reset_index()

#     table["Total_Earning"] = add_bonus(table)

#     with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
#         with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
#             table.to_excel(writer, sheet_name="Sheet1", index=False)

#         file_id = uuid.uuid4()
#         file_key = f"uploads/{file_id}/{filename}"

#         new_file = SalaryFile(
#             filekey=file_key,
#             file_name=filename,
#             file_type=".xlsx",
#             created_at=datetime.now(),
#         )

#         db.add(new_file)

#         db.commit()

#         try:
#             s3_client.upload_fileobj(temp_file, processed_bucket, file_key)

#         except exception as e:
#             return {"error": e}

#     return {
#             "message": "Successfully Calculated Salary for Zomato Surat",
#             "file_id": file_id,
#             "file_name": filename,
#         }


# return response


@surat_zomato_structure2_router.post("/zomato/new/structure2")
def claculate_salary_new(
    data: SuratZomatoStructureNew2 = Depends(), file: UploadFile = File(...)
):

    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y")

    df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "zomato")]

    df["TOTAL_ORDERS"] = df["DOCUMENT_DONE_ORDERS"] + df["PARCEL_DONE_ORDERS"]

    driver_totals = (
        df.groupby("DRIVER_ID")
        .agg({"PARCEL_DONE_ORDERS": "sum", "ATTENDANCE": "sum"})
        .reset_index()
    )

    driver_totals["AVERAGE"] = round(
        driver_totals["PARCEL_DONE_ORDERS"] / driver_totals["ATTENDANCE"], 0
    )

    df = pd.merge(
        df, driver_totals[["DRIVER_ID", "AVERAGE"]], on="DRIVER_ID", how="left"
    )

    if data.slab:

        df["ORDER_AMOUNT"] = df.apply(
            lambda row: calculate_salary_surat(row, data), axis=1
        )

    else:
        df["ORDER_AMOUNT"] = 0

    if data.vahicle_charges:

        df["BIKE_CHARGES"] = df.apply(
            lambda row: calculate_bike_charges(row, data), axis=1
        )
    else:
        df["BIKE_CHARGES"] = 0

    if data.rejection:

        df["REJECTION_AMOUNT"] = df.apply(
            lambda row: calculate_rejection(row, data), axis=1
        )
    else: 
        df["REJECTION_AMOUNT"] = 0

    if data.bad_order:

        df["BAD_ORDER_AMOUNT"] = df.apply(
            lambda row: calculate_bad_orders(row, data), axis=1
        )
    
    else:
        df["BAD_ORDER_AMOUNT"] = 0

    table = create_table(df).reset_index()

    if data.bonus:
        table["BONUS"] = table.apply(lambda row: add_bonus(row, data), axis=1)

    else: 
        table["BONUS"] = 0

    table["PANALTIES"] = table["IGCC_AMOUNT"] + table["REJECTION_AMOUNT"] + table["BAD_ORDER_AMOUNT"]

    table["FINAL_AMOUNT"] = (
        table["ORDER_AMOUNT"]
        + table["BONUS"]
        - table["PANALTIES"]
        - table["BIKE_CHARGES"]
    )

    table["VENDER_FEE (@6%)"] = (table["FINAL_AMOUNT"] * 0.06) + (table["FINAL_AMOUNT"])

    table["FINAL PAYBLE AMOUNT (@18%)"] = (table["VENDER_FEE (@6%)"] * 0.18) + (
        table["VENDER_FEE (@6%)"]
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            table.to_excel(writer, sheet_name="Sheet1", index=False)

        file_id = uuid.uuid4()
        file_key = f"uploads/{file_id}/{file.filename}"

        new_file = SalaryFile(
            filekey=file_key,
            file_name=file.filename,
            file_type=".xlsx",
            created_at=datetime.now(),
        )

        db.add(new_file)

        db.commit()

        try:
            s3_client.upload_fileobj(temp_file, processed_bucket, file_key)

        except exception as e:
            return {"error": e}

    return {
        "message": "Successfully Calculated Salary for Zomato Surat",
        "file_id": file_id,
        "file_name": file.filename,
    }
