from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime
from app.Inventory.color_category.model import ColorDb
from app.Inventory.color_category.schema import ColorCategorySchema, ColorUpdateSchema
from database.database import get_db
import uuid


color_router = APIRouter()


@color_router.get("/colors")
def get_color(db : Session = Depends(get_db)):
    
    db_color = db.query(ColorDb).filter(ColorDb.is_deleted == False).all()

    if not db_color:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="content not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Records Fetched Sucessfully",
        "colors" : db_color
    }


@color_router.get("/colors/{color_id}")
def get_colors(color_id : str, db : Session = Depends(get_db)):
    
    db_color = db.query(ColorDb).filter(ColorDb.color_id == color_id, ColorDb.is_deleted == False).first()

    if db_color is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="record not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record Fetched Sucessfully",
        "colors" : db_color
    }


@color_router.post("/colors")
def create_color(
    schema : ColorCategorySchema,
    db : Session = Depends(get_db)
):
    db_color = db.query(ColorDb).filter(ColorDb.color_name == schema.color_name).first()

    if db_color:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="color name already exist"
        )
    
    new_color = ColorDb(
        color_id = str(uuid.uuid4()),
        color_name = schema.color_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_color)

    db.commit()

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "Color created sucessfully",
        "Color" : new_color
    }


@color_router.patch("/colors/{color_id}")
def update_color(
    color_id : str,
    schema : ColorUpdateSchema,
    db : Session = Depends(get_db)
):
    db_color = db.query(ColorDb).filter(ColorDb.color_id == color_id).first()

    if db_color is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found to update"
        )
    
    db_color.color_name = schema.color_name
    db_color.updated_at = datetime.now()
    
    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Updated Successfully"
    }


@color_router.delete("/colors/{color_id}")
def delete_color(
    color_id : str,
    db : Session = Depends(get_db) 
):
    db_color = db.query(ColorDb).filter(ColorDb.color_id == color_id).first()

    if db_color is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found to delete"
        )

    db_color.is_delete = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record deleted sucessfully",
        "color_id" : db_color.color_id
    }