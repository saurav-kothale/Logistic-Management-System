from curses.ascii import HT
from itertools import product
from fastapi import APIRouter, Depends, HTTPException, status
from app.Inventory_in.product_category.schema import ProductCategorySchema
from app.Inventory_in.product_category.model import ProductCategoryDB
from sqlalchemy.orm import Session
from app.utils.util import get_current_user
from database.database import get_db
import uuid
from sqlalchemy.sql.expression import func


product_cateogry_router = APIRouter()

@product_cateogry_router.post("/product_category/category")
def create_product(
    schema : ProductCategorySchema,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    db_product = db.query(ProductCategoryDB).filter(func.lower(ProductCategoryDB.product_name) == func.lower(schema.product_name)).first()

    if db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name already exist"
        )
    
    new_product = ProductCategoryDB(
        product_id = str(uuid.uuid4()),
        product_name = schema.product_name,
        HSN_code = schema.hsn_code,
        category = schema.category,
        user = current_user

    )


    db.add(new_product)

    db.commit()

    return{
        "status" : status.HTTP_201_CREATED,
        "message" : "Product category created successfully",
        "product_category" : {
            "product_id" : new_product.product_id,
            "product_name" : new_product.product_name,
            "category" : new_product.category,
            "HSN_code" : new_product.HSN_code,
            "user" : new_product.user

        }
    }
        

@product_cateogry_router.get("/get/product_category")
def get_products(
    db : Session = Depends(get_db)
):
    
    db_products = db.query(ProductCategoryDB).all()

    if not db_products:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "product categories fetched successfully",
        "products" : db_products
    }

@product_cateogry_router.get("/get/product_category/id/{product_id}")
def get_product_by_id(
    product_id : str,
    db : Session = Depends(get_db)
):
    
    db_product = db.query(ProductCategoryDB).filter(ProductCategoryDB.product_id == product_id).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "product category fetched successfully",
        "products" : db_product
    }


@product_cateogry_router.get("/get/product_category/{hsn_code}")
def get_product(
    hsn_code : str,
    db : Session = Depends(get_db)
):
    
    db_product = db.query(ProductCategoryDB).filter(ProductCategoryDB.HSN_code == hsn_code).all()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "product category fetched successfully",
        "products" : db_product
    }

@product_cateogry_router.patch("/get/product_category/{product_id}")
def update_product(
    product_id : str,
    schema : ProductCategorySchema,
    db : Session = Depends(get_db)
):
    
    db_product = db.query(ProductCategoryDB).filter(ProductCategoryDB.product_id == product_id).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    existing_product_with_product_name = db.query(ProductCategoryDB).filter(func.lower(ProductCategoryDB.product_name) == func.lower(schema.product_name)).filter(ProductCategoryDB.product_id != product_id).first()

    if existing_product_with_product_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product Name is already present"
        )
    
    
    db_product.product_name = schema.product_name
    db_product.HSN_code = schema.hsn_code
    db_product.category = schema.category

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "product category updated successfully",
        "products" : {
            db_product.product_name,
            db_product.HSN_code,
            db_product.category
        }
    }


@product_cateogry_router.delete("/get/product_category/{product_id}")
def delete_product(
    product_id : str,
    db : Session = Depends(get_db)
):
    
    db_product = db.query(ProductCategoryDB).filter(ProductCategoryDB.product_id == product_id).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not found"
        )
    
    db.delete(db_product)

    db.commit() 
    
    return{
        "status" : status.HTTP_200_OK,
        "message" : "product category deleted successfully",
        "products" : {
            db_product.product_id,
            db_product.product_name,
            db_product.HSN_code,
            db_product.category
        }
    }