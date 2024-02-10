from datetime import datetime
from distutils.command import upload
import json
from os import name, read
from sys import exception
from urllib import response
from fastapi import APIRouter, UploadFile, Form, File, status, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from pydantic import Json
from sqlalchemy import false, table
from ..view.view import (
    is_weekend,
    week_or_weekend,
    calculate_amount_for_zomato_surat,
    calculate_amount_for_surat_swiggy,
    calculate_amount_for_bbnow_surat,
    calculate_amount_for_ecom_surat,
    calculate_amount_for_flipkart_surat,
    calculate_document_amount,
    calculate_parcel_amount,
)
import io
from fastapi.responses import FileResponse
import tempfile
from typing import List
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
import uuid
from database.database import SessionLocal
from app.salary_surat.model.model import SalaryFile
from decouple import config


salary_router = APIRouter()
db = SessionLocal()
row_bucket = config("ROW_BUCKET")
processed_bucket = config("PROCESSED_FILE_BUCKET")


@salary_router.post("/zomato/structure1")
async def calculate_zomato_surat(
    file: UploadFile = File(...),
    first_order_from: int = Form(1),
    first_order_to: int = Form(19),
    first_week_amount: int = Form(20),
    first_weekend_amount: int = Form(22),
    second_order_from: int = Form(20),
    second_order_to: int = Form(25),
    second_week_amount: int = Form(25),
    second_weekend_amount: int = Form(27),
    order_grether_than: int = Form(25),
    week_amount: int = Form(30),
    weekend_amount: int = Form(32),
    maximum_rejection: int = Form(2),
    rejection_amount: int = Form(10),
    maximum_bad_orders: int = Form(2),
    bad_order_amount: int = Form(10),
):

    df = pd.read_excel(file.file)
    df["DATE"] = pd.to_datetime(df["DATE"])

    df = df[(df["CITY NAME"] == "Surat") & (df["CLIENT NAME"] == "Zomato")]
    df["Total_Earning"] = df.apply(
        calculate_amount_for_zomato_surat,
        args=(
            first_order_from,
            first_order_to,
            first_week_amount,
            first_weekend_amount,
            second_order_from,
            second_order_to,
            second_week_amount,
            second_weekend_amount,
            order_grether_than,
            week_amount,
            weekend_amount,
            maximum_rejection,
            rejection_amount,
            bad_order_amount,
            maximum_bad_orders,
        ),
        axis=1,
    )

    df["Total_Orders"] = df["Document DONE ORDERS"] + df["Parcel DONE ORDERS"]

    table = pd.pivot_table(
        data=df,
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
        },
    ).reset_index()

    zomato_surat_table = pd.DataFrame(table)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            zomato_surat_table.to_excel(writer, sheet_name="Sheet1", index=False)

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


@salary_router.post("/swiggy/structure1/{file_id}/{file_name}")
async def calculate_swiggy_surat(
    file_id: str,
    file_name: str,
    file: UploadFile = File(...),
    first_order_from: int = Form(1),
    first_order_to: int = Form(19),
    first_week_amount: int = Form(20),
    first_weekend_amount: int = Form(22),
    second_order_from: int = Form(20),
    second_order_to: int = Form(25),
    second_week_amount: int = Form(25),
    second_weekend_amount: int = Form(27),
    order_grether_than: int = Form(25),
    week_amount: int = Form(30),
    weekend_amount: int = Form(32),
    maximum_rejection: int = Form(2),
    rejection_amount: int = Form(10),
    maximum_bad_orders: int = Form(2),
    bad_order_amount: int = Form(10),
):

    df = pd.read_excel(file.file)
    df["DATE"] = pd.to_datetime(df["DATE"])

    df = df[(df["CITY NAME"] == "Surat") & (df["CLIENT NAME"] == "Swiggy")]
    df["Total_Earning"] = df.apply(
        calculate_amount_for_surat_swiggy,
        args=(
            first_order_from,
            first_order_to,
            first_week_amount,
            first_weekend_amount,
            second_order_from,
            second_order_to,
            second_week_amount,
            second_weekend_amount,
            order_grether_than,
            week_amount,
            weekend_amount,
            maximum_rejection,
            rejection_amount,
            bad_order_amount,
            maximum_bad_orders,
        ),
        axis=1,
    )

    df["Total_Orders"] = df["Document DONE ORDERS"] + df["Parcel DONE ORDERS"]

    table = pd.pivot_table(
        data=df,
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
        },
    )

    table_reset = table.reset_index()

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()
    swiggy_surat_table = pd.DataFrame(table_reset)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, swiggy_surat_table], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

            # file_key = f"uploads/{file_id}/modified.xlsx"
        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {"file_id": file_id, "file_name": file_name}


