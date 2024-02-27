from fastapi import APIRouter, Body, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy import false
from app.salary_surat.schema.swiggy_structure2 import SuratSwiggySchema
from app.salary_surat.view.swiggy_structure2 import (
    add_bonus,
    calculate_salary_surat,
    create_table,
    calculate_bike_charges,
)
import pandas as pd
import tempfile, json
import io
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
from decouple import config


surat_swiggy_structure2_router = APIRouter()
processed_bucket = config("PROCESSED_FILE_BUCKET")


@surat_swiggy_structure2_router.post("/swiggy/structure2")
def claculate_salary(data: SuratSwiggySchema = Depends(), file: UploadFile = File(...)):

    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y")

    df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "swiggy")]

    df["TOTAL_ORDERS"] = df["DOCUMENT_DONE_ORDERS"] + df["PARCEL_DONE_ORDERS"]

    df["ORDER_AMOUNT"] = df.apply(lambda row: calculate_salary_surat(row, data), axis=1)

    df["BIKE_CHARGES"] = df.apply(lambda row: calculate_bike_charges(row, data), axis=1)


    table = create_table(df).reset_index()

    print(table)

    table["BONUS"] = table.apply(lambda row: add_bonus(row, data), axis=1)

    table["PANALTIES"] = table["IGCC_AMOUNT"]

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

    file_key = f"uploads/{data.file_id}/{data.file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()

    swiggy_surat_table = pd.DataFrame(table)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, swiggy_surat_table], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

            file_key = f"uploads/{data.file_id}/{data.file_name}"
        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {"file_id": data.file_id, "file_name": data.file_name}

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
