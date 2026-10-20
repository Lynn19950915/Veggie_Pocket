from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates

from database import create_db
from routers import dashboard, index


# 服務啟動前，建立好資料表
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)
# 掛載靜態資源路徑
app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# 由頁面各自處理請求
app.include_router(dashboard.router)
app.include_router(index.router)
