from logging import exception
from fastapi import APIRouter, Body, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy import false
from app.salary_ahmedabad.schema.zomato import AhmedabadZomatoSchema
from app.salary_ahmedabad.view.zomato import (
    add_bonus,
    calculate_salary_ahmedabad,
    calculate_bike_charges,
    create_table,
)
import pandas as pd
import tempfile, json
import uuid
from app.salary_surat.model.model import SalaryFile
from decouple import config
from database.database import SessionLocal
from datetime import datetime
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file


ahmedabad_router = APIRouter()
db = SessionLocal()
row_bucket = config("ROW_BUCKET")
processed_bucket = config("PROCESSED_FILE_BUCKET")


@ahmedabad_router.post("/zomato/structure1")
def claculate_salary(
    data: AhmedabadZomatoSchema = Depends(), file: UploadFile = File(...)
):

    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y")

    df = df[(df["CITY_NAME"] == "ahmedabad") & (df["CLIENT_NAME"] == "zomato")]

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

    table["BONUS"] = table.apply(lambda row: add_bonus(row, data), axis=1)

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
