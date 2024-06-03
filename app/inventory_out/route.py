from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.inventory_out.schema import InventoryOut
from app.product.model.model import ProductDB
from app.inventory_out.model import ProductOutDb
from app.utils.util import get_current_user
from database.database import get_db
from datetime import datetime
import uuid

inventory_out_router = APIRouter()

@inventory_out_router.post("/inventory/use")
def create_product(
    product : InventoryOut,
    db : Session = Depends(get_db),
    current_user : str = Depends(get_current_user)

):    
    # Create a new product
    new_product = ProductOutDb(
        product_out_id=str(uuid.uuid4()),
        product_name=product.product_name,
        HSN_code = product.HSN_code,
        category=product.category,
        bike_category=product.bike_category,
        quntity=product.quantity,
        name = product.name,
        size=product.size,
        city=product.city,
        color=product.color,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False,
        user = current_user
    )

    # Add the product to the database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    used_quantity = db.query(func.sum(ProductOutDb.quntity)).filter(
        ProductOutDb.category == product.category,
        ProductOutDb.bike_category == product.bike_category,
        ProductOutDb.product_name == product.product_name,
        ProductOutDb.color == product.color,
        ProductOutDb.size == product.size,
        ProductOutDb.city == product.city
    ).scalar() or 0

    total_quantity = db.query(func.sum(ProductDB.quantity)).filter(
        ProductDB.category == product.category,
        ProductDB.bike_category == product.bike_category,
        ProductDB.product_name == product.product_name,
        ProductDB.color == product.color,
        ProductDB.size == product.size,
        ProductDB.city == product.city
    ).scalar() or 0

    remaining_quantity = total_quantity - used_quantity

    return {
        "category": product.category,
        "bike_category": product.bike_category,
        "product_name": product.product_name,
        "color" : product.color,
        "size" : product.size,
        "city" : product.city,
        "name" : product.name,
        "user" : current_user,
        "remaining_quantity": remaining_quantity
    }


@inventory_out_router.get("/get/inventory/used")
def get_used_inventory(db : Session = Depends(get_db)):

    db_products = db.query(ProductOutDb).order_by(desc(ProductOutDb.created_at)).all()

    if not db_products:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No product found"
        )
    
    return{
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "Product fetched successfully",
        "products" : db_products
    }