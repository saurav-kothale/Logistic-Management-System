from fastapi import APIRouter, Depends, HTTPException,status
from numpy import size
from sqlalchemy.orm import Session
from datetime import datetime
from app.Inventory.size_category.model import SizeDb
from app.Inventory.size_category.schema import SizeCategorySchema, SizeUpdateSchema
from database.database import get_db
import uuid


size_router = APIRouter()


@size_router.get("/sizes")
def get_sizes(db : Session = Depends(get_db)):
    
    db_size = db.query(SizeDb).filter(SizeDb.is_deleted == False).all()

    if db_size is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="content not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Records Fetched Sucessfully",
        "size" : db_size
    }


@size_router.get("/sizes/{size_id}")
def get_size(size_id : str, db : Session = Depends(get_db)):
    
    db_size = db.query(SizeDb).filter(SizeDb.size_id == size_id, SizeDb.is_deleted == False).first()

    if db_size is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="record not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record Fetched Sucessfully",
        "colors" : db_size
    }


@size_router.post("/sizes")
def create_size(
    schema : SizeCategorySchema,
    db : Session = Depends(get_db)
):
    db_size = db.query(SizeDb).filter(SizeDb.size_name == schema.size_name).first()

    if db_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="size name already exist"
        )
    
    new_size = SizeDb(
        size_id = str(uuid.uuid4()),
        size_name = schema.size_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_size)

    db.commit()

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "size created sucessfully",
        "size" : new_size
    }


@size_router.patch("/sizes/{size_id}")
def update_size(
    size_id : str,
    schema : SizeUpdateSchema,
    db : Session = Depends(get_db)
):
    db_size = db.query(SizeDb).filter(SizeDb.size_id == size_id).first()

    if db_size is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size not found to update"
        )
    
    db_size.size_name = schema.size_name
    db_size.updated_at = datetime.now()
    
    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Updated Successfully"
    }


@size_router.delete("/sizes/{size_id}")
def delete_size(
    size_id : str,
    db : Session = Depends(get_db) 
):
    db_size = db.query(SizeDb).filter(SizeDb.size_id == size_id).first()

    if db_size is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Size not found to delete"
        )

    db_size.is_delete = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record deleted sucessfully",
        "size_id" : db_size.size_id
    }