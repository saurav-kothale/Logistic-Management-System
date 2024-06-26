from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime
from app.Inventory_in.color_category.model import ColorDb
from app.Inventory_in.color_category.schema import ColorCategorySchema, ColorUpdateSchema
from database.database import get_db
import uuid
from sqlalchemy.sql.expression import func


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
    db_color = db.query(ColorDb).filter(func.lower(ColorDb.color_name) == func.lower(schema.color_name)).first()

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

    color_dict = {
        "color_id" : new_color.color_id,
        "color_name" : new_color.color_name,
        "created_at" : new_color.created_at,
        "updated_at" : new_color.updated_at
    }

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "Color created sucessfully",
        "color" : color_dict
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
    
    existing_city = db.query(ColorDb).filter(
        func.lower(ColorDb.color_name) == func.lower(schema.color_name),
        ColorDb.color_id != color_id
    ).first()

    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Color already exists"
        )
    
    db_color.color_name = schema.color_name
    db_color.updated_at = datetime.now()
    
    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Updated Successfully",
        "color" : {
            "color_name" : db_color.color_name,
            "updated_at" : db_color.updated_at
        }

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

    db.delete(db_color)

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record deleted sucessfully",
        "color_id" : db_color.color_id
    }