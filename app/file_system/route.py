from datetime import datetime
from fileinput import filename
from click import File
from fastapi import APIRouter, Depends, background, status, Path, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi import UploadFile
from pydantic import HttpUrl
from app.file_system.s3_events import upload_file
from fastapi.exceptions import HTTPException
import uuid
from fastapi.responses import StreamingResponse
import io
# from app.file_system.s3_events import s3_client
from app.file_system.config import s3_client
from app.salary_surat.model.model import SalaryFile
from app.salary_surat.view.view import validate_surat_filename, validate_ahmedabad_filename
from app.file_system.model import FileInfo, FileRecord
from app.utils.util import get_current_user
from database.database import SessionLocal, get_db
from decouple import config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import pandas as pd
from app import setting
from io import BytesIO
from app.file_system.view import insert_records, delete_record, validate_header,validate_client, validate_city, validate_worktype


file_router = APIRouter()
# db = SessionLocal()
row_bucket = setting.ROW_BUCKET
processed_bucket = setting.PROCESSED_FILE_BUCKET

desire_order = [
        "CITY_NAME",
        "CLIENT_NAME",
        "DRIVER_ID",
        "DRIVER_NAME",
        "ATTENDANCE",
        "TOTAL_ORDERS",
        "ORDER_AMOUNT",
        "BAD_ORDER",
        "BAD_ORDER_AMOUNT",
        "REJECTION",
        "REJECTION_AMOUNT",
        "IGCC_AMOUNT",
        "CUSTOMER_TIP",
        "BONUS",
        "BIKE_CHARGES",
        "PANALTIES",
        "FINAL_AMOUNT",
        "VENDER_FEE (@6%)",
        "FINAL PAYBLE AMOUNT (@18%)",
    ]


@file_router.post("/uploadfile")
async def create_upload_files(
    file: UploadFile, 
    background_tasks: BackgroundTasks,
    db : Session = Depends(get_db),
    
):
        
    try:
        df = pd.read_excel(file.file)
        background_tasks.add_task(insert_records, df, file.filename, db) # type: ignore
        # await insert_records(df, file.filename, db)
        return{
            "status" : status.HTTP_202_ACCEPTED,
            "message" : "Record inserted successfully"
        }

    except Exception as e:
        
        print(f"An error occured : {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    

@file_router.post("/delete/records")
async def delete_records(file : str, background_tasks : BackgroundTasks, db : Session = Depends(get_db)):
    try:
        # await delete_record(db=db, file_name=file.filename)
        background_tasks.add_task(delete_record, db, file)

        return{
            "status" : status.HTTP_202_ACCEPTED,
            "message" : "Record deleted successfully"
        }

    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    

@file_router.post("/uploadfile/{city}")
async def create_upload_file(
     
    city : str,
    db : Session = Depends(get_db),
    file: UploadFile = None, 
    current_user : str = Depends(get_current_user)
    
):  
    if file is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "file not found"
        )
    
    
    db_file = db.query(FileInfo).filter(FileInfo.file_name == file.filename).first()

    if db_file is not None:
        raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail= "file is already exist"
            )


    if city == "surat": 
        if validate_surat_filename(file.filename) is False:

            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail= "please enter valid surat file name"
            )

    if city == "ahmedabad":
        if validate_ahmedabad_filename(file.filename) is False:

            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail= "please enter valid ahmedabad file name"
            )
    
    contents = await file.read()

    try:
        file_data = BytesIO(contents)
        validate_header(file_data)

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Invalid Header : {e}"
        )
    
    try : 

        validate_city(BytesIO(contents))
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail = f"{e}"
        )
    
    try : 

        validate_client(BytesIO(contents))
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail = f"{e}"
        )
    
    try : 

        validate_worktype(BytesIO(contents))
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail = f"{e}"
        )
    
    try:
        # Generate a unique file key using UUID and the original filename
        file_id = uuid.uuid4()
        file_key = f"uploads/{file_id}/{file.filename}"

        # Upload the file to S3
        s3_client.upload_fileobj(BytesIO(contents), row_bucket, file_key)

        new_file = FileInfo(
            filekey=file_key,
            file_name=file.filename,
            file_type="excel",
            weekly = False,
            created_at=datetime.now(),
        )

        db.add(new_file)

        db.commit()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return {"filename": file.filename, "file_id": file_id, "file_key" : file_key}
    

        


