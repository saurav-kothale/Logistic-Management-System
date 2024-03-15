from fastapi import FastAPI
from app.salary_surat.route.route import salary_router
from app.User.views.route import login_router, signup_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.file_system.route import file_router
from app.client.route import client_router
from app.vendor.route import vendor_router
from app.salary_ahmedabad.route.zomato import ahmedabad_router
from app.salary_surat.route.zomato_structure2 import surat_zomato_structure2_router
from app.salary_surat.route.swiggy_structure2 import surat_swiggy_structure2_router
from app.salary_surat.route.master_api.zomato import master_router
from app.salary_ahmedabad.route.flipkart import ahmedabad_flipkart_router
from app.salary_ahmedabad.route.ecom import ahmedabad_ecom_router
from app.salary_ahmedabad.route.blinkit import ahmedabad_blinkit_router
from app.salary_ahmedabad.route.big_basket import ahmedabadbigbascket
from app.salary_ahmedabad.route.bbnow import ahmedabadbbnow_router
from app.Inventory.route.route import inventory_router

app = FastAPI()


app.include_router(salary_router, prefix="/surat", tags= ["Surat Salary Structure 1"])
app.include_router(signup_router, tags= ["Authentication"])
app.include_router(login_router, tags= ["Authentication"])
app.include_router(file_router, tags=["File Operation"])
app.include_router(client_router, tags= ["Client"])
app.include_router(vendor_router, tags= ["Vender"])
app.include_router(ahmedabad_router, prefix="/ahmedabad", tags= ["Ahmedabad Salary Structure 1"])
app.include_router(surat_zomato_structure2_router, prefix= "/surat", tags=["Surat Structure 2"])
app.include_router(surat_swiggy_structure2_router, prefix='/surat', tags=["Surat Structure 2"])
# app.include_router(master_router, prefix='/surat')
app.include_router(ahmedabad_flipkart_router, prefix='/ahmedabad', tags= ["Ahmedabad Salary Structure 1"])
app.include_router(ahmedabad_ecom_router, prefix='/ahmedabad', tags= ["Ahmedabad Salary Structure 1"])
app.include_router(ahmedabad_blinkit_router, prefix='/ahmedabad', tags= ["Ahmedabad Salary Structure 1"])
app.include_router(ahmedabadbigbascket, prefix="/ahmedabad", tags= ["Ahmedabad Salary Structure 1"])
app.include_router(ahmedabadbbnow_router, prefix="/ahmedabad", tags= ["Ahmedabad Salary Structure 1"])
app.include_router(inventory_router)




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
