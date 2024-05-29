from datetime import datetime
from itertools import product
from nis import cat
from operator import and_
from typing import Optional
from unicodedata import category
from xml.sax import default_parser_list
from fastapi import APIRouter, Depends, HTTPException, status
from app.product.schema.schema import ProductSchema
from sqlalchemy.orm import Session
from app.product.model.model import ProductDB
from app.inventory_out.model import ProductOutDb
from app.Inventory_in.model import InventoryDB
from app.utils.util import get_current_user
from database.database import SessionLocal, get_db
import uuid
from sqlalchemy import Subquery, distinct, func, and_
from app.product.view.view import add_gst
from sqlalchemy import desc


product_router = APIRouter()


@product_router.post("/product/{invoice_id}")
def create_product(
    invoice_id: str,
    product : ProductSchema,
    current_user : str = Depends(get_current_user),
    db : Session = Depends(get_db),

):
    invoice = db.query(InventoryDB).filter(InventoryDB.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice ID not found")

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # Create a new product

    quntity_amount = product.quantity * product.amount

    gst_amount = add_gst(product.GST.value, quntity_amount)


    new_product = ProductDB(
        product_id=str(uuid.uuid4()),
        product_name=product.product_name,
        category=product.category,
        bike_category=product.bike_category,
        quantity=product.quantity,
        size=product.size,
        city=product.city,
        color=product.color,
        user = current_user,
        invoice_id=invoice_id,
        HSN_code = product.HSN_code,
        GST = product.GST,
        unit = product.unit,
        amount = product.amount,
        amount_with_gst = gst_amount,
        created_at = formatted_datetime,
        updated_at = formatted_datetime,
        is_deleted = False
    )

    # Add the product to the database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@product_router.get("/products/{product_id}")
def get_product(product_id : str, db : Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()

    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if db_product.invoice.is_deleted:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Inventory is Deleted of this product"
        )

    return{
        "status" : status.HTTP_200_OK,
        "product" : db_product
    }


@product_router.get("/products")
def get_products(db : Session = Depends(get_db)):

    db_products = db.query(ProductDB).filter(ProductDB.is_deleted == False).all()

    if not db_products:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )

    return {
        "status" : status.HTTP_200_OK,
        "message" : "Products Fetched Successfully",
        "products" : db_products
    }


@product_router.patch("/products/{product_id}")
def update_product(
    product_id : str, 
    data : ProductSchema, 
    db : Session = Depends(get_db)
):
    db_product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()

    if db_product is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Product is not found to update"
        )
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    db_product.product_name = data.product_name
    db_product.category = data.category
    db_product.bike_category = data.bike_category
    db_product.quantity = data.quantity
    db_product.size = data.size
    db_product.city = data.city
    db_product.color = data.color
    db_product.updated_at = formatted_datetime

    db.commit()

    return {
        "message": "Product Updated Sucessfully",
        "status": status.HTTP_200_OK,
        "product" : {
            "product_name" : db_product.product_name,
            "product_category" : db_product.category,
            "product_bike_category" : db_product.bike_category,
            "product_quantity" : db_product.quantity,
            "prodcut_size" : db_product.size,
            "product_city" : db_product.city,
            "product_color" : db_product.color,
            "product_updated_at" : db_product.updated_at
        }
    }


@product_router.delete("/products/{product_id}")
def delete_product(
    product_id : str,
    db : Session = Depends(get_db)
):
    db_product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()

    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product Not Found to Delete"
        )
    
    db.delete(db_product)

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Product deleted sucessfully"
    }

@product_router.get("/products/invoice/{invoice_id}")
def get_inventory_products(
    invoice_id : str,
    db : Session = Depends(get_db) 
):
    
    db_products = db.query(ProductDB).filter(ProductDB.invoice_id == invoice_id, ProductDB.is_deleted == False).all()

    if not db_products:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Products Not Found for given invoice id"
        )
    
    return {
        "status" : status.HTTP_200_OK,
        "message" : "Product Fetched successfully",
        "product" : db_products
    }