# else:
#     raise HTTPException(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         detail= "Insert Valid file with valid filename"
#     )


@file_router.get("/download_raw_file/{file_key:path}")
async def download_raw_file(file_key: str = Path(..., description="File Key")):

    file_name = file_key.split("/")[2]

    try:
        # Use Boto3 to download the file from S3

        response = s3_client.get_object(Bucket=row_bucket, Key=file_key)

        file_data = response["Body"].read()

        # Return the file as a StreamingResponse with Excel content type
        return StreamingResponse(
            io.BytesIO(file_data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={file_name}"},
        )

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Unexpected error: {e}")

        # Return a custom HTTPException response with 500 status and detail message
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@file_router.delete("/delete_raw_file/{file_key:path}")
async def delete_raw_file(
    file_key: str = Path(..., description="File Key"),
    db : Session = Depends(get_db)
    
):

    file_to_delete = db.query(FileInfo).filter(FileInfo.filekey == file_key).first()

    if file_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "file not found to delete"
        )
    
    try:

        response = s3_client.delete_object(Bucket=row_bucket, Key=file_key)
    
    except Exception as e:

        raise HTTPException(status_code=500, detail= "Expected error : {e}")
    
    db.delete(file_to_delete)

    db.commit()

    return {
        "status" : status.HTTP_200_OK,
        "message" : "file deleted successfully",
        "filekey" : file_key
    }


@file_router.get("/download_salary_file/{file_key:path}")
async def download_salary_file(file_key: str):
    filename = file_key.split("/")[2]

    try:
        # Use Boto3 to download the file from S3
        response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)
        file_data = response["Body"].read()

        # Return the file as a StreamingResponse with Excel content type
        return StreamingResponse(
            io.BytesIO(file_data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=calculated_{filename}"},
        )

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Unexpected error: {e}")

        # Return a custom HTTPException response with 500 status and detail message
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@file_router.get("/download_salary_file_format/{file_key:path}")
async def download_salary_file_with_format(file_key: str):
    filename = file_key.split("/")[2]

    try:
        # Use Boto3 to download the file from S3
        response = s3_client.get_object(Bucket=processed_bucket, Key=file_key)
        file_data = response["Body"].read()

        df = pd.read_excel(io.BytesIO(file_data))
        df = df[desire_order]

        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        # Return the file as a StreamingResponse with Excel content type
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=calculated_{filename}"},
        )

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Unexpected error: {e}")

        # Return a custom HTTPException response with 500 status and detail message
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@file_router.delete("/delete_processed_file/{file_key:path}")
async def delete_processed_file(
    file_key: str = Path(..., description="File Key"),
    db : Session = Depends(get_db)
    
):

    file_to_delete = db.query(SalaryFile).filter(SalaryFile.filekey == file_key).first()

    if file_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "file not found to delete"
        )
    
    try:

        response = s3_client.delete_object(Bucket=processed_bucket, Key=file_key)
    
    except Exception as e:

        raise HTTPException(status_code=500, detail= "Expected error : {e}")
    
    db.delete(file_to_delete)

    db.commit()

    return {
        "status" : status.HTTP_200_OK,
        "message" : "file deleted successfully",
        "filekey" : file_key
    }


@file_router.get("/salayfiles")
def get_salary_files(db : Session = Depends(get_db)):

    db_files = db.query(SalaryFile).filter(SalaryFile.weekly == False).all()

    if db_files is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Files Not Found"
        )

    return {
        "data": db_files,
        "status": status.HTTP_200_OK,
        "message": "Files Fetch Successfully",
    }


@file_router.get("/rawfiles")
def get_raw_files(db : Session = Depends(get_db)):

    db_files = db.query(FileInfo).filter(FileInfo.weekly == False).all()

    if db_files is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Files Not Found"
        )

    return {
        "data": db_files,
        "status": status.HTTP_200_OK,
        "message": "Files Fetch Successfully",
    }