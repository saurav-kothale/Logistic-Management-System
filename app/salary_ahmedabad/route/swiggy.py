import pandas as pd
from fastapi import APIRouter, UploadFile, File, Depends
from app.salary_ahmedabad.schema.swiggy import AhmedabadSwiggySchema
from app.salary_ahmedabad.view.swiggy_structure2 import (
    calculate_salary_ahmedabad,
    create_table,
    add_bonus,
)
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
from decouple import config
import io
import tempfile


ahmedabad_swiggy_structure_router = APIRouter()
processed_bucket = config("PROCESSED_FILE_BUCKET")


@ahmedabad_swiggy_structure_router.post("/swiggy/structure1")
def claculate_salary(
    data: AhmedabadSwiggySchema = Depends(), file: UploadFile = File(...)
):

    df = pd.read_excel(file.file)

    df["Total_Amount"] = df.apply(
        lambda row: calculate_salary_ahmedabad(row, data), axis=1
    )

    table = create_table(df).reset_index()

    table["Total_Amount"] = add_bonus(table)

    file_key = f"uploads/{data.file_id}/{data.file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()

    swiggy_surat_table = pd.DataFrame(table)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, swiggy_surat_table], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

            # file_key = f"uploads/{file_id}/modified.xlsx"
        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {"file_id": data.file_id, "file_name": data.file_name}

    # with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
    #     with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
    #         table.to_excel(writer, sheet_name="Sheet1", index=False)

    # content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # response = FileResponse(temp_file.name, media_type=content_type)
    # response.headers["Content-Disposition"] = (
    #     'attachment; filename="month_year_city.xlsx"'
    # )

    # return response
