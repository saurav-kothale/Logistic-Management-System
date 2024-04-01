from ast import arg
from datetime import datetime
from sys import exception
from fastapi import APIRouter, UploadFile, Form, File, HTTPException, status
import pandas as pd
from ..view.view import (
    calculate_amount_for_zomato_surat,
    calculate_amount_for_surat_swiggy,
    calculate_amount_for_bbnow_surat,
    calculate_amount_for_ecom_surat,
    calculate_amount_for_flipkart_surat,
    calculate_document_amount,
    calculate_parcel_amount,
    calculate_panalties,
    calculate_order_for_less_amount,
    calculate_amount_bluedart_van,
    calculate_uptown
)
import io
from fastapi.responses import FileResponse
import tempfile
from app.file_system.s3_events import s3_client
import uuid
from database.database import SessionLocal
from app.salary_surat.model.model import SalaryFile
from decouple import config
from app import setting


salary_router = APIRouter()
db = SessionLocal()
row_bucket = setting.ROW_BUCKET
processed_bucket = setting.PROCESSED_FILE_BUCKET




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
    df["DATE"] = pd.to_datetime(df["DATE"], format="%d/%m/%Y")

    df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "zomato")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "Zomato client not found")
    
    df["ORDER_AMOUNT"] = df.apply(
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
        ),
        axis=1,
    )

    df["PANALTIES"] = df.apply(
        calculate_panalties,
        args=(
            maximum_rejection,
            rejection_amount,
            bad_order_amount,
            maximum_bad_orders,
        ),
        axis=1,
    )

    df["TOTAL_ORDERS"] = df["DONE_DOCUMENT_ORDERS"] + df["DONE_PARCEL_ORDERS"]

    table = pd.pivot_table(
        data=df,
        index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
        aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "ORDER_AMOUNT": "sum",
            "DONE_PARCEL_ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
            "PANALTIES": "sum",
        },
    ).reset_index()

    table["FINAL_AMOUNT"] = table["ORDER_AMOUNT"] - table["PANALTIES"]

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
        "file_key" : file_key
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
    df["DATE"] = pd.to_datetime(df["DATE"], format="%d/%m/%Y")

    df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "swiggy")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "Swiggy client not found")
    
    df["ORDER_AMOUNT"] = df.apply(
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

    df["PANALTIES"] = df.apply(
        calculate_panalties,
        args=(
            maximum_rejection,
            rejection_amount,
            bad_order_amount,
            maximum_bad_orders,
        ),
        axis=1,
    )

    df["TOTAL_ORDERS"] = df["DONE_DOCUMENT_ORDERS"] + df["DONE_PARCEL_ORDERS"]

    table = pd.pivot_table(
        data=df,
        index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
        aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "ORDER_AMOUNT": "sum",
            "DONE_PARCEL_ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
            "PANALTIES": "sum",
        },
    )

    table_reset = table.reset_index()

    table_reset["FINAL_AMOUNT"] = table_reset["ORDER_AMOUNT"] - table_reset["PANALTIES"]

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

    return {"file_id": file_id, "file_name": file_name, "file_key" : file_key}


