from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from app.salary_ahmedabad.schema.bbnow import AhmedabadBbnowSchema
import pandas as pd
from app.salary_ahmedabad.view.bbnow import calculate_bbnow_salary, calculate_bbnow_salary1, create_table
import tempfile
import io
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file
from decouple import config
from app import setting

ahmedabadbbnow_router = APIRouter()
processed_bucket = setting.PROCESSED_FILE_BUCKET


@ahmedabadbbnow_router.post("/bbnow/structure1/{file_id}/{file_name}")
def get_salary(
    file_id : str,
    file_name: str,
    file : UploadFile = File(...),    
    from_order: int = Form(1),
    to_order : int = Form(15),
    first_amount : int = Form(30),
    order_greter_than: int = Form(16),
    second_amount: int = Form(35)
    ):
    
    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"])

    df =  df[(df["CITY_NAME"] == "ahmedabad") & (df["CLIENT_NAME"] == "bb now")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "bb now client not found")


    df["ORDER_AMOUNT"] = df.apply(lambda row : calculate_bbnow_salary1(
        row,
        from_order,
        to_order,
        first_amount,
        order_greter_than,
        second_amount
    ), axis=1)

    df["TOTAL_ORDERS"] = df["DONE_PARCEL _ORDERS"]

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

    # with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
    #     with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
    #         df3.to_excel(writer, sheet_name="Sheet1", index=False)

    #         # file_key = f"uploads/{file_id}/modified.xlsx"
    #     s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    # return {"file_id": data.file_id, "file_name": data.file_name}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df3.to_excel(writer, sheet_name="Sheet1", index=False)
        
        s3_client.upload_file(temp_file.name, processed_bucket, file_key)

    return {
        "message" : "BBNOW salary calculated successfully",
        "file_id": file_id, 
        "file_name": file_name, 
        "file_key" : file_key
    }

    


