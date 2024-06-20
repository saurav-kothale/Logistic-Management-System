
from email import message
from typing import Optional,Union
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.salary_surat.schema.swiggy_structure2 import SuratSwiggySchema
from app.salary_surat.schema.zomato_structure1 import SuratZomatoStructure1
from app.salary_surat.schema.zomato_structure2 import SuratZomatoStructure2
import pandas as pd
from app.salary_surat.view.zomato_structure2 import calculate_salary_surat
# from app.salary_surat.route.zomato_structure2 import calculate_zomato_salary_structure2

master_router = APIRouter()

# @master_router.post("/zomato/master")
# def master_salary(  
#     # structure_name : str,  
#     structure_data: Union[SuratZomatoStructure1, SuratZomatoStructure2],
#     # file : UploadFile = File(...),
#  ):
#     # df = pd.read_excel(file.file)

#     if isinstance(structure_data, SuratZomatoStructure1):
#         result = {"message": f"Using Schema1 with param1:"}
#     #     response = calculate_zomato_surat(
#     #         df=df,
#     #         structure=structure_data,
#     #         filename= file.filename
#     #     )

#     elif isinstance(structure_data, SuratZomatoStructure2):
#         result = {"message": f"Using Schema2 with param3"}
#     #     response = calculate_zomato_salary_structure2(
#     #         df=df,
#     #         structure = structure_data,
#     #         filename = file.filename
#     #     )
#     else:
#         # Handle invalid structure_name or mismatched structure_data
#         raise HTTPException(status_code=400, detail="Invalid structure_name or structure_data mismatch")

#     return result
