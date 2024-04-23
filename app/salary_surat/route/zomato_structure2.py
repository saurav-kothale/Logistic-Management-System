from logging import exception
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.salary_surat.schema.zomato_structure2 import (
    TimeStructureSchema
)
from app.salary_surat.view.zomato_structure2 import (
    add_bonus,
    calculate_salary_surat,
    create_table,
    calculate_rejection,
    calculate_bad_orders,
    calculate_amount_for_surat_rental_model,
    calculate_bike_charges_for_rental_model,
    calculate_amount_for_surat_time_model,
    validate_date
)
import pandas as pd
import tempfile
import uuid
from app.salary_surat.model.model import SalaryFile
from datetime import datetime
from database.database import SessionLocal
from app.file_system.s3_events import s3_client
from app import setting
import io

surat_zomato_structure2_router = APIRouter()
db = SessionLocal()
row_bucket = setting.ROW_BUCKET
processed_bucket = setting.PROCESSED_FILE_BUCKET


# @surat_zomato_structure2_router.post("/zomato/structure2")
# def claculate_salary(
#     data: SuratZomatoStructure2 = Depends(), file: UploadFile = File(...)
# ):

#     df = pd.read_excel(file.file)

#     df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y")

#     df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "zomato")]

#     df["TOTAL_ORDERS"] = df["DONE_DOCUMENT_ORDERS"] + df["DONE_PARCEL_ORDERS"]

#     driver_totals = (
#         df.groupby("DRIVER_ID")
#         .agg({"DONE_PARCEL_ORDERS": "sum", "ATTENDANCE": "sum"})
#         .reset_index()
#     )

#     driver_totals["AVERAGE"] = round(
#         driver_totals["DONE_PARCEL_ORDERS"] / driver_totals["ATTENDANCE"], 0
#     )

#     df = pd.merge(
#         df, driver_totals[["DRIVER_ID", "AVERAGE"]], on="DRIVER_ID", how="left"
#     )

#     df["ORDER_AMOUNT"] = df.apply(lambda row: calculate_salary_surat(
        
#     ), axis=1)

#     df["BIKE_CHARGES"] = df.apply(lambda row: calculate_bike_charges(row, data), axis=1)

#     df["REJECTION_AMOUNT"] = df.apply(
#         lambda row: calculate_rejection(row, data), axis=1
#     )

#     df["BAD_ORDER_AMOUNT"] = df.apply(
#         lambda row: calculate_bad_orders(row, data), axis=1
#     )

#     table = create_table(df).reset_index()

#     table["BONUS"] = table.apply(lambda row: add_bonus(row, data), axis=1)

#     table["PANALTIES"] = (
#         table["IGCC_AMOUNT"] + table["REJECTION_AMOUNT"] + table["BAD_ORDER_AMOUNT"]
#     )

#     table["FINAL_AMOUNT"] = (
#         table["ORDER_AMOUNT"]
#         + table["BONUS"]
#         - table["PANALTIES"]
#         - table["BIKE_CHARGES"]
#     )

#     table["VENDER_FEE (@6%)"] = (table["FINAL_AMOUNT"] * 0.06) + (table["FINAL_AMOUNT"])

#     table["FINAL PAYBLE AMOUNT (@18%)"] = (table["VENDER_FEE (@6%)"] * 0.18) + (
#         table["VENDER_FEE (@6%)"]
#     )

#     with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
#         with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
#             table.to_excel(writer, sheet_name="Sheet1", index=False)

#         file_id = uuid.uuid4()
#         file_key = f"uploads/{file_id}/{file.filename}"

#         new_file = SalaryFile(
#             filekey=file_key,
#             file_name=file.filename,
#             file_type=".xlsx",
#             created_at=datetime.now(),
#         )

#         db.add(new_file)

#         db.commit()

#         try:
#             s3_client.upload_fileobj(temp_file, processed_bucket, file_key)

#         except exception as e:
#             return {"error": e}

#     return {
#         "message": "Successfully Calculated Salary for Zomato Surat",
#         "file_id": file_id,
#         "file_name": file.filename,
#     }


