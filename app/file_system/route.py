from fastapi import APIRouter, status
from fastapi import UploadFile
from app.file_system.s3_events import upload_file
from fastapi.exceptions import HTTPException
import uuid
from fastapi.responses import StreamingResponse
import io
from app.file_system.s3_events import s3_client

file_router = APIRouter()

BUCKET_NAME = "evifysalary"

@file_router.get("/uploadfile/")
async def create_upload_file(file: UploadFile):

    return {"filename": file.filename}


@file_router.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    try:
        # Generate a unique file key using UUID and the original filename
        file_id = uuid.uuid4()
        file_key = f"uploads/{file_id}/{file.filename}"

        # Upload the file to S3
        s3_client.upload_fileobj(file.file, BUCKET_NAME, file_key)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"filename": file.filename, "file_id": file_id}


@file_router.get("/downloadfile/{file_id}/{filename}")
async def download_file(file_id:str, filename: str):
    file_key = f"uploads/{file_id}/{filename}"

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

