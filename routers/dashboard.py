from fastapi import APIRouter, Request, Form, Depends, HTTPException
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
    time_limit: int | None = Form(None, gt=0),  # 可為空值，有填則必為正
    level: int = Form(..., ge=1, le=3),
    station: str | None = Form(None),
    stroke: int = Form(..., ge=0),
    map_url: str = Form(...),
    db: Session = Depends(get_session)          # 依賴注入: 自動取得工作階段
):
    district_list = {item["code"] for item in DISTRICTS}
    category_list = {item["code"] for item in CATEGORIES}
    if district not in district_list or category not in category_list:
        raise HTTPException(
            status_code=422,
            detail="無效的行政區或餐廳分類"
        )
    
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