#     return FileResponse(
#     temp_file.name,
#     media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#     headers={"Content-Disposition": f"attachment; filename=calculated_{file.filename}"},
#     filename=f"calculated_{file.filename}.xlsx",
# )


# return response


# def calculate_zomato_salary_structure2(df, structure, filename):
#     df["DATE"] = pd.to_datetime(df["DATE"])

#     df = df[(df["CITY_NAME"] == "Surat") & (df["CLIENT_NAME"] == "Zomato")]

#     df["Total_Earning"] = df.apply(lambda row: calculate_salary_surat(row, structure), axis=1)

#     df["Total_Orders"] = df["DOCUMENT_DONE_ORDER"] + df["DONE_PARCEL_ORDERS"]

#     table = create_table(df).reset_index()

#     table["Total_Earning"] = add_bonus(table)

#     with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
#         with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
#             table.to_excel(writer, sheet_name="Sheet1", index=False)

#         file_id = uuid.uuid4()
#         file_key = f"uploads/{file_id}/{filename}"

#         new_file = SalaryFile(
#             filekey=file_key,
#             file_name=filename,
#             file_type=".xlsx",
#             created_at=datetime.now(),
#         )

#         db.add(new_file)

#         db.commit()

#         try:
#             s3_client.upload_fileobj(temp_file, processed_bucket, file_key)

#         except exception as e:
#             return {"error": e}

#     return {
#             "message": "Successfully Calculated Salary for Zomato Surat",
#             "file_id": file_id,
#             "file_name": filename,
#         }


# return response


@surat_zomato_structure2_router.post("/zomato/new/structure2")
def claculate_salary_new(
    file: UploadFile = File(...),
    include_slab: bool = Form(False),
    zomato_first_order_start : int = Form(1),
    zomato_first_order_end : int = Form(29),
    zomato_first_order_amount : int = Form(30),
    zomato_order_greter_than : int = Form(26),
    zomato_second_order_amount : int = Form(30),
    include_vahicle_charges : bool = Form(False),
    fulltime_average : int = Form(20),
    fulltime_greter_than_order : int = Form(20),
    vahicle_charges_fulltime : int = Form(100),
    partime_average : int = Form(11),
    partime_greter_than_order : int = Form(12),
    vahicle_charges_partime : int = Form(70),
    include_bonus : bool = Form(False),
    bonus_order_fulltime : int = Form(700),
    bonus_amount_fulltime : int = Form(100),
    bonus_order_partime : int = Form(400),
    bonus_amount_partime : int = Form(500),
    include_rejection: bool = Form(False),
    rejection_orders : int = Form(2),
    rejection_amount : int = Form(20),
    include_bad_order : bool = Form(False),
    bad_orders : int = Form(2),
    bad_orders_amount : int = Form(20)
):

    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y")

    df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "zomato")]

    df["TOTAL_ORDERS"] = df["DONE_DOCUMENT_ORDERS"] + df["DONE_PARCEL_ORDERS"]

    driver_totals = (
        df.groupby("DRIVER_ID")
        .agg({"DONE_PARCEL_ORDERS": "sum", "ATTENDANCE": "sum"})
        .reset_index()
    )

    driver_totals["AVERAGE"] = round(
        driver_totals["DONE_PARCEL_ORDERS"] / driver_totals["ATTENDANCE"], 0
    )

    df = pd.merge(
        df, driver_totals[["DRIVER_ID", "AVERAGE"]], on="DRIVER_ID", how="left"
    )

    if include_slab:

        df["ORDER_AMOUNT"] = df.apply(
            lambda row: calculate_salary_surat(
            row,
            zomato_first_order_start,
            zomato_first_order_end,
            zomato_first_order_amount,
            zomato_order_greter_than,
            zomato_second_order_amount
            ), axis=1
        )

    else:
        df["ORDER_AMOUNT"] = 0

    if include_vahicle_charges:

        df["BIKE_CHARGES"] = df.apply(
            lambda row: calculate_bike_charges_for_rental_model(
            row,
            fulltime_average,
            fulltime_greter_than_order,
            vahicle_charges_fulltime,
            partime_average,
            partime_greter_than_order,
            vahicle_charges_partime
            ), axis=1
        )
    else:
        df["BIKE_CHARGES"] = 0

    if include_rejection:

        df["REJECTION_AMOUNT"] = df.apply(
            lambda row: calculate_rejection(
            row,
            rejection_orders,
            rejection_amount 
            ), axis=1
        )
    else: 
        df["REJECTION_AMOUNT"] = 0

    if include_bad_order:

        df["BAD_ORDER_AMOUNT"] = df.apply(
            lambda row: calculate_bad_orders(
            row,
            bad_orders,
            bad_orders_amount  
            ), axis=1
        )
    
    else:
        df["BAD_ORDER_AMOUNT"] = 0

    table = create_table(df).reset_index()

    if include_bonus:
        table["BONUS"] = table.apply(lambda row: add_bonus(
            row,
            bonus_order_fulltime,
            bonus_amount_fulltime,
            bonus_order_partime,
            bonus_amount_partime
        ), axis=1)

    else: 
        table["BONUS"] = 0

    table["PANALTIES"] = table["IGCC_AMOUNT"] + table["REJECTION_AMOUNT"] + table["BAD_ORDER_AMOUNT"]

    table["FINAL_AMOUNT"] = (
        table["ORDER_AMOUNT"]
        + table["BONUS"]
        - table["PANALTIES"]
        - table["BIKE_CHARGES"]
    )

    table["VENDER_FEE (@6%)"] = (table["FINAL_AMOUNT"] * 0.06) + (table["FINAL_AMOUNT"])

    table["FINAL PAYBLE AMOUNT (@18%)"] = (table["VENDER_FEE (@6%)"] * 0.18) + (
        table["VENDER_FEE (@6%)"]
    )

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
         "file_key" : file_key
    }


