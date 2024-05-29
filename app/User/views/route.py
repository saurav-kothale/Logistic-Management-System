from fastapi import APIRouter, HTTPException, status , Depends
from database.database import SessionLocal, get_db
from app.User.user.model.user import User
from app.User.user.schema.user import (
    ResetPasswordData,
    UserLoginData,
    UserSignupData,
    mobile_no_varification, mobile_no_varification_updated
)
from datetime import timedelta

from werkzeug.security import generate_password_hash , check_password_hash
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
# from app.utils.util import signJWT, decodeJWT, get_current_user
from app.utils.util import create_access_token, get_current_user 

# from app.utils.auth_bearer import JWTBearer
from sqlalchemy.orm import Session
from decouple import config
from app import setting

signup_router = APIRouter()
accesstoken_expire_time = setting.ACCESSTOKEN_EXPIRE_TIME


@signup_router.post("/signup" , status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserSignupData, db : Session = Depends(get_db)):

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
    db_mobile_number = db.query(User).filter(User.mobile_no == user_data.mobile_no).first()

    if db_mobile_number:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mobile Number already exists"
        )


    if mobile_no_varification_updated(user_data.mobile_no) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST , detail="Mobile Number is not valid.Make sure you provided Contry code as well"
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
def log_in(user_data : UserLoginData, db : Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email_id == user_data.email_id).first()
    if db_user and check_password_hash(db_user.password , user_data.password): # type: ignore


        access_token_data = {
            "user_id" : db_user.user_id,
            "first_name" : db_user.first_name,
            "last_name" : db_user.last_name,
            "user_name" : db_user.username,
            "mobile_number" : db_user.mobile_no,
            "email_id" : db_user.email_id

        }

        access_token = create_access_token(access_token_data, int(accesstoken_expire_time))

        response = {
            "access" : access_token,
            "massage" : "User Login Successfully"
        }

        return jsonable_encoder(response)
    
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = "Invalid Username Or Password")


protected_router = APIRouter()
 

@protected_router.get("/protected") 
def protected (current_user : str = Depends(get_current_user)):
    return {"user" : current_user}



forgot_password_route = APIRouter()


@forgot_password_route.post("/forget_password", status_code = status.HTTP_201_CREATED)
def recover_password(user_data: ResetPasswordData, db : Session = Depends(get_db)):

    db_entry = db.query(User).filter(User.email_id == user_data.email_id).first()

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
def delete_user(user_data : UserLoginData, db : Session = Depends(get_db)):
    user_to_delete = db.query(User).filter(User.email_id == user_data.email_id).first()
     
    if user_to_delete and check_password_hash(user_to_delete.password, user_data.password): # type: ignore
        db.delete(user_to_delete)
        db.commit() 

        return {
            "data" : user_to_delete,
            "status" : 200,
            "message" : "User delete successfully"
            }

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Invalid Username or Password"
    )






