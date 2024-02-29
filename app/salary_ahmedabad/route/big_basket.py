from functools import total_ordering
from fastapi import APIRouter, Depends, UploadFile,File
from fastapi.responses import FileResponse
from app.salary_ahmedabad.schema.big_basket import AhmedabadBigBascketSchema
from app.salary_ahmedabad.view.big_basket import calculate_big_basket_biker_salary, calculate_big_basket_micro_salary,create_table
import pandas as pd
import io
import tempfile
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
from decouple import config


ahmedabadbigbascket = APIRouter()
processed_bucket = config("PROCESSED_FILE_BUCKET")


@ahmedabadbigbascket.post("/bigbasket/structure1")
def get_salary(data : AhmedabadBigBascketSchema = Depends(), file: UploadFile = File(...)):
    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"])

    df = df[(df["CITY_NAME"] == "ahmedabad") & (df["CLIENT_NAME"] == "bb 5k")]

    df["BIKER_AMOUNT"] = df.apply(lambda row : calculate_big_basket_biker_salary(row, data), axis=1)

    df["MICRO_AMOUNT"] = df.apply(lambda row : calculate_big_basket_micro_salary(row, data), axis=1)

    df["ORDER_AMOUNT"] = df["BIKER_AMOUNT"] + df["MICRO_AMOUNT"]

    df["TOTAL_ORDERS"] = df["BIKE"] + df["MICRO"]

    table = create_table(df).reset_index()

    table["FINAL_AMOUNT"] = table["ORDER_AMOUNT"]

    table["VENDER_FEE (@6%)"] = (table["FINAL_AMOUNT"] * 0.06) + (table["FINAL_AMOUNT"])

    table["FINAL PAYBLE AMOUNT (@18%)"] = (table["VENDER_FEE (@6%)"] * 0.18) + (
        table["VENDER_FEE (@6%)"]
    )

    # file_key = f"uploads/{data.file_id}/{data.file_name}"

    # response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    # file_data = response["Body"].read()

    # big_basket_ahmedabad = pd.DataFrame(table)

    # df2 = pd.read_excel(io.BytesIO(file_data))

    # df3 = pd.concat([df2, big_basket_ahmedabad], ignore_index=True)

    # with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
    #     with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
    #         table.to_excel(writer, sheet_name="Sheet1", index=False)

    #         # file_key = f"uploads/{file_id}/modified.xlsx"
    #     s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    # return {"file_id": data.file_id, "file_name": data.file_name}


    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            table.to_excel(writer, sheet_name="Sheet1", index=False)

    content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = FileResponse(temp_file.name, media_type=content_type)
    response.headers["Content-Disposition"] = (
        'attachment; filename="month_year_city.xlsx"'
    )

    return response


