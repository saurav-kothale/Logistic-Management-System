from fastapi import FastAPI
from app.salary.route import salary_router
from app.User.views.route import login_router, signup_router
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.file_system.route import file_router

app = FastAPI()


app.include_router(salary_router)
app.include_router(signup_router)
app.include_router(login_router)
app.include_router(file_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)