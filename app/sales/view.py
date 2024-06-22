def kilometer_run(client, battery_run_count):
    client = client.lower()
    if client in ["swiggy", "zomato", "blinkit"]:
        return battery_run_count * 80
    
    return battery_run_count * 100

def vehicle_repair(schema, total_vehicle, vehicle_deployed):
    
    if schema.city == "surat":

        return total_vehicle - vehicle_deployed * 0.41

    elif schema.city == "ahmedabad":

        return total_vehicle - vehicle_deployed * 0.38
    
    elif schema.city == "vadodara":

        return total_vehicle - vehicle_deployed * 0.28