@surat_zomato_structure2_router.post("/zomato/structure3")
def claculate_salary_structure3(
    file: UploadFile = File(...),
    include_slab: bool = Form(False),
    zomato_first_order_start : int = Form(1),
    zomato_first_order_end : int = Form(29),
    zomato_first_week_amount : int = Form(30),
    zomato_first_weekend_amount : int = Form(32),
    zomato_second_order_start : int = Form(20),
    zomato_second_order_end : int = Form(25),
    zomato_second_week_amount : int = Form(25),
    zomato_second_weekend_amount : int = Form(27),
    zomato_order_greter_than : int = Form(26),
    zomato_third_week_amount : int = Form(30),
    zomato_third_weekend_amount : int = Form(32),
    include_vahicle_charges : bool = Form(False),
    fulltime_average : int = Form(20),
    fulltime_greter_than_order : int = Form(20),
    vahicle_charges_fulltime : int = Form(100),
    partime_average : int = Form(11),
    partime_greter_than_order : int = Form(12),
    vahicle_charges_partime : int = Form(70),
    include_bonus : bool = Form(False),
    bonus_order_fulltime : int = Form(700),
    bonus_amount_fulltime : int = Form(100),
    bonus_order_partime : int = Form(400),
    bonus_amount_partime : int = Form(500),
    include_rejection: bool = Form(False),
    rejection_orders : int = Form(2),
    rejection_amount : int = Form(20),
    include_bad_order : bool = Form(False),
    bad_orders : int = Form(2),
    bad_orders_amount : int = Form(20)    

):

    df = pd.read_excel(file.file)

    df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y")

    df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "zomato")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "Zomato client not found")

    df["TOTAL_ORDERS"] = df["DONE_PARCEL_ORDERS"]

    driver_totals = (
        df.groupby("DRIVER_ID")
        .agg({"DONE_PARCEL_ORDERS": "sum", "ATTENDANCE": "sum"})
        .reset_index()
    )

    driver_totals["AVERAGE"] = round(
        driver_totals["DONE_PARCEL_ORDERS"] / driver_totals["ATTENDANCE"], 0
    )

    df = pd.merge(
        df, driver_totals[["DRIVER_ID", "AVERAGE"]], on="DRIVER_ID", how="left"
    )

    if include_slab:

        df["ORDER_AMOUNT"] = df.apply(
            lambda row: calculate_amount_for_surat_rental_model(
                row,
                zomato_first_order_start,
                zomato_first_order_end,
                zomato_first_week_amount,
                zomato_first_weekend_amount,
                zomato_second_order_start,
                zomato_second_order_end,
                zomato_second_week_amount,
                zomato_second_weekend_amount,
                zomato_order_greter_than,
                zomato_third_week_amount,
                zomato_third_weekend_amount
            ), axis=1
        )

    else:
        df["ORDER_AMOUNT"] = 0

    if include_vahicle_charges:

        df["BIKE_CHARGES"] = df.apply(
            lambda row: calculate_bike_charges_for_rental_model(
                row,
                fulltime_average,
                fulltime_greter_than_order,
                vahicle_charges_fulltime,
                partime_average,
                partime_greter_than_order,
                vahicle_charges_partime
            ), axis=1
        )
    else:
        df["BIKE_CHARGES"] = 0

    if include_rejection:

        df["REJECTION_AMOUNT"] = df.apply(
            lambda row: calculate_rejection(
                row,
                rejection_orders,
                rejection_amount

            ), axis=1
        )
    else: 
        df["REJECTION_AMOUNT"] = 0

    if include_bad_order:

        df["BAD_ORDER_AMOUNT"] = df.apply(
            lambda row: calculate_bad_orders(
                row,
                bad_orders,
                bad_orders_amount
            ), axis=1
        )
    
    else:
        df["BAD_ORDER_AMOUNT"] = 0

    table = create_table(df).reset_index()

    if include_bonus:
        table["BONUS"] = table.apply(lambda row: add_bonus(
            row,
            bonus_order_fulltime,
            bonus_amount_fulltime,
            bonus_order_partime,
            bonus_amount_partime

        ), axis=1)

    else: 
        table["BONUS"] = 0

    table["PANALTIES"] = table["IGCC_AMOUNT"] + table["REJECTION_AMOUNT"] + table["BAD_ORDER_AMOUNT"]

    table["FINAL_AMOUNT"] = (
        (table["ORDER_AMOUNT"] + table["BONUS"]) - (table["PANALTIES"] + table["BIKE_CHARGES"])
    )

    table["VENDER_FEE (@6%)"] = (table["FINAL_AMOUNT"] * 0.06) + (table["FINAL_AMOUNT"])

    table["FINAL PAYBLE AMOUNT (@18%)"] = (table["VENDER_FEE (@6%)"] * 0.18) + (
        table["VENDER_FEE (@6%)"]
    )

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
        "file_key" : file_key
    }