@product_router.get("/product/category/deprecated")
def retrieve_products_by_category123_deprecated(db: Session = Depends(get_db)):
    # Subquery to calculate the total used quantity
    used_quantity_subquery = db.query(
        ProductOutDb.HSN_code,
        ProductOutDb.product_name,
        ProductOutDb.category,
        ProductOutDb.bike_category,
        ProductOutDb.color,
        ProductOutDb.size,
        ProductOutDb.city,
        func.sum(ProductOutDb.quntity).label("total_used_quantity")
    ).group_by(
        ProductOutDb.HSN_code, 
        ProductOutDb.product_name,
        ProductOutDb.category,
        ProductOutDb.bike_category,
        ProductOutDb.color,
        ProductOutDb.size,
        ProductOutDb.city
    ).subquery()

    # Subquery to calculate the total quantity for each product
    total_quantity_subquery = db.query(
        ProductDB.HSN_code,
        ProductDB.category,
        ProductDB.bike_category,
        ProductDB.color,
        ProductDB.size,
        ProductDB.city,
        ProductDB.product_name,
        func.sum(ProductDB.quantity).label("total_quantity")
    ).group_by(
        ProductDB.HSN_code,
        ProductDB.category,
        ProductDB.bike_category,
        ProductDB.color,
        ProductDB.size,
        ProductDB.city,
        ProductDB.product_name
    ).subquery()

    # Main query to retrieve distinct products and calculate remaining quantity
    db_distinct = db.query(
        total_quantity_subquery.c.HSN_code,
        total_quantity_subquery.c.category,
        total_quantity_subquery.c.bike_category,
        total_quantity_subquery.c.color,
        total_quantity_subquery.c.size,
        total_quantity_subquery.c.city,
        total_quantity_subquery.c.product_name,
        func.coalesce(total_quantity_subquery.c.total_quantity - used_quantity_subquery.c.total_used_quantity, total_quantity_subquery.c.total_quantity).label('remaining_quantity')
    ).outerjoin(
        used_quantity_subquery,
        and_(
            total_quantity_subquery.c.HSN_code == used_quantity_subquery.c.HSN_code,
            total_quantity_subquery.c.product_name == used_quantity_subquery.c.product_name,
            total_quantity_subquery.c.category == used_quantity_subquery.c.category,
            total_quantity_subquery.c.bike_category == used_quantity_subquery.c.bike_category,
            total_quantity_subquery.c.color == used_quantity_subquery.c.color,
            total_quantity_subquery.c.size == used_quantity_subquery.c.size,
            total_quantity_subquery.c.city == used_quantity_subquery.c.city
        )
    ).all()

    # Format the result
    result = [
        {
            "hsn_code" : row.HSN_code,
            "category": row.category,
            "bike_category": row.bike_category,
            "color": row.color,
            "size": row.size,
            "city": row.city,
            "product_name": row.product_name,
            "remaining_quantity": row.remaining_quantity
        } 
        for row in db_distinct
    ]
    
    return {
        "distinct_values": result
    }


@product_router.get("/product/category")
def retrieve_products_by_category123(db: Session = Depends(get_db)):
    # Subquery to calculate the total used quantity
    used_quantity_subquery = db.query(
        ProductOutDb.HSN_code,
        ProductOutDb.product_name,
        ProductOutDb.category,
        ProductOutDb.bike_category,
        ProductOutDb.color,
        ProductOutDb.size,
        ProductOutDb.city,
        func.sum(ProductOutDb.quntity).label("total_used_quantity")
    ).group_by(
        ProductOutDb.HSN_code, 
        ProductOutDb.product_name,
        ProductOutDb.category,
        ProductOutDb.bike_category,
        ProductOutDb.color,
        ProductOutDb.size,
        ProductOutDb.city
    ).subquery()

    # Subquery to calculate the total quantity for each product
    total_quantity_subquery = db.query(
        ProductDB.HSN_code,
        ProductDB.category,
        ProductDB.bike_category,
        ProductDB.color,
        ProductDB.size,
        ProductDB.city,
        ProductDB.product_name,
        ProductDB.created_at,  # Include created_at in the subquery
        func.sum(ProductDB.quantity).label("total_quantity")
    ).group_by(
        ProductDB.HSN_code,
        ProductDB.category,
        ProductDB.bike_category,
        ProductDB.color,
        ProductDB.size,
        ProductDB.city,
        ProductDB.product_name,
        ProductDB.created_at  # Group by created_at as well
    ).subquery()

    # Main query to retrieve distinct products and calculate remaining quantity
    db_distinct = db.query(
        total_quantity_subquery.c.HSN_code,
        total_quantity_subquery.c.category,
        total_quantity_subquery.c.bike_category,
        total_quantity_subquery.c.color,
        total_quantity_subquery.c.size,
        total_quantity_subquery.c.city,
        total_quantity_subquery.c.product_name,
        func.coalesce(total_quantity_subquery.c.total_quantity - used_quantity_subquery.c.total_used_quantity, total_quantity_subquery.c.total_quantity).label('remaining_quantity')
    ).outerjoin(
        used_quantity_subquery,
        and_(
            total_quantity_subquery.c.HSN_code == used_quantity_subquery.c.HSN_code,
            total_quantity_subquery.c.product_name == used_quantity_subquery.c.product_name,
            total_quantity_subquery.c.category == used_quantity_subquery.c.category,
            total_quantity_subquery.c.bike_category == used_quantity_subquery.c.bike_category,
            total_quantity_subquery.c.color == used_quantity_subquery.c.color,
            total_quantity_subquery.c.size == used_quantity_subquery.c.size,
            total_quantity_subquery.c.city == used_quantity_subquery.c.city
        )
    ).order_by(desc(total_quantity_subquery.c.created_at))  # Order by created_at in descending order

    # Format the result
    result = [
        {
            "hsn_code" : row.HSN_code,
            "category": row.category,
            "bike_category": row.bike_category,
            "color": row.color,
            "size": row.size,
            "city": row.city,
            "product_name": row.product_name,
            "remaining_quantity": row.remaining_quantity
        } 
        for row in db_distinct
    ]
    
    return {
        "distinct_values": result
    }


@product_router.get("/products/amount/sum/{invoice_id}")
def match_sum(
    invoice_id : str ,
    db: Session = Depends(get_db)
):
    total_sum = db.query(func.sum(ProductDB.amount_with_gst)).filter(ProductDB.invoice_id == invoice_id).scalar()

    invoice = db.query(InventoryDB).filter(InventoryDB.invoice_id == invoice_id).first()

    price_diffrence = invoice.invoice_amount - total_sum

    return {
        "status" : status.HTTP_200_OK,
        "Price Difference" : price_diffrence
    }
