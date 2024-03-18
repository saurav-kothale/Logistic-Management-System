from itertools import product
from nis import cat
from operator import and_
from unicodedata import category
from fastapi import APIRouter, Depends, HTTPException
from app.Inventory.product.schema.schema import ProductSchema
from sqlalchemy.orm import Session
from app.Inventory.product.model.model import ProductDB
from app.Inventory.model.model import InventoryDB
from database.database import get_db
import uuid
from sqlalchemy import func, and_


product_router = APIRouter()

@product_router.post("/product/{invoice_number}")
def create_prodcut(
    invoice_number : int,
    product : ProductSchema,
    db : Session = Depends(get_db)
):
    invoice = db.query(InventoryDB).filter(InventoryDB.invoice_number == invoice_number).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Create a new product
    new_product = ProductDB(
        product_id=str(uuid.uuid4()),
        product_name=product.product_name,
        category=product.category,
        sub_category=product.sub_category,
        quantity=product.quantity,
        size=product.size,
        city=product.city,
        invoice=invoice.invoice_number
    )

    # Add the product to the database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


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
    