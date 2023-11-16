from fastapi import FastAPI
from app.salary.route import salary_router
from app.User.views.route import login_router, signup_router
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

templates = Jinja2Templates(directory="template/login-form-07")

# Serve static files (CSS and JS)
app.mount("/static", StaticFiles(directory="template/login-form-07/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    return templates.TemplateResponse("demo.html", {"request": request})


app.include_router(salary_router)
app.include_router(signup_router)
app.include_router(login_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)