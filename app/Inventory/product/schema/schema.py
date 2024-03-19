from pydantic import BaseModel
from enum import Enum

class BikeCategory(Enum):
    optima_cx_er = "OPTIMA CX ER"
    nyx_cx_er = "NYX CX ER"
    bgauss_c12i_max = "BGAUSS C12i MAX"
    optima_hs_500_er = "OPTIMA HS 500 ER"
    praise_pro = "PRAISE PRO"
    magnus_ex = "MAGNUS EX"
    nyx_hs_500_er = "NYX HS 500 ER"
    optima_cx = "OPTIMA CX"
    emerge = "EMERGE"
    warivo_motor_nexa_ex60 = "WARIVO MOTOR NEXA EX60"
    ape_e_xtra_fx_pu = "APE E XTRA FX PU"
    exyride = "EZYRIDE"
    stella = "STELLA"

class SubCategory(Enum):
    Headlight = "Headlight"
    Switches = "Switches"
    Horn = "Horn"
    Break = "Break"


class ProductSchema(BaseModel):
    product_name: str
    bike_category : BikeCategory
    sub_category : SubCategory
    quantity : int
    size : str
    city : str