from app.salary_ahmedabad.schema.flipkart import AhemedabadFlipkartSchema
from fastapi import APIRouter, UploadFile, File
import pandas as pd
from app.salary_ahmedabad.view.flipkart import calculate_flipkart_salary, create_table
import io
import tempfile
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
from decouple import config


ahmedabad_flipkart_router = APIRouter()
processed_bucket = config("PROCESSED_FILE_BUCKET")


@ahmedabad_flipkart_router.post("/flipkart/structure1")
def get_salary(data : AhemedabadFlipkartSchema, file: UploadFile = File(...)):
    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"])

    df = df[(df["CITY_NAME"] == "ahmedabad") & (df["CLIENT_NAME"] == "flipkart")]

    df["ORDER_AMOUNT"] = df.apply(lambda row : calculate_flipkart_salary(row, data), axis=1)

    table = create_table(df)

    file_key = f"uploads/{data.file_id}/{data.file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()

    flipkart_ahmedabad = pd.DataFrame(table)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, flipkart_ahmedabad], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

            # file_key = f"uploads/{file_id}/modified.xlsx"
        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {"file_id": data.file_id, "file_name": data.file_name}