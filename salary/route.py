from fastapi import APIRouter, UploadFile, Form, File, status, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from .view import is_weedend, calculate_amount_for_surat, week_or_weekend
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

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        temp_file.write(output.getvalue())

# Get the path of the temporary file
    temp_file_path = temp_file.name

    # Set the response headers to make the file downloadable
    # output.seek(0)
    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = FileResponse(temp_file_path, media_type=content_type)
    response.headers['Content-Disposition'] = 'attachment; filename="modified_data.xlsx'

    return response


    