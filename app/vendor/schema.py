from typing import Dict, List
from pydantic import BaseModel

class BankDetails(BaseModel):
    account_number : int
    IFSC_code : str
    bank_name : str
    party_name : str

    class Config:
        from_attributes = True

class VendorSchema(BaseModel):
    vender_name : str
    working_city : str
    register_address : str
    GST_number : str
    HSN_code : str
    PAN_number : str
    chapter_head : str
    email : List[str]
    mobile_number : List[str]        
    bank_details : BankDetails

    class Config:
        from_attributes = True

