from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import json
from pathlib import Path


app = FastAPI()
# 掛載靜態資源、建立模板引擎
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DISTRICTS = json.loads(Path("data/districts.json").read_text(encoding="utf-8"))
CATEGORIES = json.loads(Path("data/categories.json").read_text(encoding="utf-8"))

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", 
    )

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, name="dashboard.html",
        context={"districts": DISTRICTS, "categories": CATEGORIES}
    )
