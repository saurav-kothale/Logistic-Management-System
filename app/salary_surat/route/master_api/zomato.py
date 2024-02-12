
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File
from app.salary_surat.schema.swiggy_structure2 import SuratSwiggySchema
from app.salary_surat.schema.zomato_structure1 import SuratZomatoStructure1
from app.salary_surat.schema.zomato_structure2 import SuratZomatoStructure2
import pandas as pd
from app.salary_surat.view.zomato_structure1 import calculate_zomato_surat
from app.salary_surat.route.zomato_structure2 import calculate_zomato_salary_structure2

master_router = APIRouter()

@master_router.post("/zomato/master")
def master_salary(  
    structure_name : str,  
    structure1 : Optional[SuratZomatoStructure1] = Depends(),
    structure2 : Optional[SuratZomatoStructure2] = Depends(),
    file : UploadFile = File(...),
 ):
    df = pd.read_excel(file.file)

    if structure_name == "structure1":
        response = calculate_zomato_surat(
            df=df,
            structure=structure1,
            filename= file.filename
        )

    elif structure_name == "structure2":
        response = calculate_zomato_salary_structure2(
            df=df,
            structure = structure2,
            filename = file.filename
        )

    return response






    