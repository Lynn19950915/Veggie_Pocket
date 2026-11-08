from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

import json
from pathlib import Path
from sqlmodel import Session, select, func, case
from database import get_session
from models.restaurant import Restaurant


router = APIRouter()
# 建立模板引擎、讀取共用資料
templates = Jinja2Templates(directory="templates")
DISTRICTS = json.loads(Path("data/districts.json").read_text(encoding="utf-8"))
CATEGORIES = json.loads(Path("data/categories.json").read_text(encoding="utf-8"))

def restruct_data(data):
    DISTRICT_MAP = {district["code"]: district["name"] for district in DISTRICTS}
    stats = {
        "district": [],
        "level1": [],
        "level2": [],
        "level3": [],
    }
    
    for item in data:
        stats["district"].append(DISTRICT_MAP.get(item.district))
        stats["level1"].append(item.level1)
        stats["level2"].append(item.level2)
        stats["level3"].append(item.level3)

    return stats


@router.get("/statistic")
def load_statistic(
    request: Request,
    db: Session = Depends(get_session)
):
    # 行政區中各自由度的店家數
    result = db.exec(
        select(
            Restaurant.district,
            func.sum(case((Restaurant.level == 1, 1), else_=0)).label("level1"),
            func.sum(case((Restaurant.level == 2, 1), else_=0)).label("level2"),
            func.sum(case((Restaurant.level == 3, 1), else_=0)).label("level3"),
        )
        .group_by(Restaurant.district)
        .order_by(func.count(Restaurant.id).desc())
    ).all()
    stats1 = restruct_data(result)
    
    # 計算各分類的品牌、店家數
    stats2 = db.exec(
        select(
            Restaurant.category,
            Restaurant,
            func.count(func.distinct(Restaurant.brand)).label("brand_count"),
            func.count(Restaurant.id).label("restaurant_count"),
        )
        .group_by(Restaurant.category)
    ).all()
    total_brand = sum(row.brand_count for row in stats2)
    total_restaurant = sum(row.restaurant_count for row in stats2)
   
    stats3 = db.exec(
        select(
            Restaurant.station,
            func.count(Restaurant.id).label("restaurant_count"),
        )
        .where(Restaurant.station != None)
        .group_by(Restaurant.station)
        .order_by(func.count(Restaurant.id).desc())
        .limit(5)
    ).all()
    
    
    return templates.TemplateResponse(
        request=request, name="statistic.html",
        context={
            "stats1": stats1, "stats2": stats2, "stats3": stats3,
            "total_brand": total_brand, "total_restaurant": total_restaurant,
        }
    )
