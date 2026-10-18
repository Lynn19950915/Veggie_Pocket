from sqlmodel import SQLModel, Field
from pydantic import NaiveDatetime
from datetime import datetime, timezone, timedelta


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
    stroke: int
    map_url: str
    
    # 強制改寫成時區的時間
    created_at: NaiveDatetime = Field(
        default_factory=lambda: datetime.now(TW_TZ).replace(
            tzinfo=None, second=0, microsecond=0
        )
    )
