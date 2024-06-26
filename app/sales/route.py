from fastapi import APIRouter, Depends, HTTPException, status
from app.sales.schema import SalesSchema
from app.sales.model import SalesModel
from sqlalchemy.orm import Session
from database.database import get_db
import uuid
from app.sales.view import kilometer_run, vehicle_repair

sales_router = APIRouter()

@sales_router.post("/sales")
def create_sales(
    schema : SalesSchema,
    db : Session = Depends(get_db)
    
):
    battery_run_count = (schema.shift_1 * 1) + (schema.shift_2 * 2) + (schema.shift_3 * 3) + (schema.shift_4 * 4)
    bike_run_count = schema.shift_1 + schema.shift_2 + schema.shift_3 + schema.shift_4
    battery_kilometer_run = kilometer_run(schema.client, battery_run_count)
    bike_kilometer_run = kilometer_run(schema.client, bike_run_count)
    co2_emision = battery_kilometer_run * 0.137
    total_riders = schema.partime_rider + schema.fulltime_rider
    total_orders = schema.partime_order + schema.fulltime_order
    average_rider_count = schema.vehicle_deploy
    total_vehicle = schema.opening_vehicles + schema.vehicles_added - schema.vehicles_remove
    active_vehicle = schema.vehicle_deploy,
    vehicle_under_repair = vehicle_repair(schema, total_vehicle, schema.vehicle_deploy)


    db_sales = SalesModel(
        id = str(uuid.uuid4()),
        year = schema.year,
        client = schema.client,
        city = schema.city,
        month = schema.month,
        fulltime_rider = schema.fulltime_rider,
        fulltime_order = schema.fulltime_order,
        partime_rider = schema.partime_rider,
        partime_order = schema.partime_order,
        average_rider = schema.average_rider,
        carry_forward = schema.carry_forward,
        new_join_rider = schema.new_join_rider,
        left_rider = schema.left_rider,
        shift_1 = schema.shift_1,
        shift_2 = schema.shift_2,
        shift_3 = schema.shift_3,
        shift_4 = schema.shift_4,
        sales_with_gst = schema.sales_with_gst,
        sales_without_gst = schema.sales_without_gst,
        payout_with_gst = schema.payout_with_gst,
        payout_without_gst = schema.payout_without_gst,
        opening_vehicles = schema.opening_vehicles,
        vehicles_added = schema.vehicles_added,
        vehicles_remove = schema.vehicles_remove,
        vehicle_deploy = schema.vehicle_deploy,
        battery_run_count = battery_run_count,
        bike_run_count = bike_run_count,
        battery_kilometer_run = battery_kilometer_run,
        bike_kilometer_run = bike_kilometer_run,
        co2_emission = co2_emision,
        total_riders = total_riders,
        total_orders = total_orders,
        average_rider_count = average_rider_count,
        total_vehicle = total_vehicle,
        active_vehicle = active_vehicle,
        vehicle_under_repair = vehicle_under_repair
    )

    db.add(db_sales)

    db.commit()

    return {
        "status" : status.HTTP_201_CREATED,
        "message" : "sale created successfully",
        "sales" : db_sales.id
    }


@sales_router.get('/sales')
def get_sales(
    db : Session = Depends(get_db)
):

    db_sales = db.query(SalesModel).all()

    if not db_sales:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail= "Sales data not found"
        )
    
    return {
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "record fetched successfully",
        "sales" : db_sales
    }


@sales_router.get("/sales/{id}")
def get_sale(
    db : Session = Depends(get_db),
    id = str
):
    
    db_sales = db.query(SalesModel).filter(SalesModel.id == id).first()

    if not db_sales:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found for given id"
        )
    
    return{
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "record fetched successfully",
        "sales" : db_sales
        }


@sales_router.patch("/sales/{id}")
def update_sale(
    id : str,
    schema : SalesSchema,
    db : Session = Depends(get_db),
):
    db_sales = db.query(SalesModel).filter(SalesModel.id == id).first()

    if not db_sales:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "record not found to update"
        )
    battery_run_count = (schema.shift_1 * 1) + (schema.shift_2 * 2) + (schema.shift_3 * 3) + (schema.shift_4 * 4)
    bike_run_count = schema.shift_1 + schema.shift_2 + schema.shift_3 + schema.shift_4
    battery_kilometer_run = kilometer_run(schema.client, battery_run_count)
    bike_kilometer_run = kilometer_run(schema.client, bike_run_count)
    co2_emision = battery_kilometer_run * 0.137
    total_riders = schema.partime_rider + schema.fulltime_rider
    total_orders = schema.partime_order + schema.fulltime_order
    average_rider_count = schema.vehicle_deploy
    total_vehicle = schema.opening_vehicles + schema.vehicles_added - schema.vehicles_remove
    active_vehicle = schema.vehicle_deploy,
    vehicle_under_repair = vehicle_repair(schema, total_vehicle, schema.vehicle_deploy)
    
    db_sales.year = schema.year
    db_sales.client = schema.client
    db_sales.city = schema.city
    db_sales.month = schema.month
    db_sales.fulltime_rider = schema.fulltime_rider
    db_sales.fulltime_order = schema.fulltime_order
    db_sales.partime_rider = schema.partime_rider
    db_sales.partime_order = schema.partime_order
    db_sales.average_rider = schema.average_rider
    db_sales.carry_forward = schema.carry_forward
    db_sales.new_join_rider = schema.new_join_rider
    db_sales.left_rider = schema.left_rider
    db_sales.shift_1 = schema.shift_1
    db_sales.shift_2 = schema.shift_2
    db_sales.shift_3 = schema.shift_3
    db_sales.shift_4 = schema.shift_4
    db_sales.sales_with_gst = schema.sales_with_gst
    db_sales.sales_without_gst = schema.sales_without_gst
    db_sales.payout_with_gst = schema.payout_with_gst
    db_sales.payout_without_gst = schema.payout_without_gst
    db_sales.opening_vehicles = schema.opening_vehicles
    db_sales.vehicles_added = schema.vehicles_added
    db_sales.vehicles_remove = schema.vehicles_remove
    db_sales.vehicle_deploy = schema.vehicle_deploy
    db_sales.battery_run_count = battery_run_count
    db_sales.bike_run_count = bike_run_count
    db_sales.battery_kilometer_run = battery_kilometer_run
    db_sales.bike_kilometer_run = bike_kilometer_run
    db_sales.co2_emission = co2_emision
    db_sales.total_riders = total_riders
    db_sales.total_orders = total_orders
    db_sales.average_rider_count = average_rider_count
    db_sales.total_vehicle = total_vehicle
    db_sales.active_vehicle = active_vehicle
    db_sales.vehicle_under_repair = vehicle_under_repair

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record Updated successfully",
        "record" : db_sales.id
    }


@sales_router.delete("/sales/{id}")
def delete_sales(
    id : str,
    db : Session = Depends(get_db),    
):
    db_sale = db.query(SalesModel).filter(SalesModel.id == id).first()

    if not db_sale:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "record not found to delete"
        )
    
    db.delete(db_sale)

    db.commit()

    return{
        "status" : status.HTTP_200_OK,
        "message" : "Record delete successfully",
        "record_id" : db_sale.id 
    }

