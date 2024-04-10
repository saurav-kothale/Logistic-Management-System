from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime
from app.Inventory.city_category.model import CityDb
from app.Inventory.city_category.schema import CityCategorySchema, CityUpdateSchema
from database.database import get_db
import uuid


city_router = APIRouter()


@city_router.get("/cities")
def get_cities(db : Session = Depends(get_db)):
    
    db_city = db.query(CityDb).filter(CityDb.is_deleted == False).all()

    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="content not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Records Fetched Sucessfully",
        "cities" : db_city
    }


@city_router.get("/cities/{city_id}")
def get_city(city_id : str, db : Session = Depends(get_db)):
    
    db_city = db.query(CityDb).filter(CityDb.city_id == city_id, CityDb.is_deleted == False).first()

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="record not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record Fetched Sucessfully",
        "cities" : db_city
    }


@city_router.post("/cities")
def create_city(
    schema : CityCategorySchema,
    db : Session = Depends(get_db)
):
    db_city = db.query(CityDb).filter(CityDb.city_name == schema.city_name).first()

    if db_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City name already exist"
        )
    
    new_city = CityDb(
        city_id = str(uuid.uuid4()),
        city_name = schema.city_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_city)

    db.commit()

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "City created sucessfully",
        "bike" : new_city
    }


@city_router.patch("/cities/{city_id}")
def update_city(
    city_id : str,
    schema : CityUpdateSchema,
    db : Session = Depends(get_db)
):
    db_city = db.query(CityDb).filter(CityDb.city_id == city_id).first()

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found to update"
        )
    
    db_city.city_name = schema.city_name
    db_city.updated_at = datetime.now()
    
    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Updated Successfully"
    }


@city_router.delete("/cities/{city_id}")
def delete_city(
    city_id : str,
    db : Session = Depends(get_db) 
):
    db_city = db.query(CityDb).filter(CityDb.city_id == city_id).first()

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found to delete"
        )

    db_city.is_delete = True

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record deleted sucessfully",
        "city_id" : db_city.city_id
    }