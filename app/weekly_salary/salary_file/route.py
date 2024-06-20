from ast import Del
from email.policy import HTTP
import stat
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Path
from sqlalchemy import and_, func
from app.file_system.config import s3_client
from app import setting
import pandas as pd
import io
from app.weekly_salary.salary_file.view import calculate_payment
from app.weekly_salary.salary_file.view import insert_salary_records, delete_record, create_pivot_table
import tempfile
import uuid
from app.salary_surat.model.model import SalaryFile
from datetime import datetime
from sqlalchemy.orm import Session
from database.database import get_db
from app.weekly_salary.salary_file.model import WeeklySalaryData
from fastapi.responses import StreamingResponse
import io

weekly_salary = APIRouter()
raw_bucket = setting.ROW_BUCKET
processed_bucket = setting.PROCESSED_FILE_BUCKET


@weekly_salary.post("/calculate/weekly/salary/{file_key:path}")
def calculate_weekly_salary(
    background_tasks : BackgroundTasks,
    file_key : str,
    db : Session = Depends(get_db)
    
):
    try:

        response = s3_client.get_object(Bucket=raw_bucket, Key=file_key)

    except s3_client.exceptions.NoSuchKey:
    
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="File not found"
        )
    file_name = file_key.split("/")[2]
    file_data = response["Body"].read()

    df = pd.read_excel(io.BytesIO(file_data))

    calculated_df = calculate_payment(df)

    table = create_pivot_table(calculated_df).reset_index()


    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            table.to_excel(writer, sheet_name="Sheet1", index=False)

        temp_file_path = temp_file.name

    file_id = uuid.uuid4()
    file_key = f"weekly_files/{file_id}/calculated_{file_name}"
    final_file_name = f"calculated_{file_name}"

    new_file = SalaryFile(
        filekey=file_key,
        file_name=f"calculated_{file_name}",
        file_type=".xlsx",
        created_at=datetime.now(),
        weekly = True
    )

    db.add(new_file)

    db.commit()

    try:
        with open(temp_file_path, "rb") as temp_file:
            s3_client.upload_fileobj(temp_file, processed_bucket, file_key)

    except Exception as e:
        return {"error": e}

    try:
    
        # breakpoint()
        background_tasks.add_task(insert_salary_records, table, final_file_name,file_key, db) # type: ignore
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
    
    
@weekly_salary.get("/get/weekly/salaryfiles")
def get_weekly_salaryfiles(
    db : Session = Depends(get_db)
):
    db_files = db.query(SalaryFile).filter(SalaryFile.weekly == True).all()

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

@weekly_salary.get("/get/weekly/salaryfile/{file_key:path}")
def get_weekly_salaryfile(
    file_key: str = Path(..., description="File Key"),
    db : Session = Depends(get_db)
):
    db_file = db.query(SalaryFile).filter(SalaryFile.filekey == file_key).first()

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


@weekly_salary.delete("/weekly/salaryfile/{file_key:path}")
def delete_salary_file(
    background_tasks : BackgroundTasks,
    file_key : str = Path(..., description="File Key"),    
    db : Session = Depends(get_db),
):

    db_file = db.query(SalaryFile).filter(SalaryFile.filekey == file_key).first()

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


@weekly_salary.get("/get/salarydata/{file_key:path}")
def get_salarydata(
    file_key : str = Path(..., description="File Key"),
    db : Session = Depends(get_db)
):
    
    db_file = db.query(SalaryFile).filter(SalaryFile.filekey == file_key).first()
    
    if not db_file:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= "file not found"
        )

    db_record = db.query(WeeklySalaryData).filter(WeeklySalaryData.FILE_KEY == file_key).all()

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


@weekly_salary.post("/date-by-month")
def get_date(
    month : int,
    year : int,
    db : Session = Depends(get_db)
):
    try:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        data = db.query(WeeklySalaryData).filter(
            and_(
            func.to_timestamp(WeeklySalaryData.DATE, 'YYYY-MM-DD HH24:MI:SS') >= start_date,
            func.to_timestamp(WeeklySalaryData.DATE, 'YYYY-MM-DD HH24:MI:SS') < end_date
            )
            
        ).all()

        if not data:
            raise HTTPException(
                status_code = status.HTTP_204_NO_CONTENT,
                detail= "No data found for given month"
            )

        return data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@weekly_salary.get("/weekly/salaryfile/download/{file_key:path}")
def download_salaryfile(
    file_key: str = Path(..., description="File Key"),
    db : Session = Depends(get_db)
):
    file_name = file_key.split("/")[2]

    db_file = db.query(SalaryFile).filter(SalaryFile.filekey == file_key, SalaryFile.weekly == True).first()

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
