import json
from os import name, read
from sys import exception
from urllib import response
from fastapi import APIRouter, UploadFile, Form, File, status, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from pydantic import Json
from sqlalchemy import table

from app.file_system.route import BUCKET_NAME
from .view import is_weekend, week_or_weekend, calculate_amount_for_zomato_surat, calculate_amount_for_surat_swiggy
import io
from fastapi.responses import FileResponse
import tempfile
from typing import List
from app.file_system.s3_events import read_s3_contents,s3_client
import uuid

salary_router = APIRouter()


@salary_router.post("/calculate_zomato_surat")
async def calculate_zomato_surat(
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
     
    df = pd.read_excel(file.file)
    df["DATE"] = pd.to_datetime(df["DATE"])


    df = df[(df["CITY NAME"] == "Surat") & (df["CLIENT NAME"] == "Zomato")]  
    df["Final Amount"] = df.apply(
    calculate_amount_for_zomato_surat, 
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

    table = pd.pivot_table(
        data=df,
        index=["DRIVER_ID", "CLIENT NAME", "CITY NAME"],
        aggfunc={"REJECTION": "sum","BAD ORDER" : "sum","Final Amount" : "sum"}
    )

    zomato_surat_table = pd.DataFrame(table)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine='xlsxwriter') as writer:
            zomato_surat_table.to_excel(writer, sheet_name='Sheet1', index=True)

        file_id = uuid.uuid4()
        file_key = f"uploads/{file_id}/{file.filename}"

        try:
            s3_client.upload_fileobj(temp_file, "evify-salary-calculated", file_key)

        except exception as e:
            return {"error" : e}

    # Set the response headers to make the file downloadable
    # content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    # response = FileResponse(temp_file.name, media_type=content_type)
    # response.headers['Content-Disposition'] = 'attachment; filename="modified_data.xlsx"'

    return {
        "message" : "Successfully Calculated Salary for Zomato Surat",
        "file_id" : file_id,
        "file_name" : file.filename
    }


@salary_router.post("/calculate_swiggy_surat/{file_id}/{file_name}")
async def calculate_swiggy_surat(
    file_id : str,
    file_name : str,
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
    # file_key = f"uploads/{file_id}/{file_name}"
    # # try:
    # response = s3_client.get_object(Bucket="evify-salary-calculated", Key=file_key)
    # # except exception as e:
    # #     return {"error" : e}
    
    # file_data = response['Body'].read()
     
    # df = pd.read_excel(file.file)
    df = pd.read_excel(file.file)
    df["DATE"] = pd.to_datetime(df["DATE"])


    df = df[(df['CITY NAME'] == "Surat") & (df['CLIENT NAME'] == 'Swiggy')]
    df["Final Amount"] = df.apply(
    calculate_amount_for_surat_swiggy, 
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


    table = pd.pivot_table(
        data=df,
        index=["DRIVER_ID", "CLIENT NAME", "CITY NAME"],
        aggfunc={"REJECTION": "sum","BAD ORDER" : "sum","Final Amount" : "sum"}
    )

    table_reset = table.reset_index()
    # swiggy_surat_table = pd.DataFrame(table)

    file_key = f"uploads/{file_id}/{file_name}"
    # try:
    response = s3_client.get_object(Bucket="evify-salary-calculated", Key=file_key)
    # except exception as e:
    #     return {"error" : e}
    
    file_data = response['Body'].read()
    swiggy_surat_table = pd.DataFrame(table_reset)

    df2 = pd.read_excel(io.BytesIO(file_data))
    
    df3 = pd.concat([df2, swiggy_surat_table], ignore_index=True)


    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine='xlsxwriter') as writer:
            df3.to_excel(writer, sheet_name='Sheet1', index=True)

            # file_key = f"uploads/{file_id}/modified.xlsx"
        s3_client.upload_file(temp_file.name, "evify-salary-calculated", file_key)


    # Set the response headers to make the file downloadable
    # content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    # response = FileResponse(temp_file.name, media_type=content_type)
    # response.headers['Content-Disposition'] = 'attachment; filename="modified_data.xlsx"'

    return {"file_key" : file_key}
    

@salary_router.get("/getfile/{file_id}/{file_name}")
def getfile(file_id : str, file_name : str):
    file_key = f"uploads/{file_id}/{file_name}"
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_data = response['Body'].read()
    breakpoint()
    df = pd.read_excel(file_data)
    return {"message" : "successfully converted to df"}
