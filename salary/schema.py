from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional

class RequestData(BaseModel):
    field1: Optional[str]
    field2: Optional[int]
    field3: Optional[bool]

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.field1 = data.get("field1", None)
        self.field2 = data.get("field2", None)
        self.field3 = data.get("field3", None)


class SalarySchema(BaseModel):
    first_partition: Optional[int] = None
    second_partition: Optional[int] = None
    third_partition: Optional[int] = None

