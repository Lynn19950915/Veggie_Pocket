from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

import json
from pathlib import Path
from sqlmodel import Session, select
from database import get_session
from models.restaurant import Restaurant
from datetime import datetime


router = APIRouter()
# 建立模板引擎、讀取共用資料
templates = Jinja2Templates(directory="templates")
DISTRICTS = json.loads(Path("data/districts.json").read_text(encoding="utf-8"))
CATEGORIES = json.loads(Path("data/categories.json").read_text(encoding="utf-8"))

@router.get("/")
def load_index(
    request: Request,
    db: Session = Depends(get_session)
):
    restaurants = db.exec(select(Restaurant)).all()
    return templates.TemplateResponse(
        request=request, name="index.html",
        context={"restaurants": restaurants, "now": datetime.now()}
    )
