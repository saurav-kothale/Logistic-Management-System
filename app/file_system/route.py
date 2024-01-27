from datetime import datetime
from fileinput import filename
from fastapi import APIRouter, status, Path
from fastapi import UploadFile
from app.file_system.s3_events import upload_file
from fastapi.exceptions import HTTPException
import uuid
from fastapi.responses import StreamingResponse
import io
from app.file_system.s3_events import s3_client
from app.salary.model import SalaryFile
from app.salary.view import validate_filename
from app.file_system.model import FileInfo
from database.database import SessionLocal


file_router = APIRouter()
db = SessionLocal()

BUCKET_NAME = "evifysalary"

@file_router.get("/uploadfile/")
async def create_upload_files(file: UploadFile):

    return {"filename": file.filename}


@file_router.post("/uploadfile")
async def create_upload_file(file: UploadFile):

    # if validate_filename(file.filename):


        try:
            # Generate a unique file key using UUID and the original filename
            file_id = uuid.uuid4()
            file_key = f"uploads/{file_id}/{file.filename}"

            # Upload the file to S3
            s3_client.upload_fileobj(file.file, BUCKET_NAME, file_key)

            new_file = FileInfo(
                file_key = file_key,
                file_name = file.filename,
                file_type = "excel",
                created_at = datetime.now()
            )

            db.add(new_file)

            db.commit()
    
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        return {"filename": file.filename, "file_id": file_id}
    
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail= "Insert Valid file with valid filename"
    #     )


@file_router.get("/download_raw_file/{file_key:path}")
async def download_raw_file(file_key: str = Path(..., description="File Key")):

    try:
        # Use Boto3 to download the file from S3
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
        file_data = response['Body'].read()

        # Return the file as a StreamingResponse with Excel content type
        return StreamingResponse(io.BytesIO(file_data), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename={file_key}.xlsx"})

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Unexpected error: {e}")
        
        # Return a custom HTTPException response with 500 status and detail message
        raise HTTPException(status_code=500, detail="Internal Server Error")


@file_router.get("/download_salary_file/{file_key:path}")
async def download_salary_file(file_key:str):

    try:
        # Use Boto3 to download the file from S3
        response = s3_client.get_object(Bucket="evify-salary-calculated", Key=file_key)
        file_data = response['Body'].read()

        # Return the file as a StreamingResponse with Excel content type
        return StreamingResponse(io.BytesIO(file_data), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename={file_key}.xlsx"})

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Unexpected error: {e}")
        
        # Return a custom HTTPException response with 500 status and detail message
        raise HTTPException(status_code=500, detail="Internal Server Error")


@file_router.get("/salayfiles")
def get_salary_files():
    db_files = db.query(SalaryFile).all()

    if db_files is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Files Not Found"
        )
    
    return{
        "data" : db_files,
        "status" : status.HTTP_200_OK,
        "message" : "Files Fetch Successfully"
    }

@file_router.get("/rawfiles")
def get_raw_files():
    db_files = db.query(FileInfo).all()

    if db_files is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Files Not Found"
        )
    
    return{
        "data" : db_files,
        "status" : status.HTTP_200_OK,
        "message" : "Files Fetch Successfully"
    }