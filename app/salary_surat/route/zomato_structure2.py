from fastapi import APIRouter, Body, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy import false
from app.salary_surat.schema.zomato_structure2 import SuratZomatoStructure2
from app.salary_ahmedabad.view.zomato import (
    add_bonus,
    calculate_salary_surat,
    create_table,
)
import pandas as pd
import tempfile, json


surat_zomato_structure2_router = APIRouter()


@surat_zomato_structure2_router.post("/zomato/structure2")
def claculate_salary(data: SuratZomatoStructure2 = Depends(), file: UploadFile = File(...)):

    df = pd.read_excel(file.file)

    df["Total_Amount"] = df.apply(lambda row: calculate_salary_surat(row, data), axis=1)

    table = create_table(df).reset_index()

    table["Total_Amount"] = add_bonus(table)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            table.to_excel(writer, sheet_name="Sheet1", index=False)


    content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = FileResponse(temp_file.name, media_type=content_type)
    response.headers["Content-Disposition"] = (
        'attachment; filename="month_year_city.xlsx"'
    )

    return response


def calculate_zomato_salary_structure2(df, structure, filename):

    df["Total_Amount"] = df.apply(lambda row: calculate_salary_surat(row, structure), axis=1)

    table = create_table(df).reset_index()

    table["Total_Amount"] = add_bonus(table)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            table.to_excel(writer, sheet_name="Sheet1", index=False)


    content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = FileResponse(temp_file.name, media_type=content_type)
    response.headers["Content-Disposition"] = (
        'attachment; filename="month_year_city.xlsx"'
    )

    return response