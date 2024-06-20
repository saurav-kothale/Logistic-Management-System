from calendar import week
from io import BytesIO
from sqlite3 import dbapi2
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, BackgroundTasks, Path
from numpy import insert
from sqlalchemy.orm import Session
from app.weekly_salary.raw_file.model import WeeklyRawData
from database.database import get_db
from app.file_system.config import s3_client
from sqlalchemy.orm import Session
import uuid
from app.setting import ROW_BUCKET
from app.file_system.model import FileInfo
from datetime import datetime
from app.weekly_salary.raw_file.view import validate_header, insert_raw_records, delete_record
import pandas as pd
from fastapi.responses import StreamingResponse
import io

weekly_raw = APIRouter()
raw_bucket = ROW_BUCKET

@weekly_raw.post("/upload/weekly/raw_file")
async def upload_raw_file(
    file : UploadFile,
    db : Session = Depends(get_db),
    background_task : BackgroundTasks = BackgroundTasks()
):  
    
    file_extention = file.filename.split(".")[-1]

    if file_extention != "xlsx":
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="invalid file formate, file formate must be xlsx"
        )
    
    try:
        contents = await file.read()
        file_data = BytesIO(contents)
        # Validate the headers in the file
        validate_header(file_data)
    except Exception as e:
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "detail": str(e)
        }

    filekey = f"weekly_file/{uuid.uuid4()}/{file.filename}"

    try :
        s3_client.upload_fileobj(BytesIO(contents), raw_bucket, filekey)

    except Exception as e:

        print(f"Error Occure while uploading the file : {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "Internal Server Error"
        )
    
    new_file = FileInfo(
        filekey = filekey,
        file_name = file.filename,
        file_type = "excel",
        weekly = True,
        created_at = datetime.now()
    )

    try:
        db.add(new_file)
        db.commit()
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error From database while adding data"
        )
    df2 = pd.read_excel(BytesIO(contents))
    
    try:
    
        # breakpoint()
        background_task.add_task(insert_raw_records, df2,file.filename,filekey, db) # type: ignore
        # await insert_raw_records(df2, file.filename,filekey, db)
        # return{
        #     "status" : status.HTTP_202_ACCEPTED,
        #     "message" : "Record inserted successfully"
        # }

    except Exception as e:
        
        print(f"An error occured : {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    return{
        "status" : status.HTTP_200_OK,
        "file" : {
            "file_key" : new_file.filekey,
            "file_name" : new_file.file_name,
            "file_type" : new_file.file_type,
            "weekly" : new_file.weekly,
            "created_at" : new_file.created_at
        }
    }

@weekly_raw.get("/get/weekly/rawfiles")
def get_weekly_rawfiles(
    db : Session = Depends(get_db)
):
    db_files = db.query(FileInfo).filter(FileInfo.weekly == True).all()

    if not db_files:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No files"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "files fetched successfully",
        "files" : db_files
    }

@weekly_raw.get("/get/weekly/rawfile/{file_key:path}")
def get_weekly_rawfile(
    file_key: str = Path(..., description="File Key"),
    db : Session = Depends(get_db)
):
    db_file = db.query(FileInfo).filter(FileInfo.filekey == file_key).first()

    if not db_file:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="No file found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "file fetched successfully",
        "file" : {
            "file_name" : db_file.file_name,
            "file_type" : db_file.file_type,
            "file_key" : db_file.filekey,
            "created_at" : db_file.created_at
        }
    }


@weekly_raw.delete("/weekly/rawfile/{file_key:path}")
def delete_raw_file(
    background_tasks : BackgroundTasks,
    file_key : str = Path(..., description="File Key"),    
    db : Session = Depends(get_db),
):

    db_file = db.query(FileInfo).filter(FileInfo.filekey == file_key).first()

    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="file not found to delete"
        )
    
    try:
        background_tasks.add_task(delete_record, db, file_key) # type: ignore
        # await insert_records(df, file.filename, db)
        # return{
        #     "status" : status.HTTP_202_ACCEPTED,
        #     "message" : "Record inserted successfully"
        # }

    except Exception as e:
        
        print(f"An error occured : {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
    try :
        s3_client.delete_object(Bucket=raw_bucket, Key=file_key)

    except Exception as e:

        print(f"Error Occure while uploading the file : {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "Internal Server Error"
        )
    
    try:
        db.delete(db_file)
        db.commit()
    except Exception as e:
        db.rollback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
    return {
        "status" : status.HTTP_200_OK,
        "message" : "Record Deleted successfully",
        "file" : db_file.filekey
    }


@weekly_raw.get("/get/rawdata/{file_key:path}")
def get_rawdata(
    file_key : str = Path(..., description="File Key"),
    db : Session = Depends(get_db)
):
    
    db_file = db.query(FileInfo).filter(FileInfo.filekey == file_key).first()
    
    if not db_file:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= "file not found"
        )

    db_record = db.query(WeeklyRawData).filter(WeeklyRawData.FILE_KEY == file_key).all()

    if not db_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="record not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "record fetched successfully",
        "record" : db_record
    }


@weekly_raw.get("/weekly/rawfile/download/{file_key:path}")
def download_rawfile(
    file_key: str = Path(..., description="File Key"),
    db : Session = Depends(get_db)
):
    file_name = file_key.split("/")[2]
    db_file = db.query(FileInfo).filter(FileInfo.filekey == file_key, FileInfo.weekly == True).first()
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found to download"
        )
    try:

        response = s3_client.get_object(Bucket=raw_bucket, Key=file_key)

        file_data = response["Body"].read()

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


    
    
    
    
    
    
    