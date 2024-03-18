from ast import List
from datetime import datetime
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import false, true
from database.database import get_db
from sqlalchemy.orm import Session
from app.Inventory.schema.schema import Invetory, InvetoryResponse, InvetoryUpdate
from app.Inventory.model.model import InventoryDB

inventory_router = APIRouter()


@inventory_router.post("/inventories")
def create_inventory(inventory: Invetory, db: Session = Depends(get_db)):

    db_query = db.query(InventoryDB).filter(
        InventoryDB.invoice_number == inventory.invoice_number
    ).first()

    if db_query is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invoice already exist"
        )

    record = InventoryDB(
        invoice_number=inventory.invoice_number,
        invoice_amount=inventory.invoice_amount,
        invoice_date=inventory.invoice_date,
        inventory_paydate=inventory.inventory_paydate,
        vender=inventory.vender,
        invoice_image_id=inventory.invoice_image_id,
    )

    db.add(record)

    db.commit()

    return {
        "status": status.HTTP_201_CREATED,
        "message": "Inventory created successfully",
    }


@inventory_router.get("/inventories/{invoice_number}")
def get_inventory(invoice_number: int, db: Session = Depends(get_db)):

    db_inventory = (
        db.query(InventoryDB)
        .filter(InventoryDB.invoice_number == invoice_number)
        .first()
    )

    if db_inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found please check inventory Number",
        )
    
    if db_inventory.is_deleted :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory is deleted",
        )
    

    return {
        "data": db_inventory,
        "status": status.HTTP_200_OK,
        "message": "Inventory Fetched Successfully",
    }


@inventory_router.get("/inventories", response_model= list[InvetoryResponse])
def get_inventories(db: Session = Depends(get_db)):

    db_inventory = db.query(InventoryDB).filter(InventoryDB.is_deleted.is_(False)).all()

    if db_inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventories Not Found"
        )
    
    inventory_responses = [
        InvetoryResponse(
            invoice_number=inventory.invoice_number,
            invoice_amount=inventory.invoice_amount,
            invoice_date=inventory.invoice_date,
            inventory_paydate=inventory.inventory_paydate,
            vendor=inventory.vender,
            invoice_image_id=inventory.invoice_image_id
        )
        for inventory in db_inventory
    ]

    return inventory_responses

    # return {
    #     "data": db_inventory,
    # #     "status": status.HTTP_200_OK,
    # #     "message": "Inventory Fetched Successfully",
    # }



@inventory_router.patch("/inventories/{invoice_number}")
def update_inventory(
    invoice_number: int, inventory: InvetoryUpdate, db: Session = Depends(get_db)
):

    db_inventory = (
        db.query(InventoryDB)
        .filter(InventoryDB.invoice_number == invoice_number)
        .first()
    )

    if db_inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found to update",
        )

    db_inventory.invoice_amount = inventory.invoice_amount
    db_inventory.invoice_date = inventory.invoice_date
    db_inventory.inventory_paydate = inventory.inventory_paydate
    db_inventory.vender = inventory.vendor
    db_inventory.invoice_image_id = inventory.invoice_image_id
    db_inventory.updated_at = datetime.now()

    db.commit()

    return {
        "message": "Inventory Updated Sucessfully",
        "status": status.HTTP_200_OK,
    }


@inventory_router.delete("/inventories/{invoice_number}")
def delete_inventory(invoice_number: str, db: Session = Depends(get_db)):

    inventory_delete = db.query(InventoryDB).filter(
        InventoryDB.invoice_number == invoice_number
    ).first()

    if inventory_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found to delete",
        )

    inventory_delete.is_deleted = True

    db.commit()

    return {
        "status": status.HTTP_202_ACCEPTED,
        "message": "Inventory deleted sucessfully",
    }
