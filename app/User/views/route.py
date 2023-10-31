from fastapi import APIRouter, HTTPException, status , Depends
from database.db import SessionLocal
from app.User.user.model.user import User
from app.User.user.schema.user import (
    ResetPasswordData,
    UserLoginData,
    UserSignupData,
    mobile_no_varification
)
from datetime import timedelta

from werkzeug.security import generate_password_hash , check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from uuid import uuid4

signup_router = APIRouter()
db = SessionLocal()


@signup_router.post("/signup" , status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserSignupData):

    db_entry = db.query(User).filter(User.username == user_data.username).first()

    if db_entry is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail = "User already exist."
        )
   
    db_entry = db.query(User).filter(User.email_id == user_data.email_id).first()

    if db_entry is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist."
        )

    if mobile_no_varification(user_data.mobile_no) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST , detail="Mobile Number is not valid."
        )    

    if user_data.password != user_data.retype_password:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="retype password should be same as password",
        )

    user = User(
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        username = user_data.username,
        user_id = uuid4(),
        email_id = user_data.email_id,
        mobile_no = user_data.mobile_no,
        password = generate_password_hash(user_data.password),
        retype_password = generate_password_hash(user_data.retype_password),
    )

    db.add(user)

    db.commit()

    return {"status": status.HTTP_200_OK, "message": "User created successfully"}


login_router = APIRouter()


@login_router.post("/login", status_code=status.HTTP_201_CREATED)
def log_in(user_data : UserLoginData , Authorize : AuthJWT = Depends()):
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if db_user and check_password_hash(db_user.password , user_data.password):

        expires = timedelta(days = 1) 
        access_token = Authorize.create_access_token(subject = db_user.user_id , expires_time = expires)

        response = {
            "access" : access_token,
            "massage" : "User Login Successfully"
        }

        return jsonable_encoder(response)
    
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = "Invalid Username Or Password")


protected_router = APIRouter()
 

@protected_router.get("/protected") 
def protected (Authorize : AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()

    return {"user" : current_user}




forgot_password_route = APIRouter()


@forgot_password_route.post("/forget_password", status_code = status.HTTP_201_CREATED)
def recover_password(user_data: ResetPasswordData):

    db_entry = db.query(User).filter(User.username == user_data.username).first()

    if db_entry is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST , detail="email not found"
        )

    return {
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "Link has been sent to your registered Email_id or Mobile number",
    }


delete_route = APIRouter()


@delete_route.delete("/delete" , status_code=status.HTTP_200_OK)
def delete_user(user_data : UserLoginData):
    user_to_delete = db.query(User).filter(User.username == user_data.username).first()
     
    if user_to_delete and check_password_hash(user_to_delete.password , user_data.password):
        db.delete(user_to_delete)
        db.commit() 

        return {
            "data" : user_to_delete,
            "status" : 200,
            "message" : "User delete successfully"
            }

    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = "Invalid Username or Password")