@salary_router.post("/bbnow/structure1/{file_id}/{file_name}")
async def calculate_bb_now_surat(
    file_id: str,
    file_name: str,
    file: UploadFile = File(...),
    average_order: int = Form(13),
    average_amount: int = Form(400),
    from_order: int = Form(1),
    to_order: int = Form(14),
    order_amount2: int = Form(30),
    order_grether_than: int = Form(15),
    order_amount3: int = Form(35),
):

    df = pd.read_excel(file.file)

    df = df[(df["CLIENT_NAME"] == "bb now") & (df["CITY_NAME"] == "surat")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "BB Now client not found")

    driver_totals = (
        df.groupby("DRIVER_ID")
        .agg({"DONE_PARCEL_ORDERS": "sum", "ATTENDANCE": "sum"})
        .reset_index()
    )

    driver_totals["AVERAGE"] = (
        driver_totals["DONE_PARCEL_ORDERS"] / driver_totals["ATTENDANCE"] 
    )

    new_df = pd.merge(
        df, driver_totals[["DRIVER_ID", "AVERAGE"]], on="DRIVER_ID", how="left"
    )



    # table = pd.pivot_table(
    #     data=df[(df["CLIENT_NAME"] == "bb now") & (df["CITY_NAME"] == "surat")],
    #     index=[
    #         "DRIVER_ID",
    #         "DRIVER_NAME",
    #         "CITY_NAME",
    #         "CLIENT_NAME",
    #         # "REJECTION",
    #         # "BAD_ORDER",
    #     ],
    #     aggfunc={
    #         "TOTAL_ORDERS": "sum",
    #         "DONE_PARCEL_ORDERS": "sum",
    #         "CUSTOMER_TIP": "sum",
    #         "RAIN_ORDER": "sum",
    #         "IGCC_AMOUNT": "sum",
    #         "ATTENDANCE": "sum",
    #         "REJECTION" : "sum",
    #         "BAD_ORDER": "sum"
    #     },
    # ).reset_index()

    # attendance_count = (
    #     df[df["CLIENT_NAME"] == "bb now"]["DRIVER_ID"].value_counts().reset_index()
    # )
    # attendance_count.columns = ["DRIVER_ID", "ATTENDANCE"]

    # breakpoint()

    # result = pd.merge(table, attendance_count, on="DRIVER_ID", how="left")

    # table["AVERAGE"] = round(table["DONE_PARCEL_ORDERS"] / table["ATTENDANCE"])

    new_df["ORDER_AMOUNT"] = new_df.apply(
        calculate_amount_for_bbnow_surat,
        args=(
            from_order,
            to_order,
            order_amount2,
            order_grether_than,
            order_amount3,
        ),
        axis=1,
    )

    new_df["TOTAL_ORDERS"] = new_df["DONE_PARCEL_ORDERS"]

    table = pd.pivot_table(
        data=new_df,
        index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
        aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "ORDER_AMOUNT": "sum",
            "DONE_PARCEL_ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "AVERAGE": "mean",
            "TOTAL_ORDERS" : "sum"
        },
    ).reset_index()

    table["ORDER_AMOUNT"] = table.apply(
        lambda row: (
            calculate_order_for_less_amount(
                row,
                average_order,
                average_amount
            )
            if row["AVERAGE"] < average_order 
            else row["ORDER_AMOUNT"]
        ),
        axis=1,
    )

    table["FINAL_AMOUNT"] = table["ORDER_AMOUNT"]

    table["VENDER_FEE (@6%)"] = (table["FINAL_AMOUNT"] * 0.06) + (table["FINAL_AMOUNT"])

    table["FINAL PAYBLE AMOUNT (@18%)"] = (table["VENDER_FEE (@6%)"] * 0.18) + (
        table["VENDER_FEE (@6%)"]
    )

    # final_result = table[
    #     [
    #         "DRIVER_ID",
    #         "CITY_NAME",
    #         "CLIENT_NAME",
    #         "REJECTION",
    #         "BAD_ORDER",
    #         "ORDER_AMOUNT",
    #         "TOTAL_ORDERS",
    #         "DONE_PARCEL_ORDERS",
    #         "CUSTOMER_TIP",
    #         "RAIN_ORDER",
    #         "IGCC_AMOUNT",
    #         "ATTENDANCE",
    #         "FINAL_AMOUNT",
    #     ]
    # ]

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)
    # except exception as e:
    #     return {"error" : e}

    file_data = response["Body"].read()

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, table], ignore_index=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {
        "message": "BB NOW calculated successfully",
        "file_id": file_id,
        "file_name": file_name,
        "file_key" : file_key
    }

    # with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
    #     with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
    #         df3.to_excel(writer, sheet_name="Sheet1", index=False)

    #         # s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    #     content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #     response = FileResponse(temp_file.name, media_type=content_type)
    #     response.headers["Content-Disposition"] = (
    #         'attachment; filename="month_year_city.xlsx"'
    #     )

    # return response


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
    df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "e com")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "Ecom client not found")
    
    df["ORDER_AMOUNT"] = df.apply(
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

    df["TOTAL_ORDERS"] = df["DONE_DOCUMENT_ORDERS"] + df["DONE_PARCEL_ORDERS"]

    table = pd.pivot_table(
        data=df,
        index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
        aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "ORDER_AMOUNT": "sum",
            "DONE_PARCEL_ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
        },
    )

    table_reset = table.reset_index()

    table_reset["FINAL_AMOUNT"] = table_reset["ORDER_AMOUNT"]

    table_reset["VENDER_FEE (@6%)"] = (table_reset["FINAL_AMOUNT"] * 0.06) + (
        table_reset["FINAL_AMOUNT"]
    )

    table_reset["FINAL PAYBLE AMOUNT (@18%)"] = (
        table_reset["VENDER_FEE (@6%)"] * 0.18
    ) + (table_reset["VENDER_FEE (@6%)"])

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

    return {
        "message" : "Successfully calculate salary for Ecom",
        "file_id": file_id,
        "file_name": file_name,
        "file_key" : file_key
    }

    # with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
    #     with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
    #         df3.to_excel(writer, sheet_name="Sheet1", index=False)

    #         # s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    #     content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #     response = FileResponse(temp_file.name, media_type=content_type)
    #     response.headers["Content-Disposition"] = (
    #         'attachment; filename="month_year_city.xlsx"'
    # )

    # return response


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

    df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "flipkart")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "Flipkart client not found")
    
    df["ORDER_AMOUNT"] = df.apply(
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

    df["TOTAL_ORDERS"] = df["DONE_DOCUMENT_ORDERS"] + df["DONE_PARCEL_ORDERS"]

    table = pd.pivot_table(
        data=df,
        index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
        aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "ORDER_AMOUNT": "sum",
            "DONE_PARCEL_ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
        },
    )

    table_reset = table.reset_index()
    table_reset["FINAL_AMOUNT"] = table_reset["ORDER_AMOUNT"]

    table_reset["VENDER_FEE (@6%)"] = (table_reset["FINAL_AMOUNT"] * 0.06) + (
        table_reset["FINAL_AMOUNT"]
    )

    table_reset["FINAL PAYBLE AMOUNT (@18%)"] = (
        table_reset["VENDER_FEE (@6%)"] * 0.18
    ) + (table_reset["VENDER_FEE (@6%)"])

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

    return {
        "message" : "Sucessfully Calculated Salary for Flipkart",
        "file_id": file_id, 
        "file_name": file_name, 
        "file_key" : file_key
    }
    # with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
    #     with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
    #         df3.to_excel(writer, sheet_name="Sheet1", index=False)

    #         # s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    #     content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #     response = FileResponse(temp_file.name, media_type=content_type)
    #     response.headers["Content-Disposition"] = (
    #         'attachment; filename="month_year_city.xlsx"'
    # )

    # return response


