from fastapi import APIRouter, Body, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy import false
from app.salary_surat.schema.swiggy_structure2 import SuratSwiggySchema, SuratSwiggySchemaNew
from app.salary_surat.view.swiggy_structure2 import (
    add_bonus,
    calculate_salary_surat,
    create_table,
    calculate_bike_charges,
    calculate_bad_orders,
    calculate_rejection,
    calculate_amount_for_surat_rental_model
)
import pandas as pd
import tempfile, json
import io
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
from decouple import config


surat_swiggy_structure2_router = APIRouter()
processed_bucket = config("PROCESSED_FILE_BUCKET")


# @surat_swiggy_structure2_router.post("/swiggy/structure2")
# def claculate_salary(data: SuratSwiggySchema = Depends(), file: UploadFile = File(...)):

#     df = pd.read_excel(file.file)

#     df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y")

#     df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "swiggy")]

#     df["TOTAL_ORDERS"] = df["DOCUMENT_DONE_ORDERS"] + df["PARCEL_DONE_ORDERS"]

#     driver_totals = (
#         df.groupby("DRIVER_ID")
#         .agg({"PARCEL_DONE_ORDERS": "sum", "ATTENDANCE": "sum"})
#         .reset_index()
#     )

#     driver_totals["AVERAGE"] = round(
#         driver_totals["PARCEL_DONE_ORDERS"] / driver_totals["ATTENDANCE"]
#     ,0)

#     df = pd.merge(
#         df, driver_totals[["DRIVER_ID", "AVERAGE"]], on="DRIVER_ID", how="left"
#     )

#     df["ORDER_AMOUNT"] = df.apply(lambda row: calculate_salary_surat(row, data), axis=1)

#     df["BIKE_CHARGES"] = df.apply(lambda row: calculate_bike_charges(row, data), axis=1)

#     df["REJECTION_AMOUNT"] = df.apply(lambda row : calculate_rejection(row, data), axis=1)

#     df["BAD_ORDER_AMOUNT"] = df.apply(lambda row : calculate_bad_orders(row, data), axis=1)

#     table = create_table(df).reset_index()

#     print(table)

#     table["BONUS"] = table.apply(lambda row: add_bonus(row, data), axis=1)

#     table["PANALTIES"] = table["IGCC_AMOUNT"] + table["REJECTION_AMOUNT"] + table["BAD_ORDER_AMOUNT"]

#     table["FINAL_AMOUNT"] = (
#         table["ORDER_AMOUNT"]
#         + table["BONUS"]
#         - table["PANALTIES"]
#         - table["BIKE_CHARGES"]
#     )

#     table["VENDER_FEE (@6%)"] = (table["FINAL_AMOUNT"] * 0.06) + (table["FINAL_AMOUNT"])

#     table["FINAL PAYBLE AMOUNT (@18%)"] = (table["VENDER_FEE (@6%)"] * 0.18) + (
#         table["VENDER_FEE (@6%)"]
#     )

#     file_key = f"uploads/{data.file_id}/{data.file_name}"

#     response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

#     file_data = response["Body"].read()

#     swiggy_surat_table = pd.DataFrame(table)

#     df2 = pd.read_excel(io.BytesIO(file_data))

#     df3 = pd.concat([df2, swiggy_surat_table], ignore_index=True)

#     with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
#         with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
#             df3.to_excel(writer, sheet_name="Sheet1", index=False)

#             file_key = f"uploads/{data.file_id}/{data.file_name}"
#         s3_client.upload_file(temp_file.name, processed_bucket, file_key)

#     return {"file_id": data.file_id, "file_name": data.file_name}

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


# def calculate_swiggy_salary_structure2(df, structure, filename):

#     df["Total_Amount"] = df.apply(lambda row: calculate_salary_surat(row, structure), axis=1)

#     table = create_table(df).reset_index()

#     table["Total_Amount"] = add_bonus(table)


#     with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
#         with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
#             table.to_excel(writer, sheet_name="Sheet1", index=False)


#     content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     response = FileResponse(temp_file.name, media_type=content_type)
#     response.headers["Content-Disposition"] = (
#         'attachment; filename="month_year_city.xlsx"'
#     )

#     return response


@surat_swiggy_structure2_router.post("/swiggy/rentmodel/{file_id}/{file_name}")
def claculate_swiggy_rent_model(
    file_id: str,
    file_name : str,
    file: UploadFile = File(...),    
    include_slab : bool = Form(False),
    swiggy_first_order_start: int = Form(1),
    swiggy_first_order_end: int = Form(19),
    swiggy_first_week_amount: int = Form(20),
    swiggy_first_weekend_amount: int = Form(22),
    swiggy_second_order_start:int = Form(20),
    swiggy_second_order_end:int = Form(25),
    swiggy_second_week_amount: int = Form(25),
    swiggy_second_weekend_amount: int = Form(27),
    swiggy_order_greter_than: int = Form(26),
    swiggy_third_week_amount: int = Form(30),
    swiggy_third_weekend_amount: int = Form(32),
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
    bad_orders_amount : int = Form(20)):

    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y")

    df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "swiggy")]

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

    if include_slab:

        df["ORDER_AMOUNT"] = df.apply(
            lambda row: calculate_amount_for_surat_rental_model(
                row,
                swiggy_first_order_start,
                swiggy_first_order_end,
                swiggy_first_week_amount,
                swiggy_first_weekend_amount,
                swiggy_second_order_start,
                swiggy_second_order_end,
                swiggy_second_week_amount,
                swiggy_second_weekend_amount,
                swiggy_order_greter_than,
                swiggy_third_week_amount,
                swiggy_third_weekend_amount
            ), axis=1
        )

    else:
        df["ORDER_AMOUNT"] = 0

    if include_vahicle_charges:

        df["BIKE_CHARGES"] = df.apply(
            lambda row: calculate_bike_charges(
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
            lambda row: calculate_rejection(
                row,
                rejection_orders,
                rejection_amount
            ), axis=1
        )
    else: 
        df["REJECTION_AMOUNT"] = 0

    if include_bad_order:

        df["BAD_ORDER_AMOUNT"] = df.apply(
            lambda row: calculate_bad_orders(
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

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()

    swiggy_surat_table = pd.DataFrame(table)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, swiggy_surat_table], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

            file_key = f"uploads/{file_id}/{file_name}"
        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {"file_id": file_id, "file_name": file_name, "file_key" : file_key}

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


# def calculate_swiggy_salary_structure2(df, structure, filename):

#     df["Total_Amount"] = df.apply(lambda row: calculate_salary_surat(row, structure), axis=1)

#     table = create_table(df).reset_index()

#     table["Total_Amount"] = add_bonus(table)


#     with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
#         with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
#             table.to_excel(writer, sheet_name="Sheet1", index=False)


#     content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     response = FileResponse(temp_file.name, media_type=content_type)
#     response.headers["Content-Disposition"] = (
#         'attachment; filename="month_year_city.xlsx"'
#     )

#     return response
