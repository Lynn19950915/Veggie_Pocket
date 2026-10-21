from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates

import json
from pathlib import Path
from sqlmodel import Session, select, func, literal
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
    district: str | None = None,
    db: Session = Depends(get_session)
):
    # 各行政區的店家統計
    stats = db.exec(
        select(
            Restaurant,
            func.count(Restaurant.id).label("district_count")
        ).group_by(
            Restaurant.district
        ).order_by(
            func.count(Restaurant.id).desc()
        )
    ).all()
    total = sum(row.district_count for row in stats)
    
    
    district_list = {item["code"] for item in DISTRICTS}
    if district in district_list:
        restaurants = db.exec(
            select(
                Restaurant,
                literal(1).label("branch_count")
            ).where(
                Restaurant.district == district
            )
        ).all()
    elif not district:
        # 品牌: 多間分店的資料會整合成一筆
        restaurants = db.exec(
            select(
                Restaurant,
                func.count(Restaurant.id).label("branch_count")
            ).group_by(
                Restaurant.brand
            )
        ).all()
    else:
        raise HTTPException(status_code=422, detail="無效的行政區")
    
    restaurants = sorted(
        restaurants,
        key = lambda row: (
            row.Restaurant.stroke,
            row.Restaurant.district_info["order"],
            row.Restaurant.id
        )
    )
    
    
    return templates.TemplateResponse(
        request=request, name="index.html",
        context={
            "stats": stats, "total": total,
            "restaurants": restaurants, "now": datetime.now()
        }
    )
