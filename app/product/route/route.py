from itertools import product
from nis import cat
from operator import and_
from unicodedata import category
from xml.sax import default_parser_list
from fastapi import APIRouter, Depends, HTTPException, status
from app.product.schema.schema import ProductSchema
from sqlalchemy.orm import Session
from app.product.model.model import ProductDB
from app.Inventory.model.model import InventoryDB
from database.database import SessionLocal, get_db
import uuid
from sqlalchemy import func, and_


product_router = APIRouter()


@product_router.post("/product/{invoice_id}")
def create_prodcut(
    invoice_id: int,
    product : ProductSchema,
    db : Session = Depends(get_db)
):
    invoice = db.query(InventoryDB).filter(InventoryDB.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice ID not found")

    # Create a new product
    new_product = ProductDB(
        product_id=str(uuid.uuid4()),
        product_name=product.product_name,
        category=product.category,
        bike_category=product.bike_category,
        quantity=product.quantity,
        size=product.size,
        city=product.city,
        color=product.color,
        invoice_id=invoice_id
    )

    # Add the product to the database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@product_router.get("/items/{product_id}")
def get_product(product_id : str, db : Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()

    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # if db_product.invoice_id.is_deleted:


    return{

        "status" : status.HTTP_200_OK,
        "product" : db_product
    }


@product_router.get("/remaining-items/{category}")
def get_remaining_items(
    category : str,
    db: Session = Depends(get_db)
):
    
    remaining_items = []
    
    inventories = db.query(ProductDB).filter(ProductDB.category == category).all()
    
    for item in inventories:

        total_quantity = db.query(func.sum(ProductDB.quantity)).filter(ProductDB.item_id == item.id).scalar() or 0
        
  
        used_quantity = db.query(func.sum(ProductDB.quantity)).filter(ProductDB.item_id == item.id).scalar() or 0
        

        remaining_quantity = total_quantity - used_quantity
        

        remaining_items.append({
            "item_id": item.id,
            "item_name": item.name,
            "remaining_quantity": remaining_quantity
        })

    return remaining_items
    