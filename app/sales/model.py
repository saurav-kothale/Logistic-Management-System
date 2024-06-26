from re import T
from numpy import average
from database.database import Base
from sqlalchemy import Column, Integer, String

class SalesModel(Base):
    __tablename__ = "sales"
    id = Column(String, primary_key=True)
    year = Column(String)
    client = Column(String)
    city = Column(String)
    month = Column(String)
    fulltime_rider = Column(Integer)
    fulltime_order = Column(Integer)
    partime_rider = Column(Integer)
    partime_order = Column(Integer)
    average_rider = Column(Integer)
    carry_forward = Column(Integer)
    new_join_rider = Column(Integer)
    left_rider = Column(Integer)
    shift_1 = Column(Integer)
    shift_2 = Column(Integer)
    shift_3 = Column(Integer)
    shift_4 = Column(Integer)
    sales_with_gst = Column(Integer)
    sales_without_gst = Column(Integer)
    payout_with_gst = Column(Integer)
    payout_without_gst = Column(Integer)
    opening_vehicles = Column(Integer)
    vehicles_added = Column(Integer)
    vehicles_remove = Column(Integer)
    vehicle_deploy = Column(Integer)
    battery_run_count = Column(Integer)
    bike_run_count = Column(Integer)
    battery_kilometer_run = Column(Integer)
    bike_kilometer_run = Column(Integer)
    co2_emission = Column(Integer)
    total_riders = Column(Integer)
    total_orders = Column(Integer)
    average_rider_count = Column(Integer)
    total_vehicle = Column(Integer)
    active_vehicle = Column(Integer)
    vehicle_under_repair = Column(Integer)

