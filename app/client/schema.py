from typing import Dict, List
from pydantic import BaseModel

class BankDetails(BaseModel):
    account_number : int
    IFSC_code : str
    bank_name : str
    party_name : str

    class Config:
        from_attributes = True

class ClientSchema(BaseModel):
    client_name : str
    client_hub_name : str
    address : str
    city : str
    GST_number : str
    email : List[str]
    mobile_number : List[str]
    HSN_code : str
    PAN_number : str
    bank_details : BankDetails

    class Config:
        from_attributes = True

