from fastapi import APIRouter, UploadFile, Form, File, status, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from .view import is_weekend, calculate_amount_for_surat, week_or_weekend, calculate_amount_for_new_surat
import io
from fastapi.responses import FileResponse
import tempfile

salary_router = APIRouter()


@salary_router.post("/upload")
async def upload_file_and_data(
    file: UploadFile = File(...),
    first_condition_value: int = Form(None),
    second_condition_value: int = Form(None),
    first_amount: int = Form(None),
    second_amount: int = Form(None),
    third_amount : int = Form(None),
    rejection_amount : int = Form(None),
    bad_order_amount : int = Form(None)
):
    if (
        (first_condition_value is not None and second_condition_value is None)
        or (first_condition_value is None and second_condition_value is not None)
    ):
        raise HTTPException(status_code=400, detail= "Another condition can't be blank")
    
 
    df = pd.read_excel(file.file)
    df["DATE"] = pd.to_datetime(df["DATE"])

    df["Weekday_or_Weekend"] = df.apply(
        week_or_weekend, axis = 1
    )

    df["final_amount"] = df.apply(
        calculate_amount_for_surat, args=(first_condition_value, second_condition_value, first_amount, second_amount, third_amount, rejection_amount, bad_order_amount),
        axis=1
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Set the response headers to make the file downloadable
    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = FileResponse(temp_file.name, media_type=content_type)
    response.headers['Content-Disposition'] = 'attachment; filename="modified_data.xlsx"'

    return response


@salary_router.post("/updated_upload")
async def upload_new_file_and_data(
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
    week_amount : int = Form(30),
    weekend_amount : int = Form(32),
    maximum_rejection: int = Form(2),
    rejection_amount : int = Form(10),
    maximum_bad_orders : int = Form(2),
    bad_order_amount : int = Form(10)
):
    # if (
    #     (first_condition_value is not None and second_condition_value is None)
    #     or (first_condition_value is None and second_condition_value is not None)
    # ):
    #     raise HTTPException(status_code=400, detail= "Another condition can't be blank")
    
 
    df = pd.read_excel(file.file)
    df["DATE"] = pd.to_datetime(df["DATE"])


    df["final_amount"] = df.apply(
        calculate_amount_for_new_surat, 
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
            maximum_bad_orders
        ),
        axis=1
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Set the response headers to make the file downloadable
    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = FileResponse(temp_file.name, media_type=content_type)
    response.headers['Content-Disposition'] = 'attachment; filename="modified_data.xlsx"'

    return response



    