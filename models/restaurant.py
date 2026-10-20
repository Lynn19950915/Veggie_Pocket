from sqlmodel import SQLModel, Field
import json
from pathlib import Path
from pydantic import NaiveDatetime
from datetime import datetime, timezone, timedelta


# 供查詢用的編碼對應表
DISTRICTS = json.loads(Path("data/districts.json").read_text(encoding="utf-8"))
DISTRICT_MAP = {district["code"]: district["name"] for district in DISTRICTS}
CATEGORIES = json.loads(Path("data/categories.json").read_text(encoding="utf-8"))
CATEGORY_MAP = {category["code"]: category for category in CATEGORIES}

TW_TZ = timezone(timedelta(hours=8))

class Restaurant(SQLModel, table=True):
    # 建立物件後，db 會自動生成 id
    id: int | None = Field(default=None, primary_key=True)
    brand: str
    branch: str | None = None
    district: str
    address: str
    
    category: str
    time_limit: int | None = None
    level: int = Field(ge=1, le=3)
    station: str | None = None
    stroke: int = Field(ge=0)
    map_url: str
    # 強制改寫成時區的時間
    created_at: NaiveDatetime = Field(
        default_factory=lambda: datetime.now(TW_TZ).replace(
            tzinfo=None, second=0, microsecond=0
        )
    )

    @property
    def district_name(self) -> str:
        return DISTRICT_MAP.get(self.district)
    # 包含該分類的 icon 及色碼
    @property
    def category_info(self) -> dict:
        return CATEGORY_MAP.get(self.category)
