from logging import exception
from app.salary_surat.view.view import calculate_amount_for_zomato_surat
import pandas as pd
import tempfile
import uuid
from datetime import datetime
from app.salary_surat.model.model import SalaryFile
from decouple import config
from database.database import SessionLocal
from app.file_system.s3_events import read_s3_contents, s3_client, upload_file


db = SessionLocal()
row_bucket = config("ROW_BUCKET")
processed_bucket = config("PROCESSED_FILE_BUCKET")

def calculate_zomato_surat(df, structure, filename):

        df["DATE"] = pd.to_datetime(df["DATE"])

        df = df[(df["CITY NAME"] == "Surat") & (df["CLIENT NAME"] == "Zomato")]
        df["Total_Earning"] = df.apply(
            calculate_amount_for_zomato_surat,
            args=(
                structure.first_order_from,
                structure.first_order_to,
                structure.first_week_amount,
                structure.first_weekend_amount,
                structure.second_order_from,
                structure.second_order_to,
                structure.second_week_amount,
                structure.second_weekend_amount,
                structure.order_grether_than,
                structure.week_amount,
                structure.weekend_amount,
                structure.maximum_rejection,
                structure.rejection_amount,
                structure.bad_order_amount,
                structure.maximum_bad_orders,
            ),
            axis=1,
        )

        df["Total_Orders"] = df["Document DONE ORDERS"] + df["Parcel DONE ORDERS"]

        table = pd.pivot_table(
            data=df,
            index=["DRIVER_ID", "DRIVER_NAME", "CLIENT NAME", "CITY NAME"],
            aggfunc={
                "REJECTION": "sum",
                "BAD ORDER": "sum",
                "Total_Earning": "sum",
                "Parcel DONE ORDERS": "sum",
                "CUSTOMER_TIP": "sum",
                "RAIN ORDER": "sum",
                "IGCC AMOUNT": "sum",
                "ATTENDANCE": "sum",
                "Total_Orders": "sum",
            },
        ).reset_index()

        zomato_surat_table = pd.DataFrame(table)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
                zomato_surat_table.to_excel(writer, sheet_name="Sheet1", index=False)

            file_id = uuid.uuid4()
            file_key = f"uploads/{file_id}/{filename}"

            new_file = SalaryFile(
                filekey=file_key,
                file_name=filename,
                file_type=".xlsx",
                created_at=datetime.now(),
            )

            db.add(new_file)

            db.commit()

            try:
                s3_client.upload_fileobj(temp_file, processed_bucket, file_key)

            except exception as e:
                return {"error": e}

        return {
            "message": "Successfully Calculated Salary for Zomato Surat",
            "file_id": file_id,
            "file_name": filename,
        }