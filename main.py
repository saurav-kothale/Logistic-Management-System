from fastapi import FastAPI
from salary.route import salary_router
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
import uvicorn


app = FastAPI()

templates = Jinja2Templates(directory="template")

# Serve static files (CSS and JS)
app.mount("/static", StaticFiles(directory="template/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(salary_router)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)