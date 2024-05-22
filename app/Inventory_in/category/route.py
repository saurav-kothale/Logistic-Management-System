from re import S
from unicodedata import category
from fastapi import APIRouter, Depends, HTTPException,status
from app.Inventory_in.category.schema import Category, CategoryUpdate
from app.Inventory_in.category.model import CategoryDB
from sqlalchemy.orm import Session
import uuid

from database.database import get_db

category_router = APIRouter()

@category_router.get("/categories")
def get_categories(db : Session = Depends(get_db)):

    db_category = db.query(CategoryDB).all()

    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Categories Not Found"
        )

    return {
        "Status" : status.HTTP_200_OK,
        "Message" : "Record Fetched Sucessfully",
        "Category" : db_category

    }


@category_router.get("/categories/{category_id}")
def get_category(category_id : str, db : Session = Depends(get_db)):

    db_category = db.query(CategoryDB).filter(CategoryDB.category_id == category_id).first()

    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return{
        "Status" : status.HTTP_200_OK,
        "Message" : "Category fetched sucessfully",
        "Category" : db_category
    }


@category_router.post("/categories")
def create_category(schema : Category, db : Session = Depends(get_db)):

    db_category = db.query(CategoryDB).filter(CategoryDB.category_name == schema.category_name).first()

    if db_category:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Category name is already exist"
        )
    
    new_category = CategoryDB(
        category_id = str(uuid.uuid4()),
        category_name = schema.category_name,
        bike_category = schema.bike_category,
        size = schema.size,
        color = schema.color,
        city = schema.city
    )

    db.add(new_category)

    db.commit()

    return{
        "Status" : status.HTTP_201_CREATED,
        "message" : "Category Created Sucessfully",
        "category" : new_category
    }

@category_router.patch("/categories/{category_id}")
def update_category(category_id : str, schema : CategoryUpdate, db : Session = Depends(get_db)):

    db_category = db.query(CategoryDB).filter(CategoryDB.category_id == category_id).first()

    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found to update"
        )
    
    
    db_category.category_name = schema.category_name #type: ignore
    db_category.bike_category = schema.bike_category #type: ignore
    db_category.size = schema.size #type: ignore
    db_category.color = schema.color #type: ignore
    db_category.city = schema.city #type: ignore
    

    db.commit()

    return{
        "Status" : status.HTTP_201_CREATED,
        "message" : "Category Updated Sucessfully"
    }


@category_router.delete('/categories/{category_id}')
def delete_category(category_id : str, db : Session = Depends(get_db)):

    db_category = db.query(CategoryDB).filter(CategoryDB.category_id == category_id).first()

    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found to delete"
        )

    db.delete(db_category)

    db.commit()

    return {
        "status" : status.HTTP_200_OK,
        "message" : "Categoty Deleted Sucessfully",
    }