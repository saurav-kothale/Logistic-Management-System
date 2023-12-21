from distutils.command import upload
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
from .view import (
    is_weekend, week_or_weekend, 
    calculate_amount_for_zomato_surat, 
    calculate_amount_for_surat_swiggy, 
    calculate_amount_for_bbnow_surat,
    calculate_amount_for_ecom_surat,
    calculate_amount_for_flipcart_surat
)
import io
from fastapi.responses import FileResponse
import tempfile
from typing import List
from app.file_system.s3_events import read_s3_contents,s3_client, upload_file
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

    return {
        "file_id" : file_id,
        "file_name" : file_name
    }
    

@salary_router.post("/calculate_bb_now_surat/{file_id}/{file_name}")
async def calculate_bb_now_surat(
    file_id : str,
    file_name : str,
    file: UploadFile = File(...),
    orders_less_then: int = Form(13),
    order_amount1 : int = Form(400),
    from_order : int = Form(1),
    to_order : int = Form(14),
    order_amount2 : int = Form(30),
    order_grether_than : int = Form(15),
    order_amount3 : int = Form(35)
):
    
    df = pd.read_excel(file.file)

    table = pd.pivot_table(
        data=df[(df["CLIENT NAME"] == "BB now") & (df["CITY NAME"] == "Surat")],
        index=["DRIVER_ID", "CITY NAME", "CLIENT NAME", "REJECTION",  "BAD ORDER"],
        aggfunc={"Parcel DONE ORDERS" : "sum"}
    ).reset_index()

    attendance_count = df[df["CLIENT NAME"] == "BB now"]["DRIVER_ID"].value_counts().reset_index()
    attendance_count.columns = ["DRIVER_ID", "Attendance"]

    result = pd.merge(table,
        attendance_count,
        on="DRIVER_ID",
        how="left"
    )

    result["Average"] = round(
        result["Parcel DONE ORDERS"]/result["Attendance"]
    )

    result["Final Amount"] = result.apply(
        calculate_amount_for_bbnow_surat,
        args=(
            orders_less_then,
            order_amount1,
            from_order,
            to_order,
            order_amount2,
            order_grether_than,
            order_amount3
        ),  
        axis=1
    )

    final_result = result[["DRIVER_ID", "CITY NAME", "CLIENT NAME", 
                           "REJECTION", "BAD ORDER", "Final Amount"]]
    
    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket="evify-salary-calculated", Key=file_key)
    # except exception as e:
    #     return {"error" : e}
    
    file_data = response['Body'].read()

    df2 = pd.read_excel(io.BytesIO(file_data))
    
    df3 = pd.concat([df2, final_result], ignore_index=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine='xlsxwriter') as writer:
            df3.to_excel(writer, sheet_name='Sheet1', index=True)

            # file_key = f"uploads/{file_id}/modified.xlsx"
        s3_client.upload_file(temp_file.name, "evify-salary-calculated", file_key)


    return {
        "message" : "calculated successfully",
        "file_id" : file_id,
        "file_name" : file_name
    }


@salary_router.post("/calculate_ecom_surat/{file_id}/{file_name}")
def calculate_ecom_surat(
    file_id : str,
    file_name: str,
    file : UploadFile = File(...),
    from_order : int = Form(1),
    to_order : int = Form(40),
    first_amount : int =  Form(14),
    second_condition_from : int = Form(41),
    second_condition_to : int = Form(55),
    second_condition_amount : int = Form(15),
    third_condition : int = Form(55),
    third_condition_amount : int = Form(16)
):
    df = pd.read_excel(file.file)

    df = df[(df['CITY NAME'] == "Surat") & (df['CLIENT NAME'] == 'ECOM')]
    df["Final Amount"] = df.apply(
        calculate_amount_for_ecom_surat,
        args=(
            from_order,
            to_order,
            first_amount,
            second_condition_from,
            second_condition_to,
            second_condition_amount,
            third_condition,
            third_condition_amount
        ),

        axis = 1
    )

    table = pd.pivot_table(
        data=df,
        index=["DRIVER_ID", "CLIENT NAME", "CITY NAME"],
        aggfunc={"REJECTION": "sum","BAD ORDER" : "sum","Final Amount" : "sum"}
    )

    table_reset = table.reset_index()
    # swiggy_surat_table = pd.DataFrame(table)

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket="evify-salary-calculated", Key=file_key)
    
    file_data = response['Body'].read()
    ecom_surat_table = pd.DataFrame(table_reset)

    df2 = pd.read_excel(io.BytesIO(file_data))
    
    df3 = pd.concat([df2, ecom_surat_table], ignore_index=True)


    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine='xlsxwriter') as writer:
            df3.to_excel(writer, sheet_name='Sheet1', index=True)

        s3_client.upload_file(temp_file.name, "evify-salary-calculated", file_key)


    return {
        "file_id" : file_id,
        "file_name" : file_name
    }


@salary_router.post("/calculate_ecom_surat/{file_id}/{file_name}")
def calculate_flipcart_surat(
    file_id : str,
    file_name: str,
    file : UploadFile = File(...),
    from_order : int = Form(1),
    to_order : int = Form(40),
    first_amount : int =  Form(12),
    second_condition_from : int = Form(41),
    second_condition_to : int = Form(55),
    second_condition_amount : int = Form(13),
    third_condition : int = Form(55),
    third_condition_amount : int = Form(14)
):
    df = pd.read_csv(file.file)

    df = df[(df['CITY NAME'] == "Surat") & (df['CLIENT NAME'] == 'FLIPKART')]
    df["Final Amount"] = df.apply(
        calculate_amount_for_flipcart_surat,
        args=(
            from_order,
            to_order,
            first_amount,
            second_condition_from,
            second_condition_to,
            second_condition_amount,
            third_condition,
            third_condition_amount
        ),

        axis = 1
    )

    table = pd.pivot_table(
        data=df,
        index=["DRIVER_ID", "CLIENT NAME", "CITY NAME"],
        aggfunc={"REJECTION": "sum","BAD ORDER" : "sum","Final Amount" : "sum"}
    )

    table_reset = table.reset_index()
    # swiggy_surat_table = pd.DataFrame(table)

    file_key = f"uploads/{file_id}/{file_name}"

    response = s3_client.get_object(Bucket="evify-salary-calculated", Key=file_key)
    
    file_data = response['Body'].read()
    flipkart_surat_table = pd.DataFrame(table_reset)

    df2 = pd.read_excel(io.BytesIO(file_data))
    
    df3 = pd.concat([df2, flipkart_surat_table], ignore_index=True)


    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine='xlsxwriter') as writer:
            df3.to_excel(writer, sheet_name='Sheet1', index=True)

        s3_client.upload_file(temp_file.name, "evify-salary-calculated", file_key)


    return {
        "file_id" : file_id,
        "file_name" : file_name
    }
    
    


@salary_router.get("/getfile/{file_id}/{file_name}")
def getfile(file_id : str, file_name : str):
    file_key = f"uploads/{file_id}/{file_name}"
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_data = response['Body'].read()
    breakpoint()
    df = pd.read_excel(file_data)
    return {"message" : "successfully converted to df"}