@salary_router.post("/bbnow/structure1/{file_id}/{file_name}")
async def calculate_bb_now_surat(
    file_id: str,
    file_name: str,
    file: UploadFile = File(...),
    orders_less_then: int = Form(13),
    order_amount1: int = Form(400),
    from_order: int = Form(1),
    to_order: int = Form(14),
    order_amount2: int = Form(30),
    order_grether_than: int = Form(15),
    order_amount3: int = Form(35),
):

    df = pd.read_excel(file.file)

    df["Total_Orders"] = df["Document DONE ORDERS"] + df["Parcel DONE ORDERS"]

    table = pd.pivot_table(
        data=df[(df["CLIENT NAME"] == "BB now") & (df["CITY NAME"] == "Surat")],
        index=[
            "DRIVER_ID",
            "DRIVER_NAME",
            "CITY NAME",
            "CLIENT NAME",
            "REJECTION",
            "BAD ORDER",
        ],
        aggfunc={
            "Total_Orders": "sum",
            "Parcel DONE ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN ORDER": "sum",
            "IGCC AMOUNT": "sum",
            "ATTENDANCE": "sum",
        },
    ).reset_index()

    attendance_count = (
        df[df["CLIENT NAME"] == "BB now"]["DRIVER_ID"].value_counts().reset_index()
    )
    attendance_count.columns = ["DRIVER_ID", "Attendance"]

    result = pd.merge(table, attendance_count, on="DRIVER_ID", how="left")

    result["Average"] = round(result["Parcel DONE ORDERS"] / result["Attendance"])

    result["Total_Earning"] = result.apply(
        calculate_amount_for_bbnow_surat,
        args=(
            orders_less_then,
            order_amount1,
            from_order,
            to_order,
            order_amount2,
            order_grether_than,
            order_amount3,
        ),
        axis=1,
    )

    final_result = result[
        [
            "DRIVER_ID",
            "CITY NAME",
            "CLIENT NAME",
            "REJECTION",
            "BAD ORDER",
            "Total_Earning",
            "Total_Orders",
            "Parcel DONE ORDERS",
            "CUSTOMER_TIP",
            "RAIN ORDER",
            "IGCC AMOUNT",
            "ATTENDANCE",
        ]
    ]

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)
    # except exception as e:
    #     return {"error" : e}

    file_data = response["Body"].read()

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, final_result], ignore_index=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {
        "message": "calculated successfully",
        "file_id": file_id,
        "file_name": file_name,
    }


@salary_router.post("/ecom/structure1/{file_id}/{file_name}")
def calculate_ecom_surat(
    file_id: str,
    file_name: str,
    file: UploadFile = File(...),
    from_order: int = Form(1),
    to_order: int = Form(40),
    first_amount: int = Form(14),
    second_condition_from: int = Form(41),
    second_condition_to: int = Form(55),
    second_condition_amount: int = Form(15),
    third_condition: int = Form(56),
    third_condition_amount: int = Form(16),
):
    df = pd.read_excel(file.file)

    df = df[(df["CITY NAME"] == "Surat") & (df["CLIENT NAME"] == "E-com")]
    df["Total_Earning"] = df.apply(
        calculate_amount_for_ecom_surat,
        args=(
            from_order,
            to_order,
            first_amount,
            second_condition_from,
            second_condition_to,
            second_condition_amount,
            third_condition,
            third_condition_amount,
        ),
        axis=1,
    )

    df["Total_Orders"] = df["Document DONE ORDERS"] + df["Parcel DONE ORDERS"]

    table = pd.pivot_table(
        data=df,
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
        },
    )

    table_reset = table.reset_index()

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()
    ecom_surat_table = pd.DataFrame(table_reset)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, ecom_surat_table], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {"file_id": file_id, "file_name": file_name}


@salary_router.post("/flipkart/structure1/{file_id}/{file_name}")
def calculate_flipcart_surat(
    file_id: str,
    file_name: str,
    file: UploadFile = File(...),
    from_order: int = Form(1),
    to_order: int = Form(40),
    first_amount: int = Form(12),
    second_condition_from: int = Form(41),
    second_condition_to: int = Form(55),
    second_condition_amount: int = Form(13),
    third_condition: int = Form(55),
    third_condition_amount: int = Form(14),
):
    df = pd.read_excel(file.file)

    df = df[(df["CITY NAME"] == "Surat") & (df["CLIENT NAME"] == "Flipkart")]
    df["Total_Earning"] = df.apply(
        calculate_amount_for_flipkart_surat,
        args=(
            from_order,
            to_order,
            first_amount,
            second_condition_from,
            second_condition_to,
            second_condition_amount,
            third_condition,
            third_condition_amount,
        ),
        axis=1,
    )

    df["Total_Orders"] = df["Document DONE ORDERS"] + df["Parcel DONE ORDERS"]

    table = pd.pivot_table(
        data=df,
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
        },
    )

    table_reset = table.reset_index()

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()
    flipkart_surat_table = pd.DataFrame(table_reset)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, flipkart_surat_table], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {"file_id": file_id, "file_name": file_name}


