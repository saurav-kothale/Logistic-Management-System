from logging import exception
from fastapi import APIRouter, Body, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy import false
from app.salary_ahmedabad.schema.schema import AhmedabadZomatoSchema
from app.salary_ahmedabad.view.zomato import (
    add_bonus,
    calculate_salary_surat,
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

    df["Total_Earning"] = df.apply(
        lambda row: calculate_salary_surat(row, data), axis=1
    )

    table = create_table(df).reset_index()

    table["Total_Earning"] = add_bonus(table)

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

    # content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # response = FileResponse(temp_file.name, media_type=content_type)
    # response.headers["Content-Disposition"] = (
    #     'attachment; filename="month_year_city.xlsx"'
    # )

    # return response
