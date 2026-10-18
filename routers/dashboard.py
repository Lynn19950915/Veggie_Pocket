from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

import json
from pathlib import Path
from sqlmodel import Session
from database import get_session
from models.restaurant import Restaurant


router = APIRouter()
# 建立模板引擎、讀取共用資料
templates = Jinja2Templates(directory="templates")
DISTRICTS = json.loads(Path("data/districts.json").read_text(encoding="utf-8"))
CATEGORIES = json.loads(Path("data/categories.json").read_text(encoding="utf-8"))


@router.get("/dashboard")
def load_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, name="dashboard.html",
        context={"districts": DISTRICTS, "categories": CATEGORIES}
    )

@router.post("/dashboard")
def create_restaurant(
    brand: str = Form(...),
    branch: str | None = Form(None),
    district: str = Form(...),
    address: str = Form(...),
    category: str = Form(...),
    time_limit: int | None = Form(None),
    level: int = Form(...),
    station: str | None = Form(None),
    stroke: int = Form(...),
    map_url: str = Form(...),
    db: Session = Depends(get_session)
):
    restaurant = Restaurant(
        brand=brand,
        branch=branch,
        district=district,
        address=address,
        category=category,
        time_limit=time_limit,
        level=level,
        station=station,
        stroke=stroke,
        map_url=map_url,
    )
    db.add(restaurant)
    db.commit()
    
    return RedirectResponse(url="/dashboard", status_code=303)
