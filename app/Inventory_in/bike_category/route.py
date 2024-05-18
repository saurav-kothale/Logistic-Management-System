from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime
from app.Inventory_in.bike_category.model import BikeDb
from app.Inventory_in.bike_category.schema import BikeCategorySchema, BikeUpdateSchema
from database.database import get_db
import uuid


bike_router = APIRouter()


@bike_router.get("/bikes")
def get_bikes(db : Session = Depends(get_db)):
    
    db_bike = db.query(BikeDb).filter(BikeDb.is_deleted == False).all()

    if not db_bike:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="content not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Records Fetched Sucessfully",
        "bikes" : db_bike
    }


@bike_router.get("/bikes/{bike_id}")
def get_bike(bike_id : str, db : Session = Depends(get_db)):
    
    db_bike = db.query(BikeDb).filter(BikeDb.bike_id == bike_id, BikeDb.is_deleted == False).first()

    if db_bike is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="record not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record Fetched Sucessfully",
        "bikes" : db_bike
    }


@bike_router.post("/bikes")
def create_bike(
    schema : BikeCategorySchema,
    db : Session = Depends(get_db)
):
    db_bike = db.query(BikeDb).filter(BikeDb.bike_name == schema.bike_name).first()

    if db_bike:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bike name already exist"
        )
    
    new_bike = BikeDb(
        bike_id = str(uuid.uuid4()),
        bike_name = schema.bike_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    db.add(new_bike)

    db.commit()

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "Bike created sucessfully",
        "bike" : new_bike
    }


@bike_router.patch("/bikes/{bike_id}")
def update_bike(
    bike_id : str,
    schema : BikeUpdateSchema,
    db : Session = Depends(get_db)
):
    db_bike = db.query(BikeDb).filter(BikeDb.bike_id == bike_id)

    if db_bike is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bike not found to update"
        )
    
    db_bike.bike_name = schema.bike_name
    db_bike.updated_at = datetime.now()
    
    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "record Updated Successfully"
    }


@bike_router.delete("/bikes/{bike_id}")
def delete_bike(
    bike_id : str,
    db : Session = Depends(get_db) 
):
    db_bike = db.query(BikeDb).filter(BikeDb.bike_id == bike_id)

    if db_bike is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bike not found to delete"
        )

    db.delete(db_bike)

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record deleted sucessfully",
        "bike_id" : db_bike.bike_id
    }