@salary_router.post("/bluedart/biker/structure/{file_id}/{file_name}")
def calculate_bluedart_biker(
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

    df = df[df["CLIENT_NAME"].isin(["bluedart biker",])]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "BlueDart Biker client not found")
    
    df["DOCUMENT_AMOUNT"] = df.apply(
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

    df["PARCEL_AMOUNT"] = df.apply(
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

    df["ORDER_AMOUNT"] = df["DOCUMENT_AMOUNT"] + df["PARCEL_AMOUNT"]

    df["TOTAL_ORDERS"] = df["DONE_DOCUMENT_ORDERS"] + df["DONE_PARCEL_ORDERS"]

    table = pd.pivot_table(
        data=df,
        index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
        aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "ORDER_AMOUNT": "sum",
            "DONE_PARCEL_ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
        },
    )

    table_reset = table.reset_index()

    table_reset["FINAL_AMOUNT"] = table_reset["ORDER_AMOUNT"]

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()
    bluedart_table = pd.DataFrame(table_reset)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, bluedart_table], ignore_index=True)

    df3["VENDER_FEE (@6%)"] = (df3["FINAL_AMOUNT"] * 0.06) + (df3["FINAL_AMOUNT"])

    df3["FINAL PAYBLE AMOUNT (@18%)"] = (df3["VENDER_FEE (@6%)"] * 0.18) + (
        df3["VENDER_FEE (@6%)"]
    )

    desire_order = [
        "CITY_NAME",
        "CLIENT_NAME",
        "DRIVER_ID",
        "DRIVER_NAME",
        "ATTENDANCE",
        "TOTAL_ORDERS",
        "ORDER_AMOUNT",
        "BAD_ORDER",
        "BAD_ORDER_AMOUNT",
        "REJECTION",
        "REJECTION_AMOUNT",
        "IGCC_AMOUNT",
        "CUSTOMER_TIP",
        "BONUS",
        "BIKE_CHARGES",
        "PANALTIES",
        "FINAL_AMOUNT",
        "VENDER_FEE (@6%)",
        "FINAL PAYBLE AMOUNT (@18%)",
    ]

    # common_columns = list(set(desire_order).intersection(df3.columns))

    # df3 = df3[common_columns]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    # return FileResponse(
    #     temp_file.name,
    #     media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #     headers={"Content-Disposition": f"attachment; filename=calculated_{file_name}"},
    #     filename=f"calculated_{file_name}.xlsx",
    # )
    return {
        "message" : "Sucessfully Calculated Salary for BlueDart-Bike",
        "file_id": file_id, 
        "file_name": file_name, 
        "file_key" : file_key
    }


