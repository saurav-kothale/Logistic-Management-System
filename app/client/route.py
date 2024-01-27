from typing import List
from xml.sax import default_parser_list
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from app.client.schema import ClientSchema
from database.database import SessionLocal
from app.client.model import Client

client_router = APIRouter()
db = SessionLocal()


@client_router.post("/clients")
def create_vender(client : ClientSchema):
    old_client = db.query(Client).filter(Client.client_name == client.client_name).first()

    if old_client is not None:
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail = "client name already exist5")
    
    # documents_name = [file.filename for file in document]

    # if not documents_name:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail= "Document is not found Please upload the document"
    #     )

    new_client = Client(
        client_name = client.client_name,
        client_hub_name = client.client_hub_name,
        address = client.address,
        city = client.city,
        GST_number = client.GST_number,
        email = client.email,
        mobile_number = client.mobile_number,
        HSN_code = client.HSN_code,
        PAN_number = client.PAN_number,
        bank_details = dict(client.bank_details),
        document = "my_doc"
    )

    db.add(new_client)

    db.commit()

    return {
        "status" : status.HTTP_201_CREATED, 
        "message" : "Client Created Successfully"
    }

@client_router.get("/clients/getclients")
def get_clients():
    all_clients = db.query(Client).all()
    
    return {
        "data" : all_clients,
        "status" : status.HTTP_200_OK,
        "message" : "Successfullly get all the client"
    }


@client_router.get('clients/{client_id}')
def get_client(client_id : str):
    db_client = db.query(Client).filter(Client.client_id == client_id).first()

    if db_client is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "client not found"
        )

    return {
        "data" : db_client,
        "status" : status.HTTP_200_OK,
        "message" : "client fetch successfully"
    }


@client_router.patch('/clients/{client_id}' )
def update_client(client_id : str, client : ClientSchema):
    db_client = db.query(Client).filter(Client.client_id == client_id).first()

    if db_client is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "client not found"
        )
    
    db_client.client_name = client.client_name  # type: ignore
    db_client.client_hub_name = client.client_hub_name # type: ignore
    db_client.address = client.address # type: ignore
    db_client.city = client.city # type: ignore
    db_client.GST_number = client.GST_number   # type: ignore 
    db_client.email = client.email # type: ignore
    db_client.mobile_number = client.mobile_number # type: ignore
    db_client.HSN_code = client.HSN_code # type: ignore
    db_client.PAN_number = client.PAN_number # type: ignore
    db_client.bank_details = dict(client.bank_details) # type: ignore

    db.commit()

    return{
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "Client updated successfully"
    }


@client_router.delete("/clients/{client_id}")
def delete_client(client_id : str):
    db_client = db.query(Client).filter(Client.client_id == client_id).first()

    if db_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Client Not Found"
        )
    
    db.delete(db_client)
    db.commit()

    return {"data": db_client, "status": 200, "message": "Client deleted successfully"} 
