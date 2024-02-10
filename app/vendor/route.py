from typing import List
from xml.sax import default_parser_list
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from app.file_system.s3_events import upload_file
from app.vendor.schema import VendorSchema
from database.database import SessionLocal
from app.vendor.model import Vendor

vendor_router = APIRouter()
db = SessionLocal()


@vendor_router.post("/vender")
def create_vender(vender: VendorSchema):
    old_vendor = (
        db.query(Vendor).filter(Vendor.vendor_name == vender.vender_name).first()
    )

    if old_vendor is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="vendor name already exist5"
        )

    # documents_name = [file.filename for file in document]

    # if not documents_name:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail= "Document is not found Please upload the document"
    #     )

    new_vendor = Vendor(
        vendor_name=vender.vender_name,
        working_city=vender.working_city,
        register_address=vender.register_address,
        GST_number=vender.GST_number,
        HSN_code=vender.HSN_code,
        PAN_number=vender.PAN_number,
        chapter_head=vender.chapter_head,
        email=vender.email,
        mobile_number=vender.mobile_number,
        bank_details=dict(vender.bank_details),
        document="my doc",
    )

    db.add(new_vendor)

    db.commit()

    return {"status": status.HTTP_201_CREATED, "message": "Client Created Successfully"}


@vendor_router.get("/venders/getvenders")
def get_clients():
    all_vendor = db.query(Vendor).all()

    return {
        "data": all_vendor,
        "status": status.HTTP_200_OK,
        "message": "Successfullly get all the client",
    }


@vendor_router.get("venders/{vender_id}")
def get_client(vender_id: str):
    db_vendor = db.query(Vendor).filter(Vendor.vender_id == vender_id).first()

    if db_vendor is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="client not found"
        )

    return {
        "data": db_vendor,
        "status": status.HTTP_200_OK,
        "message": "client fetch successfully",
    }


@vendor_router.patch("/clients/{vendor_id}")
def update_client(vendor_id: str, vendor: VendorSchema):
    db_vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()

    if db_vendor is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="vendor not found"
        )

    db_vendor.vendor_name = vendor.vendor_name  # type: ignore
    db_vendor.working_city = vendor.working_city  # type: ignore
    db_vendor.register_address = vendor.register_address  # type: ignore
    db_vendor.GST_number = vendor.GST_number  # type: ignore
    db_vendor.HSN_code = vendor.HSN_code  # type: ignore
    db_vendor.PAN_number = vendor.PAN_number  # type: ignore
    db_vendor.chapter_head = vendor.chapter_head  # type: ignore
    db_vendor.email = vendor.email  # type: ignore
    db_vendor.mobile_number = vendor.mobile_number  # type: ignore
    db_vendor.bank_details = dict(vendor.bank_details)  # type: ignore

    db.commit()

    return {
        "status": status.HTTP_202_ACCEPTED,
        "message": "Vendor updated successfully",
    }


@vendor_router.delete("/clients/{vendor_id}")
def delete_client(vendor_id: str):
    db_vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()

    if db_vendor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client Not Found"
        )

    db.delete(db_vendor)
    db.commit()

    return {"data": db_vendor, "status": 200, "message": "Client deleted successfully"}