@salary_router.post("/bluedart/van/structure/{file_id}/{file_name}")
def calculate_bluedart_van(
    file_id: str,
    file_name: str,
    file: UploadFile = File(...),
    fixed_salary : int = Form(15000),
    days : int = Form(26)
):
    df = pd.read_excel(file.file)

    df = df[df["CLIENT_NAME"] == "bluedart van"]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "BlueDart Van client not found")
    

    df["TOTAL_ORDERS"] = df["DONE_DOCUMENT_ORDERS"] + df["DONE_PARCEL_ORDERS"]

    table = pd.pivot_table(
        data=df,
        index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
        aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "DONE_PARCEL_ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
        },
    )

    table_reset = table.reset_index()


    table_reset["ORDER_AMOUNT"] = table_reset.apply(

        calculate_amount_bluedart_van,

        args=(
            fixed_salary,
            days
        ),

        axis= 1
    )

    table_reset["FINAL_AMOUNT"] = table_reset["ORDER_AMOUNT"]

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()

    bluedart_table = pd.DataFrame(table_reset)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, bluedart_table], ignore_index=True)

    df3["VENDER_FEE (@6%)"] = (df3["FINAL_AMOUNT"] * 0.06) + (df3["FINAL_AMOUNT"])

    df3["FINAL PAYBLE AMOUNT (@18%)"] = (df3["VENDER_FEE (@6%)"] * 0.18) + (
        df3["VENDER_FEE (@6%)"]
    )
    

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

        s3_client.upload_file(temp_file.name, processed_bucket, file_key)


    return {
        "message" : "Sucessfully Calculated Salary for BlueDart Van",
        "file_id": file_id, 
        "file_name": file_name, 
        "file_key" : file_key
    }


@salary_router.post("/uptown_fresh/structure/{file_id}/{file_name}")
def calculate_uptownfresh(
    file_id: str,
    file_name: str,
    file: UploadFile = File(...),
    fixed_salary : int = Form(15000),
    days : int = Form(26)
):
    df = pd.read_excel(file.file)

    df = df[df["CLIENT_NAME"] == "uptown fresh"]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "Uptown Fresh client not found")
    

    df["TOTAL_ORDERS"] = df["DONE_DOCUMENT_ORDERS"] + df["DONE_PARCEL_ORDERS"]

    table = pd.pivot_table(
        data=df,
        index=["DRIVER_ID", "DRIVER_NAME", "CLIENT_NAME", "CITY_NAME"],
        aggfunc={
            "REJECTION": "sum",
            "BAD_ORDER": "sum",
            "DONE_PARCEL_ORDERS": "sum",
            "CUSTOMER_TIP": "sum",
            "RAIN_ORDER": "sum",
            "IGCC_AMOUNT": "sum",
            "ATTENDANCE": "sum",
            "TOTAL_ORDERS": "sum",
        },
    )

    table_reset = table.reset_index()


    table_reset["ORDER_AMOUNT"] = table_reset.apply(

        calculate_uptown,

        args=(
            fixed_salary,
            days
        ),

        axis= 1
    )

    table_reset["FINAL_AMOUNT"] = table_reset["ORDER_AMOUNT"]

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()

    bluedart_table = pd.DataFrame(table_reset)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, bluedart_table], ignore_index=True)

    df3["VENDER_FEE (@6%)"] = (df3["FINAL_AMOUNT"] * 0.06) + (df3["FINAL_AMOUNT"])

    df3["FINAL PAYBLE AMOUNT (@18%)"] = (df3["VENDER_FEE (@6%)"] * 0.18) + (
        df3["VENDER_FEE (@6%)"]
    )
    

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

        s3_client.upload_file(temp_file.name, processed_bucket, file_key)


    return {
        "message" : "Sucessfully Calculated Salary for Uptown Fresh",
        "file_id": file_id, 
        "file_name": file_name, 
        "file_key" : file_key
    }    
        


@salary_router.get("/samplefile/{city}")
def getfile(
    city : str
):
    if city == "ahmedabad":
        file_key = f"uploads/50812460-485a-41f2-8610-6282cae96e67/00_0000_ahmedabad.xlsx"
        response = s3_client.get_object(Bucket=row_bucket, Key=file_key)
    
    elif city == "surat":
        file_key = f"uploads/2d477cf3-f383-49cb-8a4b-d58576fc2fb0/00_0000_surat.xlsx"
        response = s3_client.get_object(Bucket=row_bucket, Key=file_key)

   
    file_data = response["Body"].read()
    df = pd.read_excel(io.BytesIO(file_data))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False)

    return FileResponse(
        temp_file.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=00_0000_{city}.xlsx"},
        filename=f"00_0000_{city}.xlsx",
    )
