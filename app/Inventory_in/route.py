from ast import List
from datetime import datetime
from DateTime import Timezones
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    status
)
from sqlalchemy import desc, false, true
from app.product.model.model import ProductDB
from app.utils.util import get_current_user
from database.database import get_db
from sqlalchemy.orm import Session
from app.Inventory_in.schema import Invetory, InvetoryResponse, InvetoryUpdate
from app.Inventory_in.model import InventoryDB
import uuid
from app.file_system.config import s3_client
from app import setting
from zoneinfo import ZoneInfo

inventory_router = APIRouter()
inventory = setting.INVENTORY

@inventory_router.post("/inventories/upload/image")
async def upload_inventory_image(file : UploadFile = None):
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="image not found"
        )
    
    file_extention = (file.filename).split(".")[1]

    if file_extention not in ["jpg", "jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail= "Please Upload valid file JPG or JPEG"
        )
    
    file_id = uuid.uuid4()
    file_key = f"{file_id}/{file.filename}"

    try:

        s3_client.upload_fileobj(file.file, inventory, file_key)


    except Exception as e:
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image : {e}"
        )
    
    
    return {
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "File uploaded successfully",
        "image_url" : f"https://{inventory}.s3.amazonaws.com/{file_key}",
        "file_name" : file.filename
    }
        

@inventory_router.post("/inventories")
def create_inventory(
    inventory: Invetory,
    db: Session = Depends(get_db),
    current_user : str = Depends(get_current_user)
):

    db_invoice = db.query(InventoryDB).filter(
        InventoryDB.invoice_number == inventory.invoice_number,
        InventoryDB.vendor == inventory.vendor
    ).first()

    if db_invoice:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="invoice already exist"
        )
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    record = InventoryDB(
        invoice_id=str(uuid.uuid4()),
        invoice_number=inventory.invoice_number,
        invoice_amount=inventory.invoice_amount,
        invoice_date=inventory.invoice_date,
        inventory_paydate=inventory.inventory_paydate,
        vendor=inventory.vendor,
        invoice_image_id=inventory.invoice_image_id,
        user=current_user,
        created_at = formatted_datetime,
        updated_at = formatted_datetime
    )

    db.add(record)

    db.commit()

    return {
        "status": status.HTTP_201_CREATED,
        "message": "Inventory created successfully",
        "invoice": {
            "invoice_id": str(record.invoice_id),  # Convert uuid to string for JSON response
            "invoice_number": record.invoice_number,
            "invoice_amount": record.invoice_amount,
            "invoice_date": record.invoice_date,
            "inventory_paydate": record.inventory_paydate,
            "vendor": record.vendor,
            "created_at" : record.created_at,
            "updated_at" : record.updated_at,
            "invoice_image_id": record.invoice_image_id,
            "user" : record.user,
        }
    }


@inventory_router.get("/inventories/{invoice_id}")
def get_inventory(invoice_id: str, db: Session = Depends(get_db)):

    db_inventory = (
        db.query(InventoryDB)
        .filter(InventoryDB.invoice_id == invoice_id)
        .first()
    )

    if db_inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found please check inventory number",
        )
    

    return {
        "data": db_inventory,
        "status": status.HTTP_200_OK,
        "message": "Inventory Fetched Successfully",
    }


@inventory_router.get("/inventories")
def get_inventories(db: Session = Depends(get_db)):

    db_inventory = db.query(InventoryDB).order_by(desc(InventoryDB.created_at)).all()

    if db_inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventories Not Found"
        )
    
    # inventory_responses = [
    #     InvetoryResponse(
    #         invoice_id=inventory.invoice_id,
    #         invoice_number=inventory.invoice_number,
    #         invoice_amount=inventory.invoice_amount,
    #         invoice_date=inventory.invoice_date,
    #         inventory_paydate=inventory.inventory_paydate,
    #         vendor=inventory.vendor,
    #         invoice_image_id=inventory.invoice_image_id

    #     )
    #     for inventory in db_inventory
    # ]

    return db_inventory

    # return {
    #     "data": db_inventory,
    # #     "status": status.HTTP_200_OK,
    # #     "message": "Inventory Fetched Successfully",
    # }



@inventory_router.patch("/inventories/{invoice_id}")
def update_inventory(
    invoice_id: str, inventory: InvetoryUpdate, db: Session = Depends(get_db)
):

    db_inventory = (
        db.query(InventoryDB)
        .filter(InventoryDB.invoice_id == invoice_id)
        .first()
    )

    if db_inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found to update",
        )
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


    db_inventory.invoice_number = inventory.invoice_number
    db_inventory.invoice_amount = inventory.invoice_amount
    db_inventory.invoice_date = inventory.invoice_date
    db_inventory.inventory_paydate = inventory.inventory_paydate
    db_inventory.vendor = inventory.vendor
    db_inventory.invoice_image_id = inventory.invoice_image_id
    db_inventory.updated_at = formatted_datetime

    db.commit()

    

    return {
        "message": "Inventory Updated Sucessfully",
        "status": status.HTTP_200_OK,
        "inventory" : {
            "invoice_number" : db_inventory.invoice_number,
            "invoice_amount" : db_inventory.invoice_amount,
            "invoice_date" : db_inventory.invoice_date,
            "inventory_paydate" : db_inventory.inventory_paydate,
            "vendor" : db_inventory.vendor,
            "image_id" : db_inventory.invoice_image_id,
            "create_at" : db_inventory.created_at,
            "updated_at" : db_inventory.updated_at
        }
    }


@inventory_router.delete("/inventories/{invoice_id}")
def delete_inventory(invoice_id: str, db: Session = Depends(get_db)):

    inventory_delete = db.query(InventoryDB).filter(
        InventoryDB.invoice_id == invoice_id
    ).first()

    if inventory_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found to delete",
        )
    
    products = db.query(ProductDB).filter(ProductDB.invoice_id == invoice_id).all()


    for product in products:
        db.delete(product)

    db.delete(inventory_delete)
    db.commit()

    return {
        "status": status.HTTP_202_ACCEPTED,
        "message": "Inventory deleted sucessfully",
    }
