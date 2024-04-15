from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.inventory_out.schema import InventoryOut
from app.product.model.model import ProductDB
from app.inventory_out.model import ProductOutDb
from database.database import get_db
from datetime import datetime
import uuid

inventory_out_router = APIRouter()

@inventory_out_router.post("/inventory/use")
def create_product(
    product : InventoryOut,
    db : Session = Depends(get_db)
):

    # Create a new product
    new_product = ProductOutDb(
        product_out_id=str(uuid.uuid4()),
        product_name=product.product_name,
        category=product.category,
        bike_category=product.bike_category,
        quntity=product.quantity,
        size=product.size,
        city=product.city,
        color=product.color,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    # Add the product to the database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
