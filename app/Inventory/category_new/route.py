from fastapi import APIRouter, Depends, HTTPException,status
from numpy import size
from sqlalchemy.orm import Session
from datetime import datetime
from app.Inventory.category_new.model import NewCategoryDb
from app.Inventory.category_new.schema import CategorySchema, CategoryUpdateSchema
from database.database import get_db
import uuid


new_category_router = APIRouter()


@new_category_router.get("/categories")
def get_categories(db : Session = Depends(get_db)):
    
    db_category = db.query(NewCategoryDb).filter(NewCategoryDb.is_deleted == False).all()

    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="content not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Records Fetched Sucessfully",
        "category" : db_category
    }


@new_category_router.get("/categories/{category_id}")
def get_category(category_id : str, db : Session = Depends(get_db)):
    
    db_category = db.query(NewCategoryDb).filter(NewCategoryDb.category_id == category_id, NewCategoryDb.is_deleted == False).first()

    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="record not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record Fetched Sucessfully",
        "colors" : db_category
    }


@new_category_router.post("/categories")
def create_category(
    schema : CategorySchema,
    db : Session = Depends(get_db)
):
    db_category = db.query(NewCategoryDb).filter(NewCategoryDb.category_name == schema.category_name).first()

    if db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="category name already exist"
        )
    
    new_category = NewCategoryDb(
        category_id = str(uuid.uuid4()),
        category_name = schema.category_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_category)

    db.commit()

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "category created sucessfully",
        "category" : new_category
    }


@new_category_router.patch("/categories/{category_id}")
def update_size(
    category_id : str,
    schema : CategoryUpdateSchema,
    db : Session = Depends(get_db)
):
    db_category = db.query(NewCategoryDb).filter(NewCategoryDb.category_id == category_id).first()

    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found to update"
        )
    
    db_category.category_name = schema.category_name
    db_category.updated_at = datetime.now()
    
    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Updated Successfully"
    }


@new_category_router.delete("/categories/{category_id}")
def delete_color(
    category_id : str,
    db : Session = Depends(get_db) 
):
    db_category = db.query(NewCategoryDb).filter(NewCategoryDb.category_id == category_id).first()

    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found to delete"
        )

    db_category.is_delete = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record deleted sucessfully",
        "category_id" : db_category.category_id
    }