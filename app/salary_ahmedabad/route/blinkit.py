from app.salary_ahmedabad.schema.blinkit import AhmedabadBlinkitSchema
from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
import pandas as pd
from app.salary_ahmedabad.view.blinkit import calculate_blinkit_salary, create_table
import io
import tempfile
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
from decouple import config


ahmedabad_blinkit_router = APIRouter()
processed_bucket = config("PROCESSED_FILE_BUCKET")


@ahmedabad_blinkit_router.post("/blinkit/structure1/{file_id}/{file_name}")
def get_salary(
    file_id : str,
    file_name: str,
    file: UploadFile = File(...),    
    from_order : int = Form(1),
    to_order : int = Form(19),
    first_order_amount : int = Form(24),
    order_greter_than : int = Form(20),
    second_order_amount : int = Form(28)
):
    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"])

    df = df[(df["CITY_NAME"] == "ahmedabad") & (df["CLIENT_NAME"] == "blinkit")]

    df["ORDER_AMOUNT"] = df.apply(lambda row : calculate_blinkit_salary(
        row,
        from_order,
        to_order,
        first_order_amount,
        order_greter_than,
        second_order_amount
    ), axis=1)

    df["TOTAL_ORDERS"] = df["PARCEL_DONE_ORDERS"]

    table = create_table(df).reset_index()

    table["FINAL_AMOUNT"] = table["ORDER_AMOUNT"]

    table["VENDER_FEE (@6%)"] = (table["FINAL_AMOUNT"] * 0.06) + (table["FINAL_AMOUNT"])

    table["FINAL PAYBLE AMOUNT (@18%)"] = (table["VENDER_FEE (@6%)"] * 0.18) + (
        table["VENDER_FEE (@6%)"]
    )

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)

    file_data = response["Body"].read()

    blinkit_ahmedabad = pd.DataFrame(table)

    df2 = pd.read_excel(io.BytesIO(file_data))

    df3 = pd.concat([df2, blinkit_ahmedabad], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)

            # file_key = f"uploads/{file_id}/modified.xlsx"
        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {"file_id": file_id, "file_name": file_name}

    # with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
    #     with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
    #         table.to_excel(writer, sheet_name="Sheet1", index=False)

    # content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # response = FileResponse(temp_file.name, media_type=content_type)
    # response.headers["Content-Disposition"] = (
    #     'attachment; filename="month_year_city.xlsx"'
    # )

    # return response




