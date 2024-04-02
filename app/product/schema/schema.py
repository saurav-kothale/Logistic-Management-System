from numpy import size
from pydantic import BaseModel
from enum import Enum

class Category(Enum):
    Break_Lever_Asambly = "Break Lever Asambly"
    Front_Barring_6201 = "Front Barring 6201"
    Front_Shocker_Seal = "Front Shocker Seal"
    Stering_Bearing_Small = "Stering Bearing Small"
    Stering_Bearing_Big = "Stering Bearing Big"
    Mutgaurd_Front_Silver = "Mutgaurd Front Silver"
    Mutgaurd_Front_Black = "Mutgaurd Front Black"
    Flasher_With_Buzzer = "Flasher With Buzzer"
    Headlight_Fairing_Silver = "Headlight Fairing Silver"
    Headlight_Fairing_Black = "Headlight Fairing Black"
    Headlight_Assambly = "Headlight Assambly"
    Headlight_Holder = "Headlight Holder"
    Relay = "Relay"
    Lock_Set = "Lock Set"
    Lithium_Socket_Female = "Lithium Socket Female"
    Rear_Bearing_6204 = "Rear Bearing 6204"
    Dual_Battery_Switch = "Dual Battery Switch"
    Dual_Battery_Switch_With_Wire = "Dual Battery Switch With Wire"
    Holder_Plate_Front_Break_Liner_Plate = "Holder Plate Front Break Liner Plate"
    Holder_Plate_Rear_Break_Liner_Plate = "Holder Plate Rear Break Liner Plate"
    Tail_Light_Assambly = "Tail Light Assambly"
    Stering_Bearing_Kit = "Stering Bearing Kit"
    Output_Socket_Charger = "Output Socket Charger"
    Sensor_Board = "Sensor Board"
    Side_Indication_Assambly_Left = "Side Indication Assambly Left"
    Side_Indication_Assambly_Right = "Side Indication Assambly Right"
    Side_Lower_Panal_Silver = "Side Lower Panal_Silver"
    Wing_Shield_Lower_Panal = "Wing Shield Lower Panal"
    Headlight = "Headlight"
    Front_Mudgaurd = "Front Mudgaurd"
    Bearing_6200 = "Bearing 6200"
    Front_Break_Linear_Plate = "Front Break Linear Plate"
    Jaw_Holder_Break_Linear_Plate_Rear = "Jaw Holder Break Linear Plate Rear"
    Lower_Side_Panal = "Lower Side Panal"
    Headlight_Switch = "Headlight Switch"
    Indicator_Switch = "Indicator Switch"
    Deeper_Switch = "Deeper Switch"
    Horn_Switch = "Horn Switch"
    Side_Stand_Spring = "Side Stand Spring"
    Bag_Hook = "Bag Hook"
    Motor_Bearing_Rear_6204 = "Motor Bearing Rear 6204"
    Motor_Bearing_Rear_6203 = "Motor Bearing Rear 6203"
    Mutgaurd_Bracket = "Mutgaurd Bracket"
    Throttle_Accelator = "Throttle (Accelator)"
    Connector = "Connector"
    Wing_Shield_Lower = "Wing Shield Lower"
    Rear_Indicator_Glass_Left = "Rear Indicator Glass Left"
    Rear_Indicator_Glass_Right = "Rear Indicator Glass Right"
    Tail_Light_Red_Lens = "Tail Light Red Lens"
    Swim_Arm_Cover = "Swim Arm Cover"
    Horn = "Horn"
    Dc_Convertor = "Dc Convertor"
    Side_Panal = "Side Panal"
    Side_Stand = "Side Stand"
    Wheel_Rim = "Wheel Rim"
    Front_Jumper = "Front Jumper"
    Fork_T = "Fork_T"
    Front_Side_Light = "Front Side Light"
    Rear_Side_Light = "Rear Side Light"
    Mudgaurd_Bracket = "Mudgaurd Bracket"
    Handle_Bar = "Handle Bar"
    Break_Linear = "Break Linear"
    Charging_Socket_Worio = "Charging Socket Worio"
    Break_Wire_Front = "Break Wire Front"
    Break_Wire_Rear = "Break Wire Rear"
    Headlight_Bulb = "Headlight Bulb"
    Anderson_Socket = "Anderson Socket"
    Nut_Bold = "Nut Bold"
    Puncture_Kit = "Puncture Kit"


class BikeCategory(Enum):
    OPTIMA = "OPTIMA"
    NYX = "NYX"
    BGAUSS = "BGAUSS"
    other = "OTHER"


class Size(Enum):
    S_110_MM = "110 MM"
    S_130_MM = "130 MM"
    S_10_MM = "10 MM"
    S_20_MM = "20 MM"
    OTHER = "OTHER"


class Color(Enum):
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"
    SILVER = "SILVER"
    OTHER = "OTHER"


class City(Enum):
    SURAT = "SURAT"
    AHMEDABAD = "AHMEDABAD"
    VADODARA = "VADODARA"


class ProductSchema(BaseModel):
    product_name: str
    category : Category
    bike_category : BikeCategory
    quantity : int
    size : Size
    color : Color
    city : City    



