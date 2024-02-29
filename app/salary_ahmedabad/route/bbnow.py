from fastapi import APIRouter, Depends, UploadFile, File
from app.salary_ahmedabad.schema.bbnow import AhmedabadBbnowSchema

ahmedabadbbnow_router = APIRouter()

@ahmedabadbbnow_router.post("/bbnow/structure1")
def get_salary(data : AhmedabadBbnowSchema = Depends(), file : UploadFile = File(...)):