from logging import exception
from fastapi import APIRouter, Body, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import false
from app.salary_ahmedabad.schema.zomato import AhmedabadZomatoSchema, AhmedabadZomatoSchema2
from app.salary_ahmedabad.view.zomato import (
    add_bonus,
    add_bonus_old,
    calculate_salary_ahmedabad,
    calculate_bike_charges,
    create_table,
    calculate_amount_for_ahmedabad_rental_model,
    calculate_bike_charges_for_rental_model,
    calculate_bad_orders_rantal,
    calculate_rejection_rantal
)
import pandas as pd
import tempfile, json
import uuid
from app.salary_surat.model.model import SalaryFile
from decouple import config
from database.database import SessionLocal
from datetime import datetime
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
from app import setting


ahmedabad_router = APIRouter()
db = SessionLocal()
row_bucket = setting.ROW_BUCKET
processed_bucket = setting.PROCESSED_FILE_BUCKET


@ahmedabad_router.post("/zomato/structure1")
def claculate_salary(
    data: AhmedabadZomatoSchema = Depends(), file: UploadFile = File(...)
):

    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y")

    df = df[(df["CITY_NAME"] == "ahmedabad") & (df["CLIENT_NAME"] == "zomato")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "Zomato client not found")

    df["TOTAL_ORDERS"] = df["DOCUMENT_DONE_ORDERS"] + df["PARCEL_DONE_ORDERS"]

    driver_totals = (
        df.groupby("DRIVER_ID")
        .agg({"PARCEL_DONE_ORDERS": "sum", "ATTENDANCE": "sum"})
        .reset_index()
    )

    driver_totals["AVERAGE"] = round(
        driver_totals["PARCEL_DONE_ORDERS"] / driver_totals["ATTENDANCE"]
    ,0)

    df = pd.merge(
        df, driver_totals[["DRIVER_ID", "AVERAGE"]], on="DRIVER_ID", how="left"
    )
    
    df["ORDER_AMOUNT"] = df.apply(
        lambda row: calculate_salary_ahmedabad(row, data), axis=1
    )

    df["BIKE_CHARGES"] = df.apply(lambda row: calculate_bike_charges(row, data), axis=1)

    table = create_table(df).reset_index()

    table["BONUS"] = table.apply(lambda row: add_bonus_old(row, data), axis=1)

    table["PANALTIES"] = table["IGCC_AMOUNT"] + table["BIKE_CHARGES"]

    table["FINAL_AMOUNT"] = (
        table["ORDER_AMOUNT"]
        + table["BONUS"]
        - table["PANALTIES"]
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
        "message": "Successfully Calculated Salary for Zomato Ahmedabad",
        "file_id": file_id,
        "file_name": file.filename,
        "file_key" : file_key
    }

    # content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # response = FileResponse(temp_file.name, media_type=content_type)
    # response.headers["Content-Disposition"] = (
    #     'attachment; filename="month_year_city.xlsx"'
    # )

    # return response


@ahmedabad_router.post("/zomato/v2/structure1")
def claculate_salary_structure3(
    file: UploadFile = File(...),
    include_slab : bool = Form(False),
    zomato_first_order_start: int = Form(1) ,
    zomato_first_order_end: int = Form(19),
    zomato_first_week_amount: int = Form(30),
    zomato_first_weekend_amount: int = Form(32),
    zomato_second_order_start:int = Form(20),
    zomato_second_order_end:int = Form(25),
    zomato_second_week_amount: int = Form(25),
    zomato_second_weekend_amount: int = Form(27),
    zomato_order_greter_than: int = Form(26),
    zomato_third_week_amount: int = Form(30),
    zomato_third_weekend_amount: int = Form(32),
    include_vahicle_charges: bool = Form(False),
    fulltime_average: int = Form(20),
    fulltime_greter_than_order : int = Form(20),
    vahicle_charges_fulltime : int = Form(100),
    partime_average: int = Form(11),
    partime_greter_than_order: int = Form(12),
    vahicle_charges_partime: int = Form(70),
    include_bonus : bool = Form(False),
    bonus_order_fulltime: int = Form(700),
    bonus_amount_fulltime: int = Form(1000),
    bonus_order_partime: int = Form(400),
    bonus_amount_partime: int = Form(500),
    include_rejection : bool = Form(False),
    rejection_orders: int = Form(2),
    rejection_amount : int = Form(20),
    include_bad_order : bool = Form(False),
    bad_orders : int = Form(2),
    bad_orders_amount : int = Form(20),
):

    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y")

    df = df[(df["CITY_NAME"] == "ahmedabad") & (df["CLIENT_NAME"] == "zomato")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "Zomato client not found")

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

    if include_slab:

        df["ORDER_AMOUNT"] = df.apply(
            lambda row: calculate_amount_for_ahmedabad_rental_model(
                row,
                zomato_first_order_start,
                zomato_first_order_end,
                zomato_first_week_amount,
                zomato_first_weekend_amount,
                zomato_second_order_start,
                zomato_second_order_end,
                zomato_second_week_amount,
                zomato_second_weekend_amount,
                zomato_order_greter_than,
                zomato_third_week_amount,
                zomato_third_weekend_amount
            ), axis=1
        )

    else:
        df["ORDER_AMOUNT"] = 0

    if include_vahicle_charges:

        df["BIKE_CHARGES"] = df.apply(
            lambda row: calculate_bike_charges_for_rental_model(
                row,
                fulltime_average,
                fulltime_greter_than_order,
                vahicle_charges_fulltime,
                partime_average,
                partime_greter_than_order,
                vahicle_charges_partime 
            ), axis=1
        )
    else:
        df["BIKE_CHARGES"] = 0

    if include_rejection:

        df["REJECTION_AMOUNT"] = df.apply(
            lambda row: calculate_rejection_rantal(
                row,
                rejection_orders,
                rejection_amount
            ), axis=1
        )
    else: 
        df["REJECTION_AMOUNT"] = 0

    if include_bad_order:

        df["BAD_ORDER_AMOUNT"] = df.apply(
            lambda row: calculate_bad_orders_rantal(
                row,
                bad_orders,
                bad_orders_amount 
            ), axis=1
        )
    
    else:
        df["BAD_ORDER_AMOUNT"] = 0


    table = create_table(df).reset_index()

    if include_bonus:
        table["BONUS"] = table.apply(lambda row: add_bonus(
            row,
            bonus_order_fulltime,
            bonus_amount_fulltime,
            bonus_order_partime,
            bonus_amount_partime
        ), axis=1)

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
        "message": "Successfully Calculated Salary for Zomato Ahmedabad",
        "file_id": file_id,
        "file_name": file.filename,
        "file_key" : file_key
    }