@surat_zomato_structure2_router.post("/zomato/date/structure")
def claculate_salary_time_structure(
    schema : TimeStructureSchema
):
    try:

        response = s3_client.get_object(Bucket=row_bucket, Key=schema.file_key)

    except s3_client.exceptions.NoSuchKey:
    
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Raw file not found"
        )
    
    raw_data = response["Body"].read()
    
    df = pd.read_excel(io.BytesIO(raw_data))

    df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y").dt.date

    df = df[(df["CITY_NAME"] == "surat") & (df["CLIENT_NAME"] == "zomato")]

    if df.empty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail= "Zomato client not found")

    df["TOTAL_ORDERS"] = df["DONE_PARCEL_ORDERS"]

    driver_totals = (
        df.groupby("DRIVER_ID")
        .agg({"DONE_PARCEL_ORDERS": "sum", "ATTENDANCE": "sum"})
        .reset_index()
    )

    driver_totals["AVERAGE"] = round(
        driver_totals["DONE_PARCEL_ORDERS"] / driver_totals["ATTENDANCE"], 0
    )

    df = pd.merge(
        df, driver_totals[["DRIVER_ID", "AVERAGE"]], on="DRIVER_ID", how="left"
    )

    df["ORDER_AMOUNT"] = 0

    if schema.include_slab:
        if len(schema.slabs) >= 2:
            for slab in schema.slabs:
                df["ORDER_AMOUNT"] = df.apply(
                lambda row : calculate_amount_for_surat_time_model(
                    row,
                    slab.zomato_first_order_start,
                    slab.zomato_first_order_end,
                    slab.zomato_first_week_amount,
                    slab.zomato_first_weekend_amount,
                    slab.zomato_second_order_start,
                    slab.zomato_second_order_end,
                    slab.zomato_second_week_amount,
                    slab.zomato_second_weekend_amount,
                    slab.zomato_order_greter_than,
                    slab.zomato_third_week_amount,
                    slab.zomato_third_weekend_amount
                )if validate_date(slab.from_date) <= row['DATE'] <= validate_date(slab.to_date) else row["ORDER_AMOUNT"],
            axis=1
            )
        else:
            df["ORDER_AMOUNT"] = df.apply(
                lambda row : calculate_amount_for_surat_time_model(
                    row,
                    schema.slabs[0].zomato_first_order_start,
                    schema.slabs[0].zomato_first_order_end,
                    schema.slabs[0].zomato_first_week_amount,
                    schema.slabs[0].zomato_first_weekend_amount,
                    schema.slabs[0].zomato_second_order_start,
                    schema.slabs[0].zomato_second_order_end,
                    schema.slabs[0].zomato_second_week_amount,
                    schema.slabs[0].zomato_second_weekend_amount,
                    schema.slabs[0].zomato_order_greter_than,
                    schema.slabs[0].zomato_third_week_amount,
                    schema.slabs[0].zomato_third_weekend_amount
                ), axis=1
            )

    else:
        df["ORDER_AMOUNT"] = 0

    if schema.include_vahicle_charges:

        df["BIKE_CHARGES"] = df.apply(
            lambda row: calculate_bike_charges_for_rental_model(
                row,
                schema.fulltime_average,
                schema.fulltime_greter_than_order,
                schema.vahicle_charges_fulltime,
                schema.partime_average,
                schema.partime_greter_than_order,
                schema.vahicle_charges_partime
            ), axis=1
        )
    else:
        df["BIKE_CHARGES"] = 0

    if schema.include_rejection:

        df["REJECTION_AMOUNT"] = df.apply(
            lambda row: calculate_rejection(
                row,
                schema.rejection_orders,
                schema.rejection_amount

            ), axis=1
        )
    else: 
        df["REJECTION_AMOUNT"] = 0

    if schema.include_bad_order:

        df["BAD_ORDER_AMOUNT"] = df.apply(
            lambda row: calculate_bad_orders(
                row,
                schema.bad_orders,
                schema.bad_orders_amount
            ), axis=1
        )
    
    else:
        df["BAD_ORDER_AMOUNT"] = 0

    table = create_table(df).reset_index()

    if schema.include_bonus:
        table["BONUS"] = table.apply(lambda row: add_bonus(
            row,
            schema.bonus_order_fulltime,
            schema.bonus_amount_fulltime,
            schema.bonus_order_partime,
            schema.bonus_amount_partime

        ), axis=1)

    else: 
        table["BONUS"] = 0

    table["PANALTIES"] = table["IGCC_AMOUNT"] + table["REJECTION_AMOUNT"] + table["BAD_ORDER_AMOUNT"]

    table["FINAL_AMOUNT"] = (
        (table["ORDER_AMOUNT"] + table["BONUS"]) - (table["PANALTIES"] + table["BIKE_CHARGES"])
    )

    table["VENDER_FEE (@6%)"] = (table["FINAL_AMOUNT"] * 0.06) + (table["FINAL_AMOUNT"])

    table["FINAL PAYBLE AMOUNT (@18%)"] = (table["VENDER_FEE (@6%)"] * 0.18) + (
        table["VENDER_FEE (@6%)"]
    )

    file_name = schema.file_key.split("/")[2]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            table.to_excel(writer, sheet_name="Sheet1", index=False)

        file_id = uuid.uuid4()
        calculated_file_key = f"uploads/{file_id}/{file_name}"

        new_file = SalaryFile(
            filekey=calculated_file_key,
            file_name=file_name,
            file_type=".xlsx",
            created_at=datetime.now(),
        )

        db.add(new_file)

        db.commit()

        try:
            s3_client.upload_fileobj(temp_file, processed_bucket, calculated_file_key)

        except exception as e:
            return {"error": e}

    return {
        "message": "Successfully Calculated Salary for Zomato Surat",
        "file_id": file_id,
        "file_name": file_name,
        "file_key" : calculated_file_key
    }