@salary_router.post("/bluedart/structure/{file_id}/{file_name}")
def calculate_bluedart(
    file_id: str,
    file_name: str,
    file: UploadFile = File(...),
    from_order_document: int = Form(1),
    to_order_document: int = Form(44),
    first_amount_document: int = Form(5),
    second_condition_from_document: int = Form(45),
    second_condition_to_document: int = Form(64),
    second_condition_amount_document: int = Form(6),
    third_condition_from_document: int = Form(65),
    third_condition_to_document: int = Form(79),
    third_condtion_amount_document: int = Form(7),
    order_greater_than_document: int = Form(80),
    order_amount_document: float = Form(7.5),
    from_order_parcel: int = Form(1),
    to_order_parcel: int = Form(20),
    first_amount_parcel: int = Form(10),
    second_condition_from_parcel: int = Form(21),
    second_condition_to_parcel: int = Form(35),
    second_condition_amount_parcel: int = Form(12),
    third_condition_from_parcel: int = Form(36),
    third_condition_to_parcel: int = Form(45),
    third_condtion_amount_parcel: int = Form(13),
    order_greater_than_parcel: int = Form(46),
    order_amount_parcel: float = Form(13.5),
):
    df = pd.read_excel(file.file)

    df = df[df["CLIENT NAME"].isin(["Bluedart Biker", "Bluedart ven"])]
    df["document_amount"] = df.apply(
        calculate_document_amount,
        args=(
            from_order_document,
            to_order_document,
            first_amount_document,
            second_condition_from_document,
            second_condition_to_document,
            second_condition_amount_document,
            third_condition_from_document,
            third_condition_to_document,
            third_condtion_amount_document,
            order_greater_than_document,
            order_amount_document,
        ),
        axis=1,
    )

    df["parcel_amount"] = df.apply(
        calculate_parcel_amount,
        args=(
            from_order_parcel,
            to_order_parcel,
            first_amount_parcel,
            second_condition_from_parcel,
            second_condition_to_parcel,
            second_condition_amount_parcel,
            third_condition_from_parcel,
            third_condition_to_parcel,
            third_condtion_amount_parcel,
            order_greater_than_parcel,
            order_amount_parcel,
        ),
        axis=1,
    )

    df["Total_Earning"] = df["document_amount"] + df["parcel_amount"]

    df["Total_Orders"] = df["Document DONE ORDERS"] + df["Parcel DONE ORDERS"]

    table = pd.pivot_table(
        data=df,
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
        },
    )

    table_reset = table.reset_index()

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()
    bluedart_table = pd.DataFrame(table_reset)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, bluedart_table], ignore_index=True)

    df3["Vender_fee (@6%)"] = (df3["Total_Earning"] * 0.06) + (df3["Total_Earning"])

    df3["Final Payble Amount (@18%)"] = (df3["Vender_fee (@6%)"] * 0.18) + (
        df3["Vender_fee (@6%)"]
    )

    column_order = [
        "CITY NAME",
        "CLIENT NAME",
        "DRIVER_ID",
        "DRIVER_NAME",
        "ATTENDANCE",
        "Total_Orders",
        "BAD ORDER",
        "REJECTION",
        "IGCC AMOUNT",
        "CUSTOMER_TIP",
        "Total_Earning",
        "Vender_fee (@6%)",
        "Final Payble Amount (@18%)",
    ]

    df3 = df3[column_order]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return FileResponse(
        temp_file.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=calculated_{file_name}"},
        filename=f"calculated_{file_name}.xlsx",
    )


@salary_router.get("/samplefile")
def getfile():
    file_key = f"uploads/month_year_city.xlsx"
    response = s3_client.get_object(Bucket=row_bucket, Key=file_key)
    file_data = response["Body"].read()
    df = pd.read_excel(io.BytesIO(file_data))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False)

    content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = FileResponse(temp_file.name, media_type=content_type)
    response.headers["Content-Disposition"] = (
        'attachment; filename="month_year_city.xlsx"'
    )

    return response
