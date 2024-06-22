from pydantic import BaseModel

class SalesSchema(BaseModel):
    year : str
    client : str
    city : str
    month : str
    fulltime_rider : int
    fulltime_order : int
    partime_rider : int
    partime_order : int
    average_rider : int
    carry_forward : int
    new_join_rider : int
    left_rider : int
    shift_1 : int
    shift_2 : int
    shift_3 : int
    shift_4 : int
    sales_with_gst : int
    sales_without_gst : int
    payout_with_gst : int
    payout_without_gst : int
    opening_vehicles : int
    vehicles_added : int
    vehicles_remove : int
    active_vehicle : int
    vehicle_deploy : int
    vehicle_under_repair : int
    
