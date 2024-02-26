from fastapi import APIRouter, UploadFile
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
def get_salary(data : AhmedabadBigBascketSchema, file : UploadFile):
    df = pd.read_excel(file.file)

    df["BIKER_AMOUNT"] = df.apply(lambda row : calculate_big_basket_biker_salary(row, data), axis=1)

    df["MICRO_AMOUNT"] = df.apply(lambda row : calculate_big_basket_micro_salary(row, data), axis=1)

    df["ORDER_AMOUNT"] = df["BIKER_AMOUNT"] + df["MICRO_AMOUNT"]

    table = create_table(df)

    file_key = f"uploads/{data.file_id}/{data.file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()

    big_basket_ahmedabad = pd.DataFrame(table)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, big_basket_ahmedabad], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

            # file_key = f"uploads/{file_id}/modified.xlsx"
        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {"file_id": data.file_id, "file_name": data.file_